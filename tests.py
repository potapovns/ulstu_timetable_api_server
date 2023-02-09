import unittest
import main as tested_app


class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        tested_app.app.config['TESTING'] = True
        self.app = tested_app.app.test_client()

    def test_api_endpoint(self):
        r = self.app.get('/api')
        self.assertEqual(r.json, {"status": "te st"})

    def test_home_page(self):
        r = self.app.get('/')
        self.assertEqual(r.data, b'Hello world!')


if __name__ == '__main__':
    unittest.main()
