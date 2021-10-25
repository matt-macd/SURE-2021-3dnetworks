import networkx as nx
import numpy as np
import plotly.graph_objects as go
import random
from itertools import permutations
from noise import snoise4

'''
The 'Network' class contains everything I used to not only generate and randomize symmetrical lattices, but also everything needed to visualize some of the data they produce.
Used networkx to store the networks and manipulate them easily, and Plotly/Dash to visualize data. More detailed descriptions are available within the functions
If you have any questions don't hesitate to reach out - email is matthew.macdonald3@mail.mcgill.ca
'''


class Network:

    def __init__(self):    #
        
        self.G = nx.Graph()     # New networkx graph object 
        
        self.symmetry = None    # Can be cubic/bcc/hexagonal/randomized 
        
        self.nodexvals = None   # stores the x/y/z coordinates of each node 
        self.nodeyvals = None   # *** INDEX IN THE LIST IS THE LABEL FOR THE NODE ** 
        self.nodezvals = None   # -> for  example, node with label '1''s x coordinate is stored at self.nodexvals[1]
        
        self.unitcell = None    # unit cell size for each symmetrical lattices
        self.angles = None      # list of angles between edges --> have to run findAngles method to have something stored there
        
        self.degreefig = None   # the plotly figure object --> for ex. do self.degreefig.show() if you want it displayed
        self.anglefig = None    # same as above 
        
        self.fig = None         # plotly figure of the entire lattice w/ nodes and edges

    def setHexagonalSymmetry(self, length): 
        
        '''
        sets Network object to hexagonal symmetry
        length = positive integer
        '''
        
        self.G.clear()
        
        xvals = []
        yvals = []
        zvals = []
        
        for z in range(length):
            for y in range(length):
                for x in range(length):
                    if y%2 == 0:
                        if x%4 == 0:
                            xvals.append(x)
                            yvals.append(y)
                            zvals.append(z)
                            
                            xvals.append(x+np.sqrt(2))
                            yvals.append(y)
                            zvals.append(z)
                        
                    if y%2 != 0:
                        if x%4 != 0 and x%2 == 0:
                            xvals.append(x)
                            yvals.append(y)
                            zvals.append(z)
                            
                            xvals.append(x+np.sqrt(2))
                            yvals.append(y)
                            zvals.append(z)
        
                        
        for i in range(len(xvals)):
            self.G.add_node(i, pos=[xvals[i], yvals[i], zvals[i]])
        
        for i in range(len(self.G.nodes)):
            for j in range(len(self.G.nodes)):
                
                node1 = np.array(self.G.nodes[i]['pos'])
                node2 = np.array(self.G.nodes[j]['pos'])
                
                distance = np.linalg.norm(node1-node2)
                
                if distance != 0 and distance <= (np.sqrt(2) + 0.2):
                    if not (node1[0] != node2[0] and node1[2] != node2[2]):
                        self.G.add_edge(i, j)
        
        self.symmetry = "Hexagonal"
        
        self.nodexvals = xvals
        self.nodeyvals = yvals
        self.nodezvals = zvals  
        
        self.unitcell = np.sqrt(2)
        
        return self.G
    
    def setCubicSymmetry(self, length):
        '''
        sets Network object to cubic symmetry
        length = positive integer
        '''        
        self.G.clear()
        
        xvals = []
        yvals = []
        zvals = []
        
        for x in range(0, length+1):
            for y in range(0, length+1):
                for z in range(0, length+1):
                    xvals.append(x)
                    yvals.append(y)
                    zvals.append(z)    
        
        for i in range(len(xvals)):
            self.G.add_node(i, pos=[xvals[i], yvals[i], zvals[i]])
                    
        for i in range(len(self.G.nodes)):
            for j in range(len(self.G.nodes)):
                
                node1 = np.array(self.G.nodes[i]['pos'])
                node2 = np.array(self.G.nodes[j]['pos'])
                
                distance = np.linalg.norm(node1-node2)
                
                if distance != 0 and distance <= 1:
                    self.G.add_edge(i, j)
        
        self.symmetry = "Cubic"
        
        self.nodexvals = xvals
        self.nodeyvals = yvals
        self.nodezvals = zvals
        
        self.unitcell = 1 
        
        return self.G
        
    def setBodyCenterCubic(self, length):
        '''
        sets Network object to BCC symmetry
        length = positive integer
        '''        
        
        self.G.clear()
        
        xvals = []
        yvals = []
        zvals = []
        
        for x in range(0, length+1):
            for y in range(0, length+1):
                for z in range(0, length+1):
                    xvals.append(x)
                    yvals.append(y)
                    zvals.append(z)
                    
                    xvals.append(x+0.5)
                    yvals.append(y+0.5)
                    zvals.append(z+0.5)
    
        for i in range(len(xvals)):
            self.G.add_node(i, pos=[xvals[i], yvals[i], zvals[i]])
        
        for i in range(len(self.G.nodes)):
            for j in range(len(self.G.nodes)):
                
                node1 = np.array(self.G.nodes[i]['pos'])
                node2 = np.array(self.G.nodes[j]['pos'])
                
                distance = np.linalg.norm(node1-node2)
                
                if distance != 0 and distance <= 1:
                    self.G.add_edge(i, j)
        
        self.symmetry = "BCC"
        
        self.nodexvals = xvals
        self.nodeyvals = yvals
        self.nodezvals = zvals   
        
        self.unitcell = 1 
        
        return self.G
    
    def visualizeGraph(self, bool):
        '''
        Creates a plotly figure to visualize the lattice. if bool=True then the plot is 
        displayed, else the plot is just stored in self.fig
        '''
        
        x = self.nodexvals
        y = self.nodeyvals
        z = self.nodezvals
   
        nodeTrace = go.Scatter3d(
                x=x,
                y=y, 
                z=z, 
                mode = 'markers', 
                marker = dict(size=3))
        
            
        x_lines = list()
        y_lines = list()
        z_lines = list()
        
        
        edge_list = list(self.G.edges())
        
        
        for pairs in edge_list:
            for i in range(2):
                x_lines.append(self.nodexvals[pairs[i]])
                y_lines.append(self.nodeyvals[pairs[i]])
                z_lines.append(self.nodezvals[pairs[i]])
            x_lines.append(None)
            y_lines.append(None)
            z_lines.append(None)
                
        
        
        edgeTrace = go.Scatter3d(
            x=x_lines,
            y=y_lines,
            z=z_lines,
            mode='lines')
        
        fig = go.Figure(data=[nodeTrace, edgeTrace])
        
        self.fig = fig
        
        if bool == True:
            fig.show()    
        
        
    def randomize(self, chaosmult, minrad, maxrad):
        '''
        Randomizes a lattice. Call this on a Network object that has already had a symmetry set.
        chaosmult = float between 0 and 1.0, weights the randomization
        minrad = any positive number --> sets the minimum radius for reconnection after all the nodes have been randomized
        maxrad = any positive number --> sets the maximum radius for reconnection after all the nodes have been randomized
        '''
        
        def getRandVector(coords):
            '''
            Generates a random vector implementing Perlin Noise
            
            coords = list of length 3, [x, y, z] 
            '''
            #Gets a randomization vector with perlin noise implemented 
            noisevalues = [abs(snoise4(coords[0], coords[1], coords[2], random.random())), abs(snoise4(coords[0], coords[1], coords[2], random.random())), abs(snoise4(coords[0], coords[1], coords[2], random.random())), abs(snoise4(coords[0], coords[1], coords[2], random.random()))]
            
            #We use noise4 so that we can seed the shift with a random variable (random.random())
            
            randvector = [np.sqrt(-2*np.log(noisevalues[0]))*np.cos(2*np.pi*noisevalues[1]), noisevalues[2], np.arccos(1-2*noisevalues[3])]
            
            
            
            return randvector        
        
        
        neighbours = {}  # neighbors stores all the 2nd degree neighbours of each node --> the randomization of each node is dependent on the randomization of all other nodes to 2 degrees. 
        
        for i in range(len(self.nodexvals)):
            temp = [n for n in self.G.neighbors(i)]
            iterneigh = [n for n in self.G.neighbors(i)]
            for j in iterneigh:
                temp2 = [n for n in self.G.neighbors(j)]
                for vals in temp2:
                    temp.append(vals)
            neighbours[i] = temp

         
        randnodes = []
            
        for j in range(len(neighbours.keys())):
            
            if j not in randnodes:
                
                nnodes = []
                
                for n in neighbours[j]:
                    nnodes.append(n)
                
                coords = [self.nodexvals[j], self.nodeyvals[j], self.nodezvals[j]]
                
                shift = getRandVector(coords=coords)
                
                self.nodexvals[j] = self.nodexvals[j]+shift[0]*chaosmult*self.unitcell
                self.nodeyvals[j] = self.nodeyvals[j]+shift[1]*chaosmult*self.unitcell
                self.nodezvals[j] = self.nodezvals[j]+shift[2]*chaosmult*self.unitcell
                
                randnodes.append(j)
            else:
                pass
            
            for k in nnodes:
                if k in randnodes:
                    continue
                else: 
                    coords = [self.nodexvals[k], self.nodeyvals[k], self.nodezvals[k]]
                    
                    shift1 = getRandVector(coords=coords)
                    
                    self.nodexvals[k] = self.nodexvals[k]+shift1[0]*chaosmult*self.unitcell
                    self.nodeyvals[k] = self.nodeyvals[k]+shift1[1]*chaosmult*self.unitcell
                    self.nodezvals[k] = self.nodezvals[k]+shift1[2]*chaosmult*self.unitcell 
                    
                    randnodes.append(k)
                    
        
        self.G.clear()
        
        for j in range(len(self.nodexvals)):
            self.G.add_node(j, pos=[self.nodexvals[j], self.nodeyvals[j], self.nodezvals[j]])
    
        for i in range(len(self.G.nodes)):
            for j in range(len(self.G.nodes)):
    
                node1 = np.array(self.G.nodes[i]['pos'])
                node2 = np.array(self.G.nodes[j]['pos'])
    
                distance = np.linalg.norm(node1-node2)
    
                if distance != 0 and minrad <= distance <= maxrad:
                    self.G.add_edge(i, j)
    
        self.symmetry = "Randomized"        
        
        
    def plotDegree(self, bool):
        '''
        plots the node valence 
        bool = True or False --> if True, figure is displayed, else it is just stored in self.degreefig
        '''

        
        degrees = [val for (node, val) in self.G.degree()]
        
        degrees.sort()
        
        frequency = {}
        
        for num in degrees:
            if(num in frequency):
                frequency[num] += 1
            else:
                frequency[num] = 1
                
        xvals = list(range(degrees[-1]+1))
        
        yvals = [0]*(degrees[-1]+1)
        
        for key in frequency:
            yvals[key] = frequency[key]
        
        fig = go.Figure([go.Bar(x=xvals, y=yvals)])
        fig.update_xaxes(title_text = 'Node Valence')
        fig.update_layout(title={'text':'Lattice Node Valence', 'xanchor': 'center', 'yanchor':'top'}, title_x=0.5)
        
        self.degreefig = fig 
        
        if bool == True:
            fig.show()
          
    def declutter(self):
        '''
        Gets rid of all isolated nodes
        '''
                
        self.G.remove_nodes_from(list(nx.isolates(self.G)))
        
        components = list(nx.connected_components(self.G))
        if len(components) != 0:
            biggest_component_size = max(len(c) for c in components)
            problem_components = [c for c in components if len(c) != biggest_component_size]
            for component in problem_components:
                for node in component:
                    self.G.remove_node(node)        
                              
            
            for x in range(len(self.nodexvals)):
                self.nodexvals[x] = None
                self.nodeyvals[x] = None
                self.nodezvals[x] = None
            
            for i in self.G.nodes:
                self.nodexvals[i] = self.G.nodes[i]['pos'][0]
                self.nodeyvals[i] = self.G.nodes[i]['pos'][1]
                self.nodezvals[i] = self.G.nodes[i]['pos'][2]
            
        
    
    
    def findAngles(self):
        '''
        Finds all the angles, stores them in self.angles, but does not display them or create a figure --> see visualizeAngles() for that 
        '''
        
        angles = []
        
        for node in self.G.nodes:
            perms = permutations(list(self.G.neighbors(node)), 2)
            
            nodecoords = np.array(self.G.nodes[node]['pos'])
            
            for combs in list(perms):
                
                edge1 = np.array(self.G.nodes[list(combs)[0]]['pos'])
                edge2 = np.array(self.G.nodes[list(combs)[1]]['pos'])
                
                nc1 = edge1 - nodecoords
                nc2 = edge2 - nodecoords
                
                cosine_angle = np.dot(nc1, nc2) / (np.linalg.norm(nc1) * np.linalg.norm(nc2))
                angle = np.arccos(cosine_angle) 

                angles.append(angle)
            
                
        self.angles = np.rad2deg(angles)
        
    def visualizeAngles(self, bool):
        '''
        Creates a plotly figure 
        self.findAngles() must be called first/
        bool = True or False, if True the figure will be displayed, else it will be store in self.anglefig
        '''
        
        fig = go.Figure(data=[go.Histogram(x = self.angles)])
        
        fig.update_xaxes(title_text = 'Angle between nodes (degrees)')
        
        
        fig.update_layout(title={'text':'Distribution of angles between nodes', 'xanchor': 'center', 'yanchor':'top'}, title_x=0.5)
        
        self.anglefig = fig
        
        if bool == True:
            fig.show()
    
    def findSpecificValenceAngles(self, value):
        '''
        Finds and returns a fig of the angles for nodes of a specified valence
        value = integer from 1 to highest valence value
        '''
        
        vnodes = []
        angles = []
    
        for node in self.G.nodes:
            if self.G.degree[node] in value:
                vnodes.append(node)
                
        for node in vnodes:
            perms = permutations(list(self.G.neighbors(node)), 2)
            
            nodecoords = np.array(self.G.nodes[node]['pos'])
            
            for combs in list(perms):
                
                edge1 = np.array(self.G.nodes[list(combs)[0]]['pos'])
                edge2 = np.array(self.G.nodes[list(combs)[1]]['pos'])
                
                nc1 = edge1 - nodecoords
                nc2 = edge2 - nodecoords
                
                cosine_angle = np.dot(nc1, nc2) / (np.linalg.norm(nc1) * np.linalg.norm(nc2))
                angle = np.rad2deg(np.arccos(cosine_angle))
                
                angles.append(angle)
        
        fig = go.Figure(data=[go.Histogram(x = angles)]) 
        
        return fig
    
    def connectNeighbours(self):
        '''
        Connects deadend nodes to their nearest neighbours
        '''
        

        for node1 in self.G.nodes:
            if self.G.degree[node1] == 1:
                
                
                xnode = list(self.G.edges(node1))[0][1]
                minnode = -1
                mindistance = np.inf
                
                for node2 in self.G.nodes:
                    
                    node1coords = np.array(self.G.nodes[node1]['pos'])
                    node2coords = np.array(self.G.nodes[node2]['pos'])
                    
                    distance = np.linalg.norm(node1coords-node2coords)
                    
                    if distance != 0 and distance<mindistance and node2 != xnode:
                        mindistance = distance
                        minnode  = node2
                        
                self.G.add_edge(node1, minnode)   
        for node2 in self.G.nodes:
            if self.G.degree[node2] == 1:
                
                
                xnode = list(self.G.edges(node2))[0][1]
                minnode = -1
                mindistance = np.inf
                
                for node3 in self.G.nodes:
                    
                    node1coords = np.array(self.G.nodes[node2]['pos'])
                    node2coords = np.array(self.G.nodes[node3]['pos'])
                    
                    distance = np.linalg.norm(node1coords-node2coords)
                    
                    if distance != 0 and distance<mindistance and node3 != xnode:
                        mindistance = distance
                        minnode  = node2
                        
                self.G.add_edge(node1, minnode)   
                        
                    
    def getnodedict(self):
        '''
        returns a dictionary of nodes with their xyz coordinates
        * redundant function
        '''
        
        node_pos = {}
        
        for node in self.G.nodes:
            
            node_pos[node] = self.G.nodes[node]['pos']
            
        return node_pos
    
    def removeKinks(self):
        '''
        Removes any kinks in the lattice
        '''
        for i in range(10):
            kinks = []
            for node in self.G.nodes:
                if self.G.degree[node] == 2:
                    
                    neighbors = list(self.G.neighbors(node))
                    
                    self.G.add_edge(u_of_edge=neighbors[0], v_of_edge=neighbors[1])
                    kinks.append(node)
                    self.nodexvals[node] = None
                    self.nodeyvals[node] = None
                    self.nodezvals[node] = None
                
            
            self.G.remove_nodes_from(kinks)
            kinks.clear()
            
    def prune(self):
        '''
        removes any deadends in the lattice
        '''
        for i in range(10):
            deadends = []
            for node in self.G.nodes:
                if self.G.degree[node] == 1:
                    deadends.append(node)
                
                
            self.G.remove_nodes_from(deadends)
            deadends.clear()
        
    def clear(self):  
        '''
        Clears Network object
        '''
        self.G = nx.Graph()
        self.symmetry = None
        self.nodexvals = None
        self.nodeyvals = None
        self.nodezvals = None
        self.unitcell = None
        self.angles = None 
        self.degreefig = None 
        self.anglefig = None
        self.fig = None   
            









    
                    
                    
                    
                
