import pickle
import re
from collections import defaultdict
from Bio import Entrez
from tqdm import tqdm


def get_phrases_occurrences(queries):
    global handle
    Entrez.email = "your_email@example.com"

    occurrences_dict = defaultdict(list)
    for query in tqdm(queries):
        try:
            handle = Entrez.esearch(db="pubmed", term=f'"{query}"', retmax=10)
            record = Entrez.read(handle)
            handle.close()
        except Exception as e:
            print(e)
            if handle:
                handle.close()
            continue

        # Retrieve the list of PubMed IDs
        if record and "IdList" in record:
            pubmed_ids = record["IdList"]
        else:
            continue

        # Fetch the articles corresponding to the PubMed IDs
        for pubmed_id in pubmed_ids:
            try:
                handle = Entrez.efetch(db="pubmed", id=pubmed_id, retmode="text", rettype="abstract")
                article = handle.read()
                handle.close()

                # Check if the specific word is present in the article
                if re.search(r'\b' + re.escape(query) + r'\b', article, re.IGNORECASE):
                    occurrences = re.findall(r'\b' + re.escape(query) + r'\b', article, re.IGNORECASE)
                    occurrences_dict[query] += occurrences

            except Exception as e:
                print(e)
                if handle:
                    handle.close()
                continue

            if len(occurrences_dict[query]) > 10:
                break

    return occurrences_dict


with open("data/all_nodes.pkl", 'rb') as f:
    queries = pickle.load(f)

queries=["il"]
results = get_phrases_occurrences(queries)
print(results)

with open("output/phrases_with_occurrences.txt", 'wb') as f:
    pickle.dump(results, f)
