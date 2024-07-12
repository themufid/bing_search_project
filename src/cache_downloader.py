import json
import os
import logging

def load_from_cache(query):
    """Load search results from cache.

    Args:
        query (str): Search query.

    Returns:
        dict: Search results in JSON format, or None if there is no cache.
    """
    cache_file = f"cache/{query}.json"

    if not os.path.exists(cache_file):
        return None

    with open(cache_file, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            logging.error(f"Failed to load cache for: {query}")
            return None

def save_to_cache(query, results_json):
    """Save search results to cache.

    Args:
        query (str): Search query.
        results_json (str): Search results in JSON format.
    """
    cache_dir = "cache"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    cache_file = f"{cache_dir}/{query}.json"
    with open(cache_file, 'w') as f:
        json.dump(results_json, f, indent=4)
