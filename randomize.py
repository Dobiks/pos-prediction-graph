import math
import pandas as pd
import numpy as np
import random


def pick_elements(df):
    n = random.randint(0, 17)
    nums = random.sample(range(0, 18), n)
    df = df.iloc[nums]
    return df


def randomize_angle(df):
    angle = random.randint(0, 360)
    print("ANGLE:", angle)
    angle_rad = np.radians(angle)

    rotation_matrix = np.array(
        [
            [np.cos(angle_rad), 0, np.sin(angle_rad)],
            [0, 1, 0],
            [-np.sin(angle_rad), 0, np.cos(angle_rad)],
        ]
    )

    cords_matrix = np.array([df["x"], df["y"], df["z"]])
    cords_matrix = cords_matrix.T

    rotated_cords = np.dot(cords_matrix, rotation_matrix)
    rotated_cords = np.round(rotated_cords, 2)
    # print(rotated_cords)

    df["x"] = rotated_cords[:, 0]
    df["y"] = rotated_cords[:, 1]
    df["z"] = rotated_cords[:, 2]
    return df, angle


def randomize_postion(df):
    MAX_DISTANCE = 5
    for row in df.itertuples():
        current_pos = (row.x, row.y, row.z)
        direction = [random.uniform(-1, 1) for i in range(3)]
        length = math.sqrt(sum([x**2 for x in direction]))
        direction = tuple([x / length for x in direction])

        distance = random.uniform(0, MAX_DISTANCE)

        new_pos = tuple([current_pos[i] + direction[i] * distance for i in range(3)])
        new_pos = np.round(new_pos, 2)

        df.at[row.Index, "x"] = new_pos[0]
        df.at[row.Index, "y"] = new_pos[1]
        df.at[row.Index, "z"] = new_pos[2]

    return df


def rand_all(do_angle=True, do_pos=True, do_pick=True):
    df = pd.read_csv("detection_graph.csv")

    root_df = df.iloc[0]
    df = df.iloc[1:]
    df = df.reset_index(drop=True)

    if do_pick:
        df = pick_elements(df)
    if do_pos:
        df = randomize_postion(df)
    if do_angle:
        df, angle = randomize_angle(df)
    else:
        angle = 0

    df = pd.concat([root_df.to_frame().T, df])
    df.to_csv("randomized_graph.csv", index=False)
    return angle


if __name__ == "__main__":
    rand_all(do_angle=True, do_pos=False, do_pick=False)
