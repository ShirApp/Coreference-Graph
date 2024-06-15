import os
import pickle
from collections import defaultdict
from tqdm import tqdm

debug = True if os.path.exists("/Users/shir/PycharmProjects") else False
if debug:
    output_dir = "output_spell"
    out_file = ""
    nodes_dir = "data/all_nodes.pkl"
else:
    output_dir = "/home/nlp/shirash1/Coreference-Graph/output_spell"
    out_file = "__1"
    nodes_dir = "/home/nlp/shirash1/Coreference-Graph/fcoref/data/all_nodes.pkl"


with open(os.path.join(output_dir, "dict_spell" + out_file + ".pkl"), "rb") as f_spell:
    dict_spell = pickle.load(f_spell)
    print("len spell dict:", len(dict_spell))

c_in = 0
c_out = 0
temp_dict = defaultdict(dict)
with open(nodes_dir, 'rb') as f:
    all_nodes = list(pickle.load(f))
    for node in tqdm(all_nodes):
        if node in dict_spell:
            temp_dict[node] = dict_spell[node]
            c_in += 1
        else:
            c_out += 1
            for k in dict_spell.keys():
                if len(node.split()) == 1:
                    if node in k.split():
                        print(node, "|", k)
                        break
                else:
                    if node in k:
                        print(node, "|", k)
                        break

print("in", c_in, "out", c_out)
