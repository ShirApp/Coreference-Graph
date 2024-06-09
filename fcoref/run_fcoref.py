import os
from fastcoref import FCoref
from datasets import load_dataset

debug = True if os.path.exists("/Users/shir/PycharmProjects") else False

if debug:
    dataset = load_dataset("datajuicer/the-pile-pubmed-abstracts-refined-by-data-juicer")
else:
    dataset = load_dataset("qualis2006/PUBMED_title_abstracts_2020_baseline")

abstracts_text = dataset['train']['text']

model = FCoref()

preds = model.predict(
    texts=abstracts_text, max_tokens_in_batch=10000
)
for pred in preds:
    print(pred.get_clusters(), pred.get_clusters(as_strings=False))

