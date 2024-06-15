import os
import pickle
from collections import defaultdict

from tqdm import tqdm

debug = True if os.path.exists("/Users/shir/PycharmProjects") else False
if debug:
    output_dir = "output"
    out_file = ""
else:
    output_dir = "/home/nlp/shirash1/Coreference-Graph/fcoref/output"
    out_file = "1"


with open(os.path.join(output_dir, "chains" + out_file + ".txt"), "r") as f_chains:
    dict_spell = defaultdict(dict)
    for line in tqdm(f_chains.readlines()):
        chain = line[:-1].split('\t')
        lower_chain = [ph.lower() for ph in chain]
        for ind in range(len(chain)):
            if chain[ind] not in dict_spell[lower_chain[ind]]:
                dict_spell[lower_chain[ind]][chain[ind]] = 0
            dict_spell[lower_chain[ind]][chain[ind]] += 1

print(dict_spell)
output_dir = "./output_spell"
os.makedirs(output_dir, exist_ok=True)

with open(os.path.join(output_dir, "dict_spell" + out_file + ".pkl"), "wb") as f_spell:
    pickle.dump(dict_spell, f_spell)
