from flask import Flask, send_file, request, render_template
import networkx as nx
import matplotlib.pyplot as plt
import io
from PIL import Image
import json
import os
import pickle

app = Flask(__name__)


def get_data(root, layers):
    os.system(f"python3 connection_tree_v2.py {root} {layers}")
    f = open(f".{root}_{layers}".replace("/", "o"), "rb")
    data = pickle.loads(f.read())
    f.close()

    return data


def add_nodes_edges(graph, node, parent=None):
    """
    Recursively add nodes and edges to the graph.
    """
    if parent:
        graph.add_edge(parent, node['name'])

    if 'children' in node:
        for child in node['children']:
            add_nodes_edges(graph, child, node['name'])

def plot_tree(data, output_file='tree.png'):
    """
    Plot a tree graph from the data and save it as an image.
    """
    G = nx.DiGraph()
    add_nodes_edges(G, data)

    pos = nx.spring_layout(G, seed=42, k=0.5)  # Position nodes using spring layout
    plt.figure(figsize=(14, 10))
    nx.draw(G, pos, with_labels=True, arrows=True, node_size=2000, node_color='lightblue', font_size=6, font_weight='bold', edge_color='gray')
    plt.title('Tree Graph')
    plt.savefig(output_file)



@app.route('/')
def index():
    return render_template('tree.html')


@app.route('/generate_tree')
def generate_tree():
    root = request.headers.get('root')
    layers = int(request.headers.get('layers'))
    
    data = get_data(root, layers)
    data = data[root]
    plot_tree(data)

    return send_file("tree.png", mimetype='image/png')

if __name__ == '__main__':
    app.run()
