"""
Unit Testing the endpoints
"""
import unittest

import main


class TestTailAgent(unittest.TestCase):
    """
    Unit testcases for tail agent
    """

    def setUp(self):
        """
        setting up flask test client
        """
        self.app = main.app.test_client()
        self.app.testing = True

    def test_start_endpoint(self):
        """
        testing start endpoint
        """
        response = self.app.post('/start', json={"filepath": "new.txt"})
        self.assertEqual(response.status_code, 200)

    def test_stop_endpoint(self):
        """
        testing stop endpoint
        """
        response = self.app.get('/stop')
        self.assertEqual(response.status_code, 200)

    def test_status_endpoint(self):
        """
        testing status endpoint
        """
        response = self.app.get('/status')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
