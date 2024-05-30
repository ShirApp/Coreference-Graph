import pickle
import re
from collections import defaultdict
import asyncio
import aiohttp
from Bio import Entrez
from tqdm import tqdm

Entrez.email = "your_email2@example.com"


async def fetch_esearch(session, query):
    try:
        async with session.get(f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term="{query}"&retmax=10&retmode=json') as response:
            return await response.json()
    except Exception as e:
        print(f"Error fetching esearch for query '{query}': {e}")
        return None


async def fetch_efetch(session, pubmed_id):
    try:
        async with session.get(f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pubmed_id}&retmode=text&rettype=abstract') as response:
            return await response.text()
    except Exception as e:
        print(f"Error fetching efetch for PubMed ID '{pubmed_id}': {e}")
        return None


async def process_query(session, query, occurrences_dict):
    record = await fetch_esearch(session, query)
    print(record)
    if record and "esearchresult" in record and "idlist" in record["esearchresult"]:
        pubmed_ids = record["esearchresult"]["idlist"]
        for pubmed_id in pubmed_ids:
            article = await fetch_efetch(session, pubmed_id)
            if article:
                if re.search(r'\b' + re.escape(query) + r'\b', article, re.IGNORECASE):
                    occurrences = re.findall(r'\b' + re.escape(query) + r'\b', article, re.IGNORECASE)
                    occurrences_dict[query] += occurrences
                    if len(occurrences_dict[query]) > 10:
                        break


async def process_batch(session, queries, occurrences_dict, overall_progress):
    tasks = [process_query(session, query, occurrences_dict) for query in queries]
    for f in tqdm(asyncio.as_completed(tasks), total=len(tasks), leave=False):
        await f
        overall_progress.update(1)


def chunked_iterable(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]


async def get_phrases_occurrences(queries):
    occurrences_dict = defaultdict(list)
    async with aiohttp.ClientSession() as session:
        total_queries = len(queries)
        with tqdm(total=total_queries) as overall_progress:
            for batch in chunked_iterable(queries, 1000):
                await process_batch(session, batch, occurrences_dict, overall_progress)
    return occurrences_dict


async def main():
    with open("data/all_nodes.pkl", 'rb') as f:
        queries = pickle.load(f)
    queries = queries[:1000]
    print(queries)
    results = await get_phrases_occurrences(queries)
    print(results)

    with open("output/phrases_with_occurrences.pkl", 'wb') as f:
        pickle.dump(results, f)

# Run the main function
asyncio.run(main())
