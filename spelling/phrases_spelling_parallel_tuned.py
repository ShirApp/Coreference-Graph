import json
import pickle
import re
import asyncio
import aiohttp
from collections import defaultdict
from Bio import Entrez
from tqdm import tqdm

Entrez.email = "your_email@example.com"
RATE_LIMIT = 3  # Adjust based on API's rate limit
RETRY_LIMIT = 5  # Number of retries before giving up
RETRY_BACKOFF_FACTOR = 2  # Exponential backoff factor


async def fetch_with_retry(session, url, retries=RETRY_LIMIT):
    for attempt in range(retries):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json() if 'json' in url else await response.text()
                elif response.status == 429:  # Rate limit exceeded
                    retry_after = int(response.headers.get("Retry-After", 2))  # Use Retry-After header if available
                    await asyncio.sleep(retry_after * RETRY_BACKOFF_FACTOR ** attempt)
                else:
                    response.raise_for_status()
        except Exception as e:
            if attempt == retries - 1:
                print(f"Error fetching URL '{url}': {e}")
                return None
            await asyncio.sleep(RETRY_BACKOFF_FACTOR ** attempt)


async def fetch_esearch(session, query):
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term="{query}"&retmax=10&retmode=json'
    return await fetch_with_retry(session, url)


async def fetch_efetch(session, pubmed_id):
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pubmed_id}&retmode=text&rettype=abstract'
    return await fetch_with_retry(session, url)


async def process_query(semaphore, session, query, occurrences_dict):
    async with semaphore:
        record = await fetch_esearch(session, query)
        if record and "esearchresult" in record and "idlist" in record["esearchresult"]:
            pubmed_ids = record["esearchresult"]["idlist"]
            for pubmed_id in pubmed_ids:
                async with semaphore:
                    article = await fetch_efetch(session, pubmed_id)
                    if article:
                        if re.search(r'\b' + re.escape(query) + r'\b', article, re.IGNORECASE):
                            occurrences = re.findall(r'\b' + re.escape(query) + r'\b', article, re.IGNORECASE)
                            occurrences_dict[query] += occurrences
                            if len(occurrences_dict[query]) > 10:
                                break


async def get_phrases_occurrences(query):
    occurrences_dict = defaultdict(list)
    semaphore = asyncio.Semaphore(RATE_LIMIT)  # Rate limit semaphore
    async with aiohttp.ClientSession() as session:
        await process_query(semaphore, session, query, occurrences_dict)
    return occurrences_dict


async def main():
    with open("data/nodes_10%_high.pkl", 'rb') as f:
        queries = list(pickle.load(f).keys())
    # queries = queries[:2]
    all_results = defaultdict(list)
    total_queries = len(queries)
    done_queries = set()
    with open("output/phrases_with_occurrences.txt", "r") as f:
        for line in f.readlines():
            phrase = set(eval(line.strip()).keys())
            done_queries = done_queries.union(phrase)
    with open("output/phrases_with_occurrences.txt", "a") as f:
        with tqdm(total=total_queries) as overall_progress:
            for query in queries:
                if query in done_queries:
                    continue
                results = await get_phrases_occurrences(query)
                for key, value in results.items():
                    all_results[key].extend(value)
                f.write(str(dict(results)) + "\n")
                overall_progress.update(1)

    print(all_results)

asyncio.run(main())
