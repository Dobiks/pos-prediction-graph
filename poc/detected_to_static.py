import networkx as nx
from utils.graph_utils import plot_graph
import numpy as np
import pandas as pd
from utils.transformation_utils import get_rotation, rotate_graph, get_rotation_nn, optim_rotation

SAVE_GRAPH = True

static = pd.read_csv('static_graph.csv')
detected = pd.read_csv('randomized_graph.csv')
static['name'] = static['name'].str.replace(' ', '')
detected['name'] = detected['name'].str.replace(' ', '')

G = nx.Graph()
G2 = nx.Graph()
for i in range(len(static)):
    G.add_node(static['name'][i], pos=(static['x'][i], static['z'][i], static['y'][i]))

for i in range(len(detected)):
    G2.add_node(detected['name'][i], pos=(detected['x'][i], detected['z'][i], detected['y'][i]))

for i in range(len(static)):
    if static['parent'][i] != 0 and static['parent'][i] != '0':
        G.add_edge(static['name'][i], static['parent'][i])

plot_graph(G, G2, name='before',save = SAVE_GRAPH)

# rotation = get_rotation_nn(static, detected, save_plot=True)
rotation = get_rotation_nn(static, detected, save_plot=True)
detected = rotate_graph(detected, rotation)

G2 = nx.Graph()
for i in range(len(detected)):
    G2.add_node(detected['name'][i], pos=(detected['x'][i], detected['z'][i], detected['y'][i]))

plot_graph(G, G2, name='after',save = SAVE_GRAPH)

