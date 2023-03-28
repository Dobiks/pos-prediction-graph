import random
import math

#random int values
max_dist = 0
min_dist = 100
for i in range(10000):
    x = random.randint(0, 50)
    y = random.randint(0, 50)
    z = random.randint(0, 50)

    prev_position = (x, y, z)

    direction = [random.uniform(-1, 1) for i in range(3)]
    length = math.sqrt(sum([x**2 for x in direction]))
    direction = tuple([x/length for x in direction])

    distance = random.uniform(0, 5)

    new_position = tuple([prev_position[i] + direction[i]*distance for i in range(3)])
