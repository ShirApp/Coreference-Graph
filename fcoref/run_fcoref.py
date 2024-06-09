import os
from fastcoref import FCoref
from datasets import load_dataset, DownloadConfig

debug = True if os.path.exists("/Users/shir/PycharmProjects") else False

if debug:
    dataset = load_dataset("datajuicer/the-pile-pubmed-abstracts-refined-by-data-juicer")
    model = FCoref()
else:
    # dataset = load_dataset("qualis2006/PUBMED_title_abstracts_2020_baseline", streaming=True)

    data_files = "https://huggingface.co/datasets/casinca/PUBMED_title_abstracts_2019_baseline/resolve/main/PUBMED_title_abstracts_2019_baseline.jsonl.zst"
    pubmed_dataset = load_dataset(
        "json",
        data_files=data_files,
        split="train",
        download_config=DownloadConfig(delete_extracted=True),  # (optional arg)using DownloadConfig to save HD space
    )

    # model = FCoref(device='cuda:0')
    model = FCoref()

abstracts_text = dataset['train']['text']

preds = model.predict(
    texts=abstracts_text, max_tokens_in_batch=10000
)

with open("output/chains.txt", "w") as f_chains, open("output/indices_chains.txt", "w") as f_indices:
    for pred in preds:
        chains = pred.get_clusters()
        indices = pred.get_clusters(as_strings=False)
        for chain, index in zip(chains, indices):
            f_chains.write('\t'.join(chain) + '\n')
            f_indices.write(str(index) + '\n')
