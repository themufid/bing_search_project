import unittest
from src.bing_search import fetch_search_results

class TestBingSearch(unittest.TestCase):
    def test_fetch_search_results(self):
        query = "test"
        results = fetch_search_results(query, 10)
        self.assertIsNotNone(results)
        self.assertTrue(len(results) > 0)

if __name__ == '__main__':
    unittest.main()

