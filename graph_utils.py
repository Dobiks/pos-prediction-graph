import math
import random
import networkx as nx
import plotly.subplots as sp
import plotly.graph_objs as go


def plot_graph(static_graph, detected_graph=None, save=False):
    pos = nx.get_node_attributes(static_graph, 'pos')
    nodes = static_graph.nodes()
    x, y, z = zip(*[pos[v] for v in static_graph.nodes()])

    node_names = list(static_graph.nodes())
    # Create a scatter plot for the nodes
    node_scatter = go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(
        size=10, color='red'), text=node_names)

    # Create a scatter plot for the edges
    edge_x, edge_y, edge_z = [], [], []
    for u, v in static_graph.edges():
        x1, y1, z1 = pos[u]
        x2, y2, z2 = pos[v]
        edge_x.extend([x1, x2, None])
        edge_y.extend([y1, y2, None])
        edge_z.extend([z1, z2, None])
    edge_scatter = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z, mode='lines', line=dict(width=2, color='blue'))

    if detected_graph is not None:
        pos2 = nx.get_node_attributes(detected_graph, 'pos')
        nodes2 = detected_graph.nodes()
        x2, y2, z2 = zip(*[pos2[v] for v in detected_graph.nodes()])
        node_names2 = list(detected_graph.nodes())
        # Create a scatter plot for the nodes
        node_scatter2 = go.Scatter3d(x=x2, y=y2, z=z2, mode='markers', marker=dict(
            size=10, color='green'), text=node_names2)
        


    # #change the color of the nodes of node_scatter that contains 'cross' in name else its red
    
    node_scatter.marker.color = ['red' if 'cross' not in node else 'pink' for node in node_names]


    # Create a subplot with 3D scatter plots for nodes and edges
    fig = sp.make_subplots(rows=1, cols=1, specs=[[{'type': 'scatter'}]])
    fig.add_trace(node_scatter)
    fig.add_trace(edge_scatter)

    if detected_graph is not None:
        fig.add_trace(node_scatter2)


    # Set the axis limits
    fig.update_layout(scene=dict(xaxis=dict(range=[-100, 100], autorange=False),
                                 yaxis=dict(range=[-100, 100],
                                            autorange=False),
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
