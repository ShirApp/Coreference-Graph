import json
import os
import pickle
from collections import defaultdict
import pandas as pd
from tqdm import tqdm

file_graph_clean = "data/weighted_graph_clean2.csv"

if not os.path.exists(file_graph_clean):
    print(os.listdir("data"))

else:
    df = pd.read_csv(file_graph_clean)
    pairs_dict = []

    pairs = defaultdict(tuple)

    for index, row in df.iterrows():
        ph1 = row['node1']
        ph2 = row['node2']
        pairs[(ph1, ph2)] = {"1": 0, "2": 0, "0": 0}
        # if len(pairs) > 10000:
        #     break

    between_path = "output/"
    for between_file in tqdm(os.listdir(between_path)):
        try:
            with open(between_path + between_file, "r") as f:
                data = json.load(f)
                for ph1, ph2 in pairs.keys():
                    if ph1 in data and ph2 in data:
                        if data[ph1] > data[ph2]:
                            pairs[(ph1, ph2)]["1"] += 1
                        elif data[ph1] < data[ph2]:
                            pairs[(ph1, ph2)]["2"] += 1
                        else:
                            pairs[(ph1, ph2)]["0"] += 1
        except:
            print("error file ", between_file)

    output_dir = "analysis"
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "result.pkl"), "wb") as f:
        pickle.dump(pairs, f)
