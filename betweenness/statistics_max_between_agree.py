import os
import pickle
from collections import defaultdict

THRESHOLD = 2/3
NUM_OF_RUNS = 52
debug = True if os.path.exists("/Users/shir/PycharmProjects") else False
if debug:
    path = "analysis/result.pkl"
else:
    path = "/home/nlp/shirash1/Coreference-Graph/betweenness/analysis/result.pkl"
with open(path, "rb") as f:
    d = pickle.load(f)
    all_max = defaultdict(int)
    min_max = 1
    for k, v in d.items():
        vals = v.values()
        max_val = max(vals)
        all_max[max_val] += 1
        min_max = min(min_max, max_val/sum(vals)) if max_val > 0 else min_max

print(all_max)
print(min_max)
print(sum([v for k, v in all_max.items() if int(k) <= THRESHOLD*NUM_OF_RUNS])/sum([v for k, v in all_max.items()]))
