import unittest
from unittest.mock import patch
from src.bing_search import fetch_search_results

class TestBingSearch(unittest.TestCase):
    @patch('sys.argv', ['bing_search.py', '-query', 'python web scraping', '-limit', '100'])
    def test_fetch_search_results(self):
        results = fetch_search_results()
        self.assertIsNotNone(results)

if __name__ == '__main__':
    unittest.main()
