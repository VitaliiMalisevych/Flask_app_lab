import unittest
from app import app

class FlaskProductTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def test_products_list_page(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("IPhone".encode('utf-8'), response.data)

    def test_product_detail_page(self):
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("IPhone".encode('utf-8'), response.data)

    def test_product_not_found(self):
        response = self.client.get("/products/999")
        # Якщо товару немає, програма робить flash та redirect (302) на список
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()