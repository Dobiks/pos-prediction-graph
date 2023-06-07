import csv
import json

def create_node(name):
    return {"name": name, "childs": []}

def build_tree(nodes, parent):
    tree = []
    for node in nodes:
        if node["parent"] == parent:
            child = create_node(node["name"])
            child["childs"] = build_tree(nodes, node["name"])
            tree.append(child)
    return tree

def convert_csv_to_json(csv_file):
    nodes = []
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            nodes.append({"name": row["name"], "parent": row["parent"]})

    root = create_node("root")
    root["childs"] = build_tree(nodes, "root")

    return json.dumps(root, indent=4)

csv_file = "randomized_graph.csv"
json_data = convert_csv_to_json(csv_file)
print(json_data)
#save
with open('data.json', 'w') as outfile:
    json.dump(json_data, outfile)

