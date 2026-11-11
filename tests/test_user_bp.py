
import unittest

from app import create_app


class FlaskUserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_login_page(self):
        response = self.client.get('/users/login')

        self.assertEqual(response.status_code, 200)

    def test_profile_redirect_without_login(self):
        response = self.client.get('/users/profile')

        self.assertEqual(response.status_code, 302)

    def test_login_success(self):
        response = self.client.post(
            '/users/login',
            data={
                'username': 'admin',
                'password': '1234'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'admin',
            response.get_data(as_text=True)
        )


if __name__ == '__main__':
    unittest.main()
