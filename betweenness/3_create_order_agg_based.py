import os
import pickle

THRESHOLD = 2/3
debug = True if os.path.exists("/Users/shir/PycharmProjects") else False
if debug:
    path = "analysis/result.pkl"
else:
    path = "/home/nlp/shirash1/Coreference-Graph/betweenness/analysis/result.pkl"
with open(path, "rb") as f:
    d = pickle.load(f)
    final_pairs = dict()
    unknown = dict()
    for k, v in d.items():
        vals = v.values()
        max_val = max(vals)
        total_val = sum(vals)
        if total_val == 0 or max_val/total_val < THRESHOLD:
            unknown[k] = v
        else:
            max_ind = list(v.values()).index(max_val)
            if max_ind == 0:
                final_pairs[k] = ("H", max_ind, total_val)
            elif max_ind == 1:
                final_pairs[(k[1], k[0])] = ("H", max_ind, total_val)
            else:   # == '2'
                final_pairs[k] = ("I", max_ind, total_val)

    output_dir = "./decision"
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "directed_pairs.pkl"), "wb") as f:
        pickle.dump(final_pairs, f)
    with open(os.path.join(output_dir, "unknown_pairs.pkl"), "wb") as f:
        pickle.dump(unknown, f)
