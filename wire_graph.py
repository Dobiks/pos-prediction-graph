import networkx as nx
from graph_utils import plot_graph
import numpy as np
import pandas as pd

SAVE_GRAPH = True
ONLY_STATIC = False

static = pd.read_csv('corrected_static.csv')
detected = pd.read_csv('rotated_graph.csv')
static['name'] = static['name'].str.replace(' ', '')
detected['name'] = detected['name'].str.replace(' ', '')

G = nx.Graph()
G2 = nx.Graph()
for i in range(len(static)):
    G.add_node(static['name'][i], pos=(static['x'][i], static['z'][i], static['y'][i]))

for i in range(len(detected)):
    G2.add_node(detected['name'][i], pos=(detected['x'][i], detected['z'][i], detected['y'][i]))

#add parent basing on static['parent']
for i in range(len(static)):
    if static['parent'][i] != 0 and static['parent'][i] != '0':
        G.add_edge(static['name'][i], static['parent'][i])

if ONLY_STATIC: G2 = None
plot_graph(G, G2, save = SAVE_GRAPH)

