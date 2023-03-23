import pandas as pd
import numpy as np

# Load data
static = pd.read_csv('corrected_static.csv')
detected = pd.read_csv('detected_graph.csv')

# Create dictionaries to map node names to indices
static_names = static['name'].to_dict()
detected_names = detected['name'].to_dict()

#revert dict static names
static_names_r = {v: k for k, v in static_names.items()}
detected_names_r = {v: k for k, v in detected_names.items()}

# Create adjacency matrices
num_nodes = len(static_names)
static_adj = np.zeros((num_nodes, num_nodes))
detected_adj = np.zeros((num_nodes, num_nodes))

for _, row in static.iterrows():
    parent_name = row['parent']
    if parent_name == '0':
        parent_idx = None
    else:
        parent_idx = static_names_r[parent_name]
    node_name = row['name']
    if node_name == 'root':
        node_idx = 0
    else:
        node_idx = static_names_r[node_name]
    if parent_idx is not None:
        static_adj[parent_idx, node_idx] = 1
        static_adj[node_idx, parent_idx] = 1

for _, row in detected.iterrows():
    parent_name = row['parent']
    if parent_name == '0':
        parent_idx = None
    else:
        parent_idx = detected_names_r[parent_name]
    node_idx = detected_names_r[row['name']]
    if parent_idx is not None:
        detected_adj[parent_idx, node_idx] = 1
        detected_adj[node_idx, parent_idx] = 1

# Find rotation matrix using SVD
U, _, Vt = np.linalg.svd(static_adj @ detected_adj.T)
R = Vt.T @ U.T


# Apply rotation to detected node positions
detected_positions = detected[['x', 'y', 'z']].to_numpy()
detected_positions_rotated = (R @ detected_positions.T).T

# Calculate translation vector
static_root = static.loc[static['name'] == 'root', ['x', 'y', 'z']].to_numpy()[0]
detected_root = detected.loc[detected['name'] == 'root', ['x', 'y', 'z']].to_numpy()[0]
t = static_root - (R @ detected_root.T).T

# Apply translation to detected node positions
detected_positions_corrected = detected_positions_rotated + t

# Update detected graph with corrected positions
detected_corrected = detected.copy()
detected_corrected[['x', 'y', 'z']] = detected_positions_corrected

# Print corrected positions
print(detected_corrected[['name', 'x', 'y', 'z']])
