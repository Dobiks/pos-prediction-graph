import networkx as nx
from graph_utils import plot_graph
import pandas as pd

static = pd.read_csv('corrected_static.csv')
G = nx.Graph()

for i in range(len(static)):
    G.add_node(static['name'][i], pos=(static['x'][i], static['z'][i], static['y'][i]))

#add parent basing on static['parent']
for i in range(len(static)):
    if static['parent'][i] != '0':
        G.add_edge(static['name'][i], static['parent'][i])


plot_graph(G)

