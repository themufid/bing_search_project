import argparse
import logging
import requests
from bs4 import BeautifulSoup
from config import COOKIES, HEADERS
import os
import json
import signal
import sys
from urllib.parse import quote_plus
from api_handler import post_to_api

def signal_handler(sig, frame):
    logging.info("Exiting script...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def setup_logging(debug):
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    log_level = logging.DEBUG if debug == 'Y' else logging.INFO
    logging.basicConfig(level=log_level, 
                        format='%(asctime)s - %(levelname)s - %(message)s', 
                        handlers=[logging.FileHandler('logs/bing_search.log'),
                                  logging.StreamHandler()])

def parse_and_log_results(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []

    for item in soup.select("li.b_algo"):
        title = item.find("a").text
        link = item.find("a")["href"]
        description = item.find("div.b_caption").text
        results.append({"Title": title, "Link": link, "Description": description})

    return results

def main(query, limit, debug):
    setup_logging(debug)
    session = requests.Session()
    session.cookies.update(COOKIES)

    logging.info(f"Starting Bing search for: {query}")

    offset = 0
    total_results = 0

    while total_results < limit:
        search_url = f"https://www.bing.com/search?q={quote_plus(query)}&first={offset}"
        response = session.get(search_url, headers=HEADERS)

        if response.status_code != 200:
            logging.error(f"Failed to retrieve results: {response.status_code}")
            break

        results = parse_and_log_results(response.content)
        total_results += len(results)
        logging.info(f"Retrieved {len(results)} results.")
        
        for result in results:
            logging.info(result)

            api_response = post_to_api("24.152.187.23", result)
            if api_response:
                logging.info(f"Posted to API: {api_response.status_code}")

        offset += 10

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Bing Search Script')
    parser.add_argument('-query', type=str, required=True, help='Query for Bing search')
    parser.add_argument('-limit', type=int, default=500, help='Max number of search results to get')
    parser.add_argument('-debug', type=str, default='N', help='Debug mode (Y/N)')
    args = parser.parse_args()

    main(args.query, args.limit, args.debug)
