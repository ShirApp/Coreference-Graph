import pickle

file_path = "/home/nlp/shirash1/Coreference-Graph/betweenness/analysis/result.pkl"
with open(file_path, "rb") as f:
    d = pickle.load(f)
    final_pairs = dict()
    unknown = dict()
    total_max = 52
    x = 0
    for k, v in d.items():
        vals = v.values()
        max_val = max(vals)
        if max_val > 0 and max_val < total_max:
            total_max = min(max_val, total_max)
            x = vals
        #     print(max_val, d)

print(total_max, vals)
# print(total_max/52)
