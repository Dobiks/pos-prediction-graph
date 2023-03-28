from tqdm import tqdm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
def rotate_graph(detected, angle):

    angle = 360-angle
    angle_rad = np.radians(angle)

    rotation_matrix = np.array([[np.cos(angle_rad), 0, np.sin(angle_rad)],
                                [0, 1, 0],
                                [-np.sin(angle_rad), 0, np.cos(angle_rad)]])

    cords_matrix = np.array([detected['x'], detected['y'], detected['z']])
    cords_matrix = cords_matrix.T
    rotated_cords = np.dot(cords_matrix, rotation_matrix)
    rotated_cords = np.round(rotated_cords, 2)

    detected['x'] = rotated_cords[:, 0]
    detected['y'] = rotated_cords[:, 1]
    detected['z'] = rotated_cords[:, 2]
    return detected


def get_rotation(static, detected, save_plot=False):
    start = time.time()
    detected = detected.rename(columns={'x': 'x1', 'y': 'y1', 'z': 'z1'})
    merged = pd.merge(static, detected, on='name', how='outer')
    merged = merged[merged['x1'].notna()]

    loss = {}
    for angle in range(0, 360, 1):
        df = merged.copy()
        angle_rad = np.radians(angle)

        rotation_matrix = np.array([[np.cos(angle_rad), 0, np.sin(angle_rad)],
                                    [0, 1, 0],
                                    [-np.sin(angle_rad), 0, np.cos(angle_rad)]])

        cords_matrix = np.array([df['x1'], df['y1'], df['z1']])
        cords_matrix = cords_matrix.T
        rotated_cords = np.dot(cords_matrix, rotation_matrix)
        rotated_cords = np.round(rotated_cords, 2)

        df['x1'] = rotated_cords[:, 0]
        df['y1'] = rotated_cords[:, 1]
        df['z1'] = rotated_cords[:, 2]

        df['distance'] = np.sqrt(
            (df['x'] - df['x1'])**2 + (df['y'] - df['y1'])**2 + (df['z'] - df['z1'])**2)
        df['distance'] = np.round(df['distance'], 2)
        loss[angle] = df['distance'].sum()

    rotation = 360-min(loss, key=loss.get)
    print('Rotation:', rotation)
    print('Rotation find time:', time.time()-start)
    if save_plot:
        plt.plot(loss.keys(), loss.values())
        plt.xlabel('Angle')
        plt.ylabel('Loss')
        plt.savefig('loss.png')

    return rotation

def get_rotation_nn(static, detected, save_plot=False):
        start = time.time()

        loss = {}
        for angle in tqdm(range(0, 360, 1)):
            df = detected.copy()
            angle_rad = np.radians(angle) 

            rotation_matrix = np.array([[np.cos(angle_rad), 0, np.sin(angle_rad)],
                                        [0, 1, 0],
                                        [-np.sin(angle_rad), 0, np.cos(angle_rad)]])

            cords_matrix = np.array([df['x'], df['y'], df['z']])
            cords_matrix = cords_matrix.T
            rotated_cords = np.dot(cords_matrix, rotation_matrix)
            rotated_cords = np.round(rotated_cords, 2)

            df['x'] = rotated_cords[:, 0]
            df['y'] = rotated_cords[:, 1]
            df['z'] = rotated_cords[:, 2]
            distances = []
            for i, row1 in df.iterrows():
                distances_i = []
                for j, row2 in static.iterrows():
                    dist = np.sqrt((row1["x"] - row2["x"])**2 + (row1["y"] - row2["y"])**2 + (row1["z"] - row2["z"])**2)
                    distances_i.append(dist)
                closest = min(distances_i)
                distances.append(closest)
            loss[angle] = sum(distances)


            

        rotation = 360-min(loss, key=loss.get)
        print('Rotation:', rotation)
        print('Rotation find time:', time.time()-start)
        if save_plot:
            plt.plot(loss.keys(), loss.values())
            plt.xlabel('Angle')
            plt.ylabel('Loss')
            plt.savefig('loss.png')

        return rotation



if __name__ == '__main__':
    static = pd.read_csv('static_graph.csv')
    detected = pd.read_csv('randomized_graph.csv')
    static['name'] = static['name'].str.replace(' ', '')
    detected['name'] = detected['name'].str.replace(' ', '')
    rotation = get_rotation_nn(static, detected, save_plot=True)
    print(rotation)