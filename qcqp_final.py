import networkx as nx
from utils.graph_utils import plot_graph
import numpy as np
import pandas as pd
from gurobipy import GRB, Model
from utils.consts import COMPONENTS, LEVEL_ORDER

def validate_detections():
    static = pd.read_csv(
        "/home/mikolaj/git/pos-prediction-graph/data_generation/mega_static.csv"
    )
    detected = pd.read_csv(
        "/home/mikolaj/git/pos-prediction-graph/data_generation/mega_randomized.csv"
    )

    quadratic_model = Model("quadratic")
    variables = {}
    for name in LEVEL_ORDER:
        variables[f"{name}_x"] = quadratic_model.addVar(
            vtype=GRB.CONTINUOUS, lb=-250, ub=250, name=f"{name}_x"
        )
        variables[f"{name}_y"] = quadratic_model.addVar(
            vtype=GRB.CONTINUOUS, lb=-250, ub=250, name=f"{name}_y"
        )
        variables[f"{name}_z"] = quadratic_model.addVar(
            vtype=GRB.CONTINUOUS, lb=-250, ub=250, name=f"{name}_z"
        )

    obj_fn = 0
    for row in detected.iterrows():
        detected_x = row[1]["x"]
        detected_y = row[1]["y"]
        detected_z = row[1]["z"]
        for component in COMPONENTS:
            confidence = row[1][component]
            term = confidence * (
                (variables[f"{component}_x"] - detected_x) ** 2
                + (variables[f"{component}_y"] - detected_y) ** 2
                + (variables[f"{component}_z"] - detected_z) ** 2
            )
            obj_fn += term


    for name in LEVEL_ORDER:
        node_info = static[static["name"] == name]
        parent = node_info["parent"].values[0]
        distance_to_parent = node_info["distance_to_parent"].values[0]
        if name == "root_cross_left":
            quadratic_model.addQConstr(variables[f"{name}_x"] == -13)
            quadratic_model.addQConstr(variables[f"{name}_y"] == -20)
            quadratic_model.addQConstr(variables[f"{name}_z"] == 0)

        elif name == "root_cross_right":
            quadratic_model.addQConstr(variables[f"{name}_x"] == 10)
            quadratic_model.addQConstr(variables[f"{name}_y"] == -1)
            quadratic_model.addQConstr(variables[f"{name}_z"] == 0)
        else:
            quadratic_model.addQConstr(
                (
                    (variables[f"{name}_x"] - variables[f"{parent}_x"]) ** 2
                    + (variables[f"{name}_y"] - variables[f"{parent}_y"]) ** 2
                    + (variables[f"{name}_z"] - variables[f"{parent}_z"]) ** 2
                )
                <= distance_to_parent**2
            )


    quadratic_model.setObjective(obj_fn, GRB.MINIMIZE)

    quadratic_model.optimize()

    G1 = nx.Graph()
    for i in range(len(detected)):
        G1.add_node(
            str(detected["id"][i]),
            pos=(detected["x"][i], detected["z"][i], detected["y"][i]),
        )


    G2 = nx.Graph()
    for name in LEVEL_ORDER:
        if variables[f"{name}_x"].x != 250 and variables[f"{name}_x"].x != -250:
            G2.add_node(
                name,
                pos=(
                    variables[f"{name}_x"].x,
                    variables[f"{name}_z"].x,
                    variables[f"{name}_y"].x,
                ),
            )


    plot_graph(static_graph=G1, detected_graph=G2, name="qcqp2", save=True)


    def calculate_distance(point1, point2):
        """Calculates the Euclidean distance between two 3D points"""
        x1, y1, z1 = point1
        x2, y2, z2 = point2
        return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)


    def find_closest_node(G1, G2):
        """Finds the closest G1 node for each node in G2"""
        closest_nodes = {}
        for g2_node in G2.nodes(data=True):
            g2_pos = g2_node[1]["pos"]
            min_dist = float("inf")
            min_node = None
            for g1_node in G1.nodes(data=True):
                g1_pos = g1_node[1]["pos"]
                dist = calculate_distance(g1_pos, g2_pos)
                if dist < min_dist:
                    min_dist = dist
                    min_node = g1_node[0]
            closest_nodes[g2_node[0]] = min_node
        return closest_nodes


    # Call the function
    closest_nodes = find_closest_node(G2, G1)

    # If you want to see the result in a DataFrame
    df_closest_nodes = pd.DataFrame(
        closest_nodes.items(), columns=["G1_Node", "Closest_G2_Node"]
    )
    df_closest_nodes = df_closest_nodes.set_index("G1_Node")

    # sort by column "closest_G2_node"
    df_closest_nodes.sort_values(by=["Closest_G2_Node"], inplace=True)
    detected['valid'] = detected['id'].astype(str).map(df_closest_nodes['Closest_G2_Node'])



    final_model = Model("quadratic")

    f_vars = {}
    for name in LEVEL_ORDER:
        f_vars[f"{name}_x"] = final_model.addVar(
            vtype=GRB.CONTINUOUS, lb=-250, ub=250, name=f"{name}_x"
        )
        f_vars[f"{name}_y"] = final_model.addVar(
            vtype=GRB.CONTINUOUS, lb=-250, ub=250, name=f"{name}_y"
        )
        f_vars[f"{name}_z"] = final_model.addVar(
            vtype=GRB.CONTINUOUS, lb=-250, ub=250, name=f"{name}_z"
        )



    obj_fn = 0
    for row in detected.iterrows():
        detected_x = row[1]["x"]
        detected_y = row[1]["y"]
        detected_z = row[1]["z"]
        component = row[1]["valid"]
        term = (
            (f_vars[f"{component}_x"] - detected_x) ** 2
            + (f_vars[f"{component}_y"] - detected_y) ** 2
            + (f_vars[f"{component}_z"] - detected_z) ** 2
        )
        obj_fn += term

    for name in LEVEL_ORDER:
        node_info = static[static["name"] == name]
        parent = node_info["parent"].values[0]
        distance_to_parent = node_info["distance_to_parent"].values[0]
        if name == "root_cross_left":
            final_model.addQConstr(f_vars[f"{name}_x"] == -13)
            final_model.addQConstr(f_vars[f"{name}_y"] == -20)
            final_model.addQConstr(f_vars[f"{name}_z"] == 0)

        elif name == "root_cross_right":
            final_model.addQConstr(f_vars[f"{name}_x"] == 10)
            final_model.addQConstr(f_vars[f"{name}_y"] == -1)
            final_model.addQConstr(f_vars[f"{name}_z"] == 0)
        else:
            final_model.addQConstr(
                (
                    (f_vars[f"{name}_x"] - f_vars[f"{parent}_x"]) ** 2
                    + (f_vars[f"{name}_y"] - f_vars[f"{parent}_y"]) ** 2
                    + (f_vars[f"{name}_z"] - f_vars[f"{parent}_z"]) ** 2
                )
                <= distance_to_parent**2
            )

    final_model.setObjective(obj_fn, GRB.MINIMIZE)
    final_model.optimize()

    G1 = nx.Graph()
    for i in range(len(static)):
        G1.add_node(static["name"][i], pos=(static["x"][i], static["z"][i], static["y"][i]))
    for i in range(len(static)):
        if static["parent"][i] != 0 and static["parent"][i] != "0":
            G1.add_edge(static["name"][i], static["parent"][i])


    G2 = nx.Graph()
    for name in LEVEL_ORDER:
        # if x and y and z are  different than 250 or -250
        if f_vars[f"{name}_x"].x != 250 and f_vars[f"{name}_x"].x != -250:
            # print(name, variables[f"{name}_x"].x, variables[f"{name}_y"].x, variables[f"{name}_z"].x)
            G2.add_node(
                name,
                pos=(
                    f_vars[f"{name}_x"].x,
                    f_vars[f"{name}_z"].x,
                    f_vars[f"{name}_y"].x,
                ),
            )



    plot_graph(static_graph=G1, detected_graph=G2, name="qcqp3", save=True)

    #save all g2 nodes to csv with header
    #name,x,y,z
    with open('/home/mikolaj/git/pos-prediction-graph/data_generation/qcqp.csv', 'w') as f:
        f.write('name,x,y,z\n')
        f.write('root,0.0,0.0,0.0\n')
        #round position to 2 decimal places
        for name in LEVEL_ORDER:
            f.write(f'{name},{round(f_vars[f"{name}_x"].x, 2)},{round(f_vars[f"{name}_y"].x, 2)},{round(f_vars[f"{name}_z"].x, 2)}\n')     


    G1 = nx.Graph()
    for i in range(len(static)):
        G1.add_node(static["name"][i], pos=(static["x"][i], static["z"][i], static["y"][i]))
    for i in range(len(static)):
        if static["parent"][i] != 0 and static["parent"][i] != "0":
            G1.add_edge(static["name"][i], static["parent"][i])

    G2 = nx.Graph()
    for i in range(len(detected)):
        G2.add_node(
            str(detected["id"][i]), pos=(detected["x"][i], detected["z"][i], detected["y"][i])
        )

    plot_graph(static_graph=G1, detected_graph=G2, name="qcqp1", save=True)

if __name__ == "__main__":
    validate_detections()