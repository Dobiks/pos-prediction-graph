import networkx as nx
from graph_utils import plot_graph

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

plot_graph(G)