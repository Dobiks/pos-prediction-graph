from graph_utils import plot_graph, random_point_on_sphere
import networkx as nx
import random

G = nx.read_gml('graph.gml')

positions = nx.get_node_attributes(G, 'pos')

for i, node in enumerate(G.nodes()):
    if i == 0: continue
    neighbors = list(G.neighbors(node))
    parent = neighbors[0]

    x, y, z = positions[parent]
    print(x, y, z)

        # positions[node] = (x, y, z)
        


plot_graph(G)