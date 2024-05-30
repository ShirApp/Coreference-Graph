import csv
import gzip
from collections import *

children = defaultdict(list)
parents = defaultdict(list)
equiv_pairs = defaultdict(set)
edge_types = {}
split_nodes = defaultdict(set)

path = "/app/data/full_graph_tagged5_2023-11-29_18:49.csv"
fh = open(path, "r")
next(fh)
for _, n1, n2, w, kind in csv.reader(fh):
    if float(w) < 4: continue
    if kind[0] == "h":
        if kind[-1] in "56": continue
        children[n1].append(n2)
        parents[n2].append(n1)
        edge_types[(n1,n2)] = f"{kind[0]}{kind[-1]}"
        edge_types[(n2,n1)] = f"{kind[0]}{kind[-1]}"
    if kind[0] == "i":
        equiv_pairs[n1].add(n2)
        equiv_pairs[n2].add(n1)
    n1_base = n1.split(" [[[")[0]
    n2_base = n2.split(" [[[")[0]
    split_nodes[n1_base].add(n1)
    split_nodes[n2_base].add(n2)

print(len(equiv_pairs))

def equiv_set(s):
    cur = {s}
    prev_len = len(cur)
    while True:
        for x in list(cur):
            cur.update(equiv_pairs.get(x,[]))
        if len(cur) == prev_len: break
        prev_len = len(cur)
    return list(cur)

def traverse(x, seen=None, dir="c"):
    D = children if dir == "c" else parents
    max_depth_of_child = defaultdict(int)
    senses = split_nodes.get(x, [x])
    k = [(s, "R", 0) for s in senses]
    while k:
        s, et, depth = k.pop()
        max_depth_of_child[s] = depth
        k.extend([(c, edge_types[(s,c)], depth+1) for c in D.get(s,[])])
    k = [(s, "R", 0) for s in senses]
    result = []
    while k:
        s, et, depth = k.pop()
        if depth < max_depth_of_child[s]: continue # we will get to this one later.
        equivs = equiv_set(s)
        equiv_string = "; ".join([e for e in equivs if e != x])
        # print(f"{'  ' * depth}{et}: {s} [{equiv_string}]")
        result.append((depth, et, s, equiv_string))
        k.extend([(c, edge_types[(s,c)], depth+1) for c in D.get(s,[])])
    # print(result)
    return result