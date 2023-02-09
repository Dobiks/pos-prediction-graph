import networkx as nx
import plotly.subplots as sp
import plotly.graph_objs as go
import pandas as pd

G = nx.Graph()

# Add nodes with positions
G.add_node('root', pos=(0, 0, 0))
G.add_node('node_1', pos=(-15, 0, -20))
G.add_node('node_2', pos=(15, 0, -20))
G.add_node('node_3', pos=(-20, 0, -45.5))
G.add_node('node_4', pos=(-14, -2, -29.9))
G.add_node('node_5', pos=(-5, 2, -48.3))

# Add edges to specify parent-child relationships
G.add_edge('root', 'node_1')
G.add_edge('root', 'node_2')
G.add_edge('node_1', 'node_3')
G.add_edge('node_1', 'node_4')
G.add_edge('node_1', 'node_5')

# Plot the graph in 3D
pos = nx.get_node_attributes(G, 'pos')
x, y, z = zip(*[pos[v] for v in G.nodes()])

# Create a scatter plot for the nodes
node_scatter = go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(size=10, color='red'))

# Create a scatter plot for the edges
edge_x, edge_y, edge_z = [], [], []
for u, v in G.edges():
    x1, y1, z1 = pos[u]
    x2, y2, z2 = pos[v]
    edge_x.extend([x1, x2, None])
    edge_y.extend([y1, y2, None])
    edge_z.extend([z1, z2, None])
edge_scatter = go.Scatter3d(x=edge_x, y=edge_y, z=edge_z, mode='lines', line=dict(width=1, color='blue'))

# Create a subplot with 3D scatter plots for nodes and edges
fig = sp.make_subplots(rows=1, cols=1, specs=[[{'type': 'scatter'}]])
fig.add_trace(node_scatter)
fig.add_trace(edge_scatter)

fig.show()
