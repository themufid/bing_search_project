import json
import os

def load_from_cache(query):
    """Memuat hasil pencarian dari cache.

    Args:
        query (str): Kueri pencarian.

    Returns:
        dict: Hasil pencarian dalam format JSON, atau None jika tidak ada cache.
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
    """Menyimpan hasil pencarian ke cache.

    Args:
        query (str): Kueri pencarian.
        results_json (str): Hasil pencarian dalam format JSON.
    """
    cache_dir = "cache"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    cache_file = f"{cache_dir}/{query}.json"
    with open(cache_file, 'w') as f:
        json.dump(results_json, f, indent=4)
