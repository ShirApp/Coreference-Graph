import argparse
import json
import os
from fastcoref import FCoref
from datasets import load_dataset, DownloadConfig
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--device', type=int, required=True,)
parser.add_argument('--out_file', type=str, required=True)

args = parser.parse_args()
device: int = args.device
out_file: str = args.out_file

print("Running-- device:", device, ", out_file=", out_file,)

debug = True if os.path.exists("/Users/shir/PycharmProjects") else False
if debug:
    dataset = load_dataset("datajuicer/the-pile-pubmed-abstracts-refined-by-data-juicer")
    model = FCoref()
    abstracts_text = dataset['train']['text']
else:
    data_files = "https://huggingface.co/datasets/casinca/PUBMED_title_abstracts_2019_baseline/resolve/main/PUBMED_title_abstracts_2019_baseline.jsonl.zst"
    dataset = load_dataset(
        "json",
        data_files=data_files,
        split="train",
        download_config=DownloadConfig(delete_extracted=True),
    )
    device_num = 'cuda:' + str(device)
    model = FCoref(device=device_num)
    abstracts_text = dataset['text']

batch_size = 1024

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Open the output files
with open(os.path.join(output_dir, "chains__" + out_file + ".txt"), "w") as f_chains, \
        open(os.path.join(output_dir, "indices_chains__" + out_file + ".json"), "w") as f_indices:

    for i in tqdm(range(0, len(abstracts_text), batch_size)):

        batch = abstracts_text[i:i + batch_size]

        preds = model.predict(
            texts=batch, max_tokens_in_batch=10000
        )

        for pred in preds:
            chains = pred.get_clusters()
            indices = pred.get_clusters(as_strings=False)
            for chain, index in zip(chains, indices):
                f_chains.write('\t'.join(chain) + '\n')
                f_indices.write(json.dumps(index) + '\n')
