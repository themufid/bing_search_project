# Bing Search and Cache Downloader

## Project Overview
We need a Python script that will use the Bing search engine to perform searches and optionally download cached results. The script will initiate a session, extract a conversation ID (CID) from the Bing homepage, and use it to perform searches until a specified limit is reached. The results can be limited to a specific domain if provided. Additionally, the script can download the cached versions of the search results. If the -endpoint argument is provided, the script should send the search results to an internal API instead of writing them to a file.

## Usage Instructions

### Prerequisites
- Python 3.x
- Required Python libraries: requests, BeautifulSoup4, concurrent.futures, logging, argparse

### Setup
1. Clone the repository containing the script.
2. Install the required libraries:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Script
Basic Usage:
```sh
python src/bing_search.py -query "<search_query>" [-limit <limit>] [-resolve] [-search-domain <domain>] [-endpoint [<ip_address>]]

