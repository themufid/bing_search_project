# Bing Search and Cache Downloader

## Project Overview
This Python script provides functionalities for performing Bing searches, retrieving results, and optionally downloading cached versions of the results. It offers features like:
- User-defined search queries
- Result limit specification
- Cached result downloading (optional)
- Domain-limited searches (optional)
- Integration with an internal API for result delivery (optional)
- Robust error handling and comprehensive logging
- User control over limits and options

## Usage Instructions

### Setup
1. Clone the repository containing the script.
2. Install the required libraries:
    ```sh
    python -m pip install -r requirements.txt
    ```

### Running the Script
Usage:
1. Navigate to the project directory in your terminal.
2. Run the script using the following command:

```sh
python src/bing_search.py -query "<search_query>" [OPTIONS]
```

Options:
-query <search_query>: Replace <search_query> with your desired search term.

-limit <number>: Specify the maximum number of results (default: 50).

-debug Y|N: Enable (Y) or disable (N) debug logging (default: N).

-resolve: Download cached versions of search results (optional).

Examples:
1. Basic search with default limit:
```sh
python src/bing_search.py -query "python book"
```

2. Search with limit of 100 results:
```sh
python src/bing_search.py -query "web development" -limit 100
```

3. Enable debug logging:
```sh
python src/bing_search.py -query "machine learning" -debug Y
```

4. Download cached results:
```sh
python src/bing_search.py -query "data science" -resolve
```

5. Combine options:
```sh
python src/bing_search.py -query "cloud computing site:ibm.com" -limit 25 -debug Y -resolve
```

Cached Results:

- Cached results are downloaded and saved in JSON format to the cache directory within the project directory.
- The filename follows the format <search_query>.json, where <search_query> is replaced with the actual search term.