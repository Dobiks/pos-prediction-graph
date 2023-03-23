import csv
import math

# Define the rotation function
def rotate_y(point, angle):
    # Convert angle to radians
    angle = math.radians(angle)
    # Compute the new x and z coordinates
    x = point[0] * math.cos(angle) + point[2] * math.sin(angle)
    z = -point[0] * math.sin(angle) + point[2] * math.cos(angle)
    # Return the rotated point
    return (x, point[1], z)

# Load the graph from a CSV file
graph = {}
with open('corrected_static.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row
    for row in reader:
        name, number, x, y, z, parent = row
        graph[name] = (float(x), float(y), float(z), parent)

# Rotate each node around the root in the y-axis by 90 degrees
root_position = graph['root'][:3]
for name in graph:
    if name == 'root':
        continue
    point = graph[name][:3]
    point = tuple(point[i] - root_position[i] for i in range(3))  # Translate to origin
    point = rotate_y(point, 90)  # Rotate around y-axis
    point = tuple(point[i] + root_position[i] for i in range(3))  # Translate back to original position
    graph[name] = point + (graph[name][3],)

# Write the updated graph to a new CSV file
with open('rotated_graph.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'number', 'x', 'y', 'z', 'parent'])
    for name in graph:
        point = graph[name]
        writer.writerow([name, '', point[0], point[1], point[2], point[3]])
