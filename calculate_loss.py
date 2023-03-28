import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

static = pd.read_csv('corrected_static.csv')
detected = pd.read_csv('rotated_graph.csv')
detected = detected.rename(columns={'x': 'x1', 'y': 'y1', 'z': 'z1'})
merged = pd.merge(static, detected, on='name', how='outer')
merged = merged[merged['x1'].notna()]

#calculate distance between static and detected
# df['distance'] = np.sqrt((df['x'] - df['x1'])**2 + (df['y'] - df['y1'])**2 + (df['z'] - df['z1'])**2)

loss = {}
prev = 0
positions = []
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


    #distance between static and detected
    df['x1'] = rotated_cords[:,0]
    df['y1'] = rotated_cords[:,1]
    df['z1'] = rotated_cords[:,2]

    df['distance'] = np.sqrt((df['x'] - df['x1'])**2 + (df['y'] - df['y1'])**2 + (df['z'] - df['z1'])**2)

    #round to 2 decimals
    df['distance'] = np.round(df['distance'], 2)

    loss[angle] = df['distance'].sum()
    # print(df)


#print min value
print('min', 360-min(loss, key=loss.get))



#plot
plt.plot(loss.keys(), loss.values())
plt.xlabel('Angle')
plt.ylabel('Loss')
plt.show()
#save
plt.savefig('loss.png')
