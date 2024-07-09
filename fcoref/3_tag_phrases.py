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
    out_file = "__1.2"
    nodes_dir = "/home/nlp/shirash1/Coreference-Graph/fcoref/data/all_nodes.pkl"


with open(os.path.join(output_dir, "dict_spell" + out_file + ".pkl"), "rb") as f_spell:
    dict_spell = pickle.load(f_spell)
    print("len spell dict:", len(dict_spell))

dict_spell_words = defaultdict(dict)
for phrase, spell_dict in dict_spell.items():
    words = phrase.split()
    if len(words) > 1:
        for word in words:
            curr_dict = dict()
            for k, v in spell_dict.items():
                curr_k = [i for i in k.split() if i.lower() == word][0]
                curr_dict[curr_k] = v
                dict_spell_words[word.lower()].update(curr_dict)

c_in = 0
c_out = 0
temp_dict = defaultdict(dict)
with open(nodes_dir, 'rb') as f:
    all_nodes = list(pickle.load(f))
    for node in tqdm(all_nodes):
        if node in dict_spell:
            temp_dict[node] = dict_spell[node]
            c_in += 1
        elif node in dict_spell_words:
            temp_dict[node] = dict_spell_words[node]
            c_in += 1
        # else:
        #     c_out += 1
        #     if len(node.split()) == 1:
        #         continue
        #     else:
        #         first_word = node.split()[0]
        #         if first_word in dict_spell_words:
        #             temp_dict[node] = dict_spell_words[first_word]

print("in", c_in, "out", c_out)

tags_dict = defaultdict()

for k, v in temp_dict.items():
    strings = list(v.keys())
    done = False
    for s in strings:
        if s.isupper() and s.isalpha():
            tags_dict[k] = "abb"
            done = True
            break
        if s[0].islower():
            tags_dict[k] = "noun"
            done = True
            break
    if not done:
        tags_dict[k] = "name"

output_dir = "./output_tags"
os.makedirs(output_dir, exist_ok=True)

with open(os.path.join(output_dir, "phrases_tags" + out_file + ".pkl"), "wb") as f_spell:
    pickle.dump(tags_dict, f_spell)
