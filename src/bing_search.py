import argparse
import logging
import os
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote_plus
import signal
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.parser import parse_search_results

def signal_handler(sig, frame):
    logging.info("Exiting script...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

parser = argparse.ArgumentParser(description='Bing Search Script')
parser.add_argument('-query', type=str, required=True, help='Query for Bing search')
parser.add_argument('-limit', type=int, default=100, help='Max number of search results to get')
parser.add_argument('-resolve', action='store_true', help='Download cached results')
parser.add_argument('-search-domain', type=str, help='Limit search to a specific domain')
args = parser.parse_args()

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/bing_search.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def fetch_search_results(query, limit, domain=None):
    session = requests.Session()
    response = session.get('https://www.bing.com')
    soup = BeautifulSoup(response.content, 'html.parser')
    cid_tag = soup.find('input', {'name': 'IID'})
    cid = cid_tag['value'] if cid_tag else None
    
    if not cid:
        logging.error("Failed to retrieve conversation ID (CID).")
        return []

    results = []
    offset = 0

    while len(results) < limit:
        search_url = f"https://www.bing.com/search?q={quote_plus(query)}&first={offset}&count=50"
        if domain:
            search_url += f"+site:{domain}"
        
        response = session.get(search_url)
        page_results = parse_search_results(response.content, query, offset)

        if not page_results:
            break
        
        results.extend(page_results)
        offset += len(page_results)
    
    return results[:limit]

def download_cached_results(results):
    with ThreadPoolExecutor() as executor:
        for result in results:
            executor.submit(download_cached_version, result)

def download_cached_version(result):
    cache_url = result.get('cache_url')
    if cache_url:
        try:
            response = requests.get(cache_url)
            result['cached_content'] = response.text
        except requests.RequestException as e:
            logging.error(f"Failed to download cached version for URL: {cache_url} - {e}")

def main():
    query = args.query
    limit = args.limit
    domain = args.search_domain

    results = fetch_search_results(query, limit, domain)
    
    if results:
        print(f"Found {len(results)} results for '{query}'")
        for result in results:
            print(f"{result['Position']}: {result['Title']} - {result['link']}")
    else:
        print("Scrapping Successfully.")

    if args.resolve:
        download_cached_results(results)

    if not os.path.exists('output'):
        os.makedirs('output')
    output_file = f"output/{query.replace(' ', '_')}_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    logging.info(f"Results written to {output_file}")

if __name__ == "__main__":
    main()
