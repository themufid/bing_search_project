import argparse
import logging
import requests
from bs4 import BeautifulSoup
import os
import json
import signal
import sys
from urllib.parse import quote_plus
import cache_downloader

def signal_handler(sig, frame):
  """Handles interrupt signals (Ctrl+C) gracefully."""
  logging.info("Exiting script...")
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def setup_logging(debug):
  """Sets up logging configuration."""
  if not os.path.exists('logs'):
    os.makedirs('logs') 

  log_level = logging.DEBUG if debug == 'Y' else logging.INFO
  logging.basicConfig(level=log_level,
                      format='%(asctime)s - %(levelname)s - %(message)s',
                      handlers=[logging.FileHandler('logs/bing_search.log'),
                                logging.StreamHandler()])

def parse_and_log_results(html_content):
  """Parses HTML content and returns search results in JSON format."""
  soup = BeautifulSoup(html_content, 'html.parser')
  results = []

  for item in soup.select("li.b_algo"):
    title = item.find("a").text.strip()
    link = item.find("a")["href"]
    description = item.find("div.b_caption")
    if description:
      description = description.text.strip()
    else:
      description = ""

    results.append({"Title": title, "Link": link, "Description": description})

  with open('output/bing_search_results.json', 'w') as outfile:
    json.dump(results, outfile, indent=4)

  if args.resolve:
    cache_downloader.save_to_cache(args.query, results)  # Use results directly

  return results

def main(query, limit, debug):
  """Performs Bing search, retrieves results, and handles caching."""
  setup_logging(debug)
  session = requests.Session()

  logging.info(f"Starting Bing search for: {query}")

  offset = 0
  total_results = 0

  while total_results < limit:
    search_url = f"https://www.bing.com/search?q={quote_plus(query)}&first={offset}"
    response = session.get(search_url)

    cached_results = cache_downloader.load_from_cache(query)
    if cached_results:
      logging.info(f"Using cached results for: {query}")
      print(cached_results)  
      break  
  
    if response.status_code != 200:
      logging.error(f"Failed to retrieve results: {response.status_code}")
      break

    results_json = parse_and_log_results(response.content)

    print(results_json)  

    offset += 10

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Bing Search with Cache Download")
  parser.add_argument("-query", required=True, help="Search query")
  parser.add_argument("-limit", type=int, default=50, help="Maximum results (default: 50)")
  parser.add_argument("-debug", choices=["Y", "N"], default="N", help="Enable debug logging (Y/N)")
  parser.add_argument("-resolve", action="store_true", help="Download cached results (optional)")

  args = parser.parse_args()

  main(args.query, args.limit, args.debug)
