import math
import random
import networkx as nx
import plotly.subplots as sp
import plotly.graph_objs as go

def plot_graph(G, save=False):
    pos = nx.get_node_attributes(G, 'pos')
    nodes = G.nodes()
    x, y, z = zip(*[pos[v] for v in G.nodes()])

    node_names = list(G.nodes())
    # Create a scatter plot for the nodes
    node_scatter = go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(
        size=10, color='red'), text=node_names)

    # Create a scatter plot for the edges
    edge_x, edge_y, edge_z = [], [], []
    for u, v in G.edges():
        x1, y1, z1 = pos[u]
        x2, y2, z2 = pos[v]
        edge_x.extend([x1, x2, None])
        edge_y.extend([y1, y2, None])
        edge_z.extend([z1, z2, None])
    edge_scatter = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z, mode='lines', line=dict(width=2, color='blue'))

    # Create a subplot with 3D scatter plots for nodes and edges
    fig = sp.make_subplots(rows=1, cols=1, specs=[[{'type': 'scatter'}]])
    fig.add_trace(node_scatter)
    fig.add_trace(edge_scatter)

    # Set the axis limits
    fig.update_layout(scene=dict(xaxis=dict(range=[-100, 100], autorange=False),
                                 yaxis=dict(range=[-100, 100], autorange=False),
                                 zaxis=dict(range=[-230, 10], autorange=False)),)

    if save:
        fig.write_html('graph.html')
        print('Graph saved to graph.html')
    else:
        fig.show()
        print('Graph displayed')


def random_point_on_sphere(r):
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    z = random.uniform(-1, 0)

    x *= r
    y *= r
    z *= r

    normalization_factor = math.sqrt(x**2 + y**2 + z**2)
    x /= normalization_factor
    y /= normalization_factor
    z /= normalization_factor

    return x, y, z
