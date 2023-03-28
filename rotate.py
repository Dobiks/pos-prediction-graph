import pandas as pd
import numpy as np
import random

df = pd.read_csv('detected_graph.csv')

#random from 0 to 360
angle = random.randint(0,360)
print(angle)
angle_rad = np.radians(angle)

#rotation matrix for y axis
rotation_matrix = np.array([[np.cos(angle_rad), 0, np.sin(angle_rad)],
                            [0, 1, 0],
                            [-np.sin(angle_rad), 0, np.cos(angle_rad)]])

cords_matrix = np.array([df['x'], df['y'], df['z']])
cords_matrix = cords_matrix.T

#rotate
rotated_cords = np.dot(cords_matrix, rotation_matrix)
rotated_cords = np.round(rotated_cords, 2)
print(rotated_cords)
#round to 2 decimals
#save to df
df['x'] = rotated_cords[:,0]
df['y'] = rotated_cords[:,1]
df['z'] = rotated_cords[:,2]

df.to_csv('rotated_graph.csv', index=False)

