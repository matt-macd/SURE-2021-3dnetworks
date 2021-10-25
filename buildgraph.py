import Network
import pandas as pd 
import numpy as np 

df = pd.DataFrame(pd.read_csv("nodecoords_prox_femur_head.csv"))
vals = df.to_numpy()

minval = vals.min()
maxval = vals.max()
diff = maxval-minval

xvals = []
yvals = []
zvals = []

nwrk = Network.Network()

i=0

for coords in vals:
    x1 = coords[0] + (coords[3]-coords[0])/2
    y1 = coords[1] + (coords[4]-coords[1])/2  # pre transformed coords
    z1 = coords[2] + (coords[5]-coords[2])/2
    
    x = ((x1-minval)/diff)*15
    y = ((y1-minval)/diff)*15  # translate to 0 = minval, 15 = maxval 
    z = ((z1-minval)/diff)*15
    
    xvals.append(x)
    yvals.append(y)
    zvals.append(z)
    nwrk.G.add_node(i, pos=[x, y, z])

    i=i+1
    
nwrk.nodexvals = xvals
nwrk.nodeyvals = yvals
nwrk.nodezvals = zvals

nwrk.visualizeGraph(True)


    
    