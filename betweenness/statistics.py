import os
import pickle

THRESHOLD = 2/3
with open("analysis/result.pkl", "rb") as f:
    d = pickle.load(f)
    final_pairs = dict()
    unknown = dict()
    for k, v in d.items():
        vals = v.values()
        max_val = max(vals)
        total_val = sum(vals)/len(vals)
        if max_val/total_val > THRESHOLD:
            max_ind = list(v.values()).index(max_val)
            if max_ind == 0:
                final_pairs[k] = "H"
            elif max_ind == 1:
                final_pairs[(k[1], k[0])] = "H"
            else:   # == '2'
                final_pairs[k] = "I"
        else:
            unknown[k] = v
    # print()

    output_dir = "./decision"
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "directed_pairs.pkl"), "wb") as f:
        pickle.dump(final_pairs, f)
    with open(os.path.join(output_dir, "unknown_pairs.pkl"), "wb") as f:
        pickle.dump(unknown, f)
