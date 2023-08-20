import numpy as np
import pandas as pd
from utils.consts import level_order
import math
import networkx as nx
from utils.graph_utils import plot_graph
import numpy as np
import pandas as pd
import random
import copy

def calculate_softmax(df):
    df = copy.deepcopy(df)
    df = df[df["name"] != "root"]
    df = df.reset_index(drop=True)
    for i in range(len(df)):
        df[df["name"][i]] = 0 
    #drop row with name root

    names_list = df["name"].tolist()
    # for row
    for i in range(len(df)):
        name = df["name"][i]
        current_softmax = random.uniform(0.5, 0.99)
        df.at[i, name] = current_softmax


        random_names = random.sample(names_list, random.randint(1, len(names_list)))
        if name in random_names:
            random_names.remove(name)
        other_values = [random.randint(1, 100) for i in range(len(random_names))]
        other_values = [
            (float(i) / np.sum(other_values)) * (1 - current_softmax)
            for i in other_values
        ]
        for j in range(len(random_names)):
            df.at[i, random_names[j]] = other_values[j]


    return df


def randomize_nodes(df):
    max_distance = 3
    #reset index
    df = df.reset_index(drop=True)
    for i in range(len(df)):
        current_pos = (df["x"][i], df["y"][i], df["z"][i])
        direction = [random.uniform(-1, 1) for i in range(3)]
        length = math.sqrt(sum([x**2 for x in direction]))
        direction = tuple([x / length for x in direction])

        distance = random.uniform(0, max_distance)

        new_pos = tuple([current_pos[i] + direction[i] * distance for i in range(3)])
        new_pos = np.round(new_pos, 2)
        df.loc[i, ["x", "y", "z"]] = new_pos
    return df


def add_softmax(df, n=10):
    new_frames = []  # List to hold the DataFrames

    for _ in range(n):
        tmp_df = randomize_nodes(df)
        tmp_df = calculate_softmax(tmp_df)
        new_frames.append(tmp_df)

    # Concatenate all DataFrames at once
    df = pd.concat(new_frames, ignore_index=True)

    df = df.drop(columns=["name"])
    #move index to first column "id"
    df.insert(0, "id", df.index)

    return df



def calc_child_pos(parent_cords: tuple, max_distance: float):
    direction = (
        random.uniform(-1, 1),
        random.uniform(-1, -0.6),
        random.uniform(-1, 1),
    )
    length = math.sqrt(sum([x**2 for x in direction]))
    direction = tuple([x / length for x in direction])

    distance = random.uniform(max_distance * 0.8, max_distance)

    new_pos = tuple([parent_cords[i] + direction[i] * distance for i in range(3)])
    new_pos = np.round(new_pos, 2)
    return new_pos


def generate_graph():
    STATIC_PATH = "/home/mikolaj/git/pos-prediction-graph/csv_files/static_with_t.csv"
    static_df = pd.read_csv(STATIC_PATH)
    skip_names = [
        "root_cross_right",
        "root_cross_left",
        "root_cross_right2",
    ]

    

    for node_name in level_order:
        if node_name in skip_names:
            continue
        node_df = static_df[static_df["name"] == node_name]
        parent_name = node_df["parent"].iloc[0]
        parent_df = static_df[static_df["name"] == parent_name]
        print(static_df)
        parent_cords = (
            parent_df["x"].iloc[0],
            parent_df["y"].iloc[0],
            parent_df["z"].iloc[0],
        )
        new_pos = calc_child_pos(parent_cords, node_df["distance_to_parent"].iloc[0])
        static_df.loc[static_df["name"] == node_name, ["x", "y", "z"]] = new_pos

    G1 = nx.Graph()
    for i in range(len(static_df)):
        G1.add_node(
            static_df["name"][i],
            pos=(static_df["x"][i], static_df["z"][i], static_df["y"][i]),
        )
    for i in range(len(static_df)):
        if static_df["parent"][i] != 0 and static_df["parent"][i] != "0":
            G1.add_edge(static_df["name"][i], static_df["parent"][i])

    plot_graph(static_graph=G1, detected_graph=None, name="random", save=True)
    static_df.to_csv(
        "/home/mikolaj/git/pos-prediction-graph/data_generation/mega_static.csv",
        index=False,
    )
    static_df = static_df[static_df["number"] >= 0]


    return static_df


def main():
    df = generate_graph()
    df = add_softmax(df)
    df.to_csv(
        "/home/mikolaj/git/pos-prediction-graph/data_generation/mega_randomized.csv",
        index=False,
    )




if __name__ == "__main__":
    main()
