import unittest
from app import app

class FlaskUserTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def test_login_page(self):
        response = self.client.get("/users/login")
        self.assertEqual(response.status_code, 200)

    def test_profile_page_redirect_without_login(self):
        response = self.client.get("/users/profile")
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()