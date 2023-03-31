import numpy as np
from scipy.optimize import minimize

# Define the two points
P1 = np.array([3, 4, 5])
P2 = np.array([7, 4, 9])

# Define the distance function between the two points
def distance_function(theta):
    # Construct the rotation matrix
    theta = theta[0]
    R = np.array([[np.cos(theta), 0, np.sin(theta)],
                  [0, 1, 0],
                  [-np.sin(theta), 0, np.cos(theta)]])
    # Rotate P2 by the angle theta
    rotated_P2 = np.dot(R, P2)
    # Calculate the distance between P1 and rotated_P2
    distance = np.linalg.norm(P1 - rotated_P2)
    return distance

# Choose an initial guess for the angle of rotation
theta_initial_guess = 0

# Use the minimize function to find the optimal angle of rotation
result = minimize(distance_function, theta_initial_guess)

# Print the optimal angle of rotation and the corresponding distance
#in degrees
angle = np.degrees(result.x[0])
print(f"Optimal angle of rotation: {angle}")
print("Distance between the two points at optimal rotation: {:.3f}".format(result.fun))

