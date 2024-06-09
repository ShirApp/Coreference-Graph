import os
from fastcoref import FCoref
from datasets import load_dataset

debug = True if os.path.exists("/Users/shir/PycharmProjects") else False

if debug:
    dataset = load_dataset("datajuicer/the-pile-pubmed-abstracts-refined-by-data-juicer")
    model = FCoref()
else:
    dataset = load_dataset("qualis2006/PUBMED_title_abstracts_2020_baseline")
    model = FCoref(device='cuda:0')

abstracts_text = dataset['train']['text']

preds = model.predict(
    texts=abstracts_text, max_tokens_in_batch=10000
)


for pred in preds:
    chains = pred.get_clusters()
    indices = pred.get_clusters(as_strings=False)
    for chain, index in zip(chains, indices):
        print('\t'.join(chain))
        print(index)
