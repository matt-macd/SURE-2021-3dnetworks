import Network as nwrk
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash_extensions.enrich import Input, Output, State, DashProxy, MultiplexerTransform


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

graph = nwrk.Network()

colours = {'text' : '#27213C'}

app = DashProxy(__name__, external_stylesheets=external_stylesheets, transforms=[MultiplexerTransform()], prevent_initial_callbacks=True)


app.layout = html.Div([html.Div([html.H4("Interactive Visualization of 3D Lattices", style={'textAlign' : 'center', 'backgroundColor' : '#ff9999'}
)]), 
    
html.Div([
html.Div([html.H6('Lattice Visualization', style={'textAlign':'center', 'backgroundColor':'#cce6ff'})]),
html.Div([dcc.Graph(id='network')], style={'margin-top':'10px'}),
            
html.Div([dcc.Dropdown(id='symmetry_selector', options=[{'label' : 'Hexagonal Symmetry', 'value' : 'HEX'}, {'label' : 'Cubic Symmetry', 'value' : 'CUB'}, {'label' : 'Body Center Cubic Symmetry', 'value' : 'BCC'}], value='CUB')], style={'width' : '30%', 'display' : 'inline-block', 'margin-left':'75px'}),

html.Div([dcc.Input(id='length', type='number', placeholder='Length', value=0)], style={'display' : 'inline-block'}), 

html.Div([html.Button('Generate Lattice', id='generate', n_clicks=0)],style={'display' : 'inline-block', 'margin-bottom':'30px'}),

html.Div([html.H6('Chaos Slider - 0-100%', style={'textAlign':'center','backgroundColor':'#cce6ff', 'margin-bottom':'30px'})]),
    
html.Div([dcc.Slider(id='chaos',min=0, max=1, step = 0.01, value=0, tooltip = { 'always_visible': True })], style={'width':'50%', 'margin-top':'5px', 'margin-left':'180px'}),
html.Div(children=[dcc.Input(id='minrad', type='number', placeholder='Minimum Edge Radius')], style={'display':'inline-block', 'margin-left':'100px'}),
html.Div([html.H6('------------------')], style={'display':'inline-block', 'color':'red'}),
html.Div(children=[dcc.Input(id='maxrad', type='number', placeholder='Maximum Edge Radius')], style={'display':'inline-block'}),
html.Div(style={'backgroundColor':'#FFD4CB'}),
html.Div([html.H6('Kinks')], style={'display':'inline-block', 'margin-left':'175px'}),
html.Div([html.H6('Deadends')], style={'display':'inline-block', 'margin-left': '275px'}),
html.Div(style={'backgroundColor':'#FFD4CB'}),
html.Div([dcc.Dropdown(id='kinks', options=[{'label':'No kink straightening', 'value':'yeskinks'}, {'label':'Straighten kinks', 'value':'nokinks'}])], style={'width':'45%', 'margin-left':'29px', 'display':'inline-block'}),
html.Div([dcc.Dropdown(id='deadends', options=[{'label':'Prune', 'value':'prune'}, {'label':'Connect to nearest neighbor', 'value':'connect'}, {'label':'Do nothing', 'value':'nada'}])], style={'width':'45%', 'display':'inline-block'}),
html.Div(style={'margin-bottom':'30px'}),
html.Div(children=[html.Button('Randomize', id='randomize', n_clicks=0)], style={'margin-bottom':'30px','margin-left':'290px'}),
html.Div([html.H6('Select node valence to display angle distribution', style={'textAlign':'center', 'margin-bottom':'35px','backgroundColor':'#cce6ff'})]),
html.Div(dcc.Checklist(id='checker',
    options=[
        {'label': '2', 'value': 2},
        {'label': '3', 'value': 3},
        {'label': '4', 'value': 4},
        {'label': '5', 'value': 5},
        {'label': '6', 'value': 6},
        {'label': '7', 'value': 7},
        {'label': '8', 'value': 8},  
    ],
    value=[],
    labelStyle={'display': 'inline-block', 'width':'80px'}), style={'margin-left' : '115px', 'margin-bottom' : '35px', 'backgroundColour':'#e0e0eb'}),
html.Div(id='dummy'),
html.Div(id='numnodes', style={'display':'inline-block', 'margin-left':'165px', 'margin-right':'80px'}),
html.Div(id='numedges', style={'margin-bottom':'100px','display':'inline-block'}),
html.Div([html.H6('Distribution of angles between nodes', style={'textAlign':'center','backgroundColor':'#cce6ff'})]),
html.Div([dcc.Graph(id='anglegraph')], style={'margin-top':'70px'}),
html.Div([html.H6('Node Valence', style={'textAlign':'center','backgroundColor':'#cce6ff'})]),
html.Div([dcc.Graph(id='valencegraph')], style={'column-count':'1'})], style={'column-count':'2'})])


@app.callback(
    Output('network', 'figure'),
    [Input('generate', 'n_clicks')],
    state = [State('symmetry_selector', 'value'),
    State('length', 'value')])
def selectSymmetry(n_clicks, symmetry_selector, length):
    
    if symmetry_selector == 'HEX':
        graph.setHexagonalSymmetry(length=length)
        graph.visualizeGraph(bool=False)
        return graph.fig
    
    if symmetry_selector == 'CUB':
        graph.setCubicSymmetry(length=length)
        graph.visualizeGraph(bool=False)
        return graph.fig 
    
    if symmetry_selector == 'BCC':
        graph.setBodyCenterCubic(length=length)
        graph.visualizeGraph(bool=False)
        return graph.fig 
    
    
@app.callback(
    Output('anglegraph', 'figure'),
    Output('valencegraph', 'figure'),   
    Input('network', 'figure'),
    Input('checker', 'value'))
def updateData(figure, value):
    
    if len(value) == 0:
        graph.findAngles()
        graph.visualizeAngles(bool=False)
        graph.plotDegree(bool=False)
        return graph.anglefig, graph.degreefig
    else:
        x = graph.findSpecificValenceAngles(value=value)
        graph.plotDegree(bool=False)
        
        return x, graph.degreefig
    
    
@app.callback(
    Output('network', 'figure'),
    [Input('randomize', 'n_clicks')],
    state=[State('chaos', 'value'),
     State('minrad', 'value'),
     State('maxrad', 'value'),
     State('kinks', 'value'),
     State('deadends', 'value')])
def randomize(clicks, chaos, minrad, maxrad, kinks, deadends):
    
    graph.randomize(chaosmult=chaos, minrad=minrad, maxrad=maxrad)
    graph.declutter()
    
    if deadends=='nada':
        pass
    
    if deadends=='prune':
        graph.prune()
        
    if deadends=='connect':
        graph.connectNeighbours()
        
    if kinks=='nokinks':
        graph.removeKinks()
        
    if deadends=='prune':
        graph.prune()    
        
    if kinks=='nokinks':
        graph.removeKinks()
    
    if deadends=='connect':
        graph.connectNeighbours()    
    
    if kinks=='yeskinks':
        pass
        
    graph.declutter()
    
    graph.visualizeGraph(bool=False)
    
    return graph.fig

@app.callback(
    Output('numnodes', 'children'),
    Output('numedges', 'children'),
    Input('network', 'figure'))
def updateNumNodesEdges(figure):
    nodes = 'Number of Nodes: {}'.format(graph.G.number_of_nodes())
    edges = 'Number of Edges: {}'.format(graph.G.number_of_edges())
    return nodes, edges

    
if __name__ == '__main__':
    app.run_server(debug=True)
    
    

        
    
















