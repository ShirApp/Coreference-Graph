import os
import pickle

debug = True if os.path.exists("/Users/shir/PycharmProjects") else False
if debug:
    output_dir = "output_spell"
    out_file = ""
else:
    output_dir = "/home/nlp/shirash1/Coreference-Graph/output_spell"
    out_file = "__1"


with open(os.path.join(output_dir, "dict_spell" + out_file + ".pkl"), "rb") as f_spell:
    dict_spell = pickle.load(f_spell)
    print(len(dict_spell))

c_in = 0
c_out = 0
with open("data/all_nodes.pkl", 'rb') as f:
    all_nodes = list(pickle.load(f))
    for node in all_nodes:
        if node in dict_spell:
            c_in += 1
        else:
            c_out += 1

print("in", c_in, "out", c_out)
