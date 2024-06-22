import json
import argparse
import networkx as nx
import pandas as pd
import time
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--weighted', type=bool, required=False, default=False)
parser.add_argument('--k_min', type=int, required=False, default=500)
parser.add_argument('--k_max', type=int, required=False, default=2000)
parser.add_argument('--k_jump', type=int, required=False, default=500)
parser.add_argument('--repeat', type=int, required=False, default=10)

args = parser.parse_args()
weighted: bool = args.weighted
k_min: int = args.k_min
k_max: int = args.k_max
k_jump: int = args.k_jump
repeat: int = args.repeat

print("Running-- weighted:", weighted, ", k_min=", k_min, ", k_max=", k_max, ", k_jump=", k_jump, ", repeat=", repeat)


# load graph
input_path = "data/"
file_graph_clean = input_path + "weighted_graph_clean2.csv"
df = pd.read_csv(file_graph_clean)

G_w = nx.Graph()
for index, row in df.iterrows():
    G_w.add_edge(row['node1'], row['node2'], weight=row["weight"], tag=row["tag"])

l = []
for n in G_w.nodes:
    if type(n) != str:
        l.append(n)
G_w.remove_nodes_from(l)

# run betweenness algo
if weighted:    # weights are reversed !
    max_w = 0
    for u, v in G_w.edges:
        curr_w = G_w.get_edge_data(u, v)["weight"]
        if curr_w > max_w:
            max_w = curr_w

    for u, v in G_w.edges:
        curr_w = G_w.get_edge_data(u, v)["weight"]
        nx.set_edge_attributes(G_w, {(u, v): {"weight": max_w - curr_w + 1}})

out_path = "output/"
for k in tqdm(range(k_min, k_max+1, k_jump)):
    for i in tqdm(range(repeat)):
        start = time.time()
        if weighted:
            between = nx.betweenness_centrality(G_w, backend="parallel", weight="weight", k=k)
        else:
            between = nx.betweenness_centrality(G_w, backend="parallel", k=k)
        end = time.time()

        path = out_path + "betweenness_full_graph_#k=" + str(k) + "_run=" + str(i) + ".json"
        with open(path, "w") as file:
            json.dump(between, file)

        print("finished betweenness! time:" + str(end - start))
