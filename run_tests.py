import unittest
import requests
import time
import threading
from main import app

class SleepMonitorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
    
    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_token_route(self):
        response = self.app.post('/api/token')
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.get_json())

if __name__ == '__main__':
    unittest.main()
