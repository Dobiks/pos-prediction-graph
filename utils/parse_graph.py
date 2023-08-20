import json
from collections import deque

def parse_json_graph(json_data):
    graph = json.loads(json_data)

    queue = deque([(graph["name"], graph["childs"])])
    level_order = []

    while queue:
        node, children = queue.popleft()
        level_order.append(node)

        for child in children:
            queue.append((child["name"], child["childs"]))

    return level_order

json_path = 'data.json'
with open(json_path) as json_file:
    json_data = json.load(json_file)


level_order = parse_json_graph(json_data)
# for node in level_order:
#     print(node)
print(level_order)
