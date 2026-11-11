
import unittest
from unittest.mock import patch

from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from app import create_app


class FlaskProductTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

        self.test_db = TinyDB(storage=MemoryStorage)

        self.db_patcher = patch(
            'app.products.views.db',
            self.test_db
        )
        self.db_patcher.start()

        self.product_id = self.test_db.insert({
            'name': 'Laptop',
            'price': 25000,
            'amount': 10,
            'description': 'Тестовий ноутбук',
            'image': None
        })

    def tearDown(self):
        self.db_patcher.stop()
        self.test_db.close()

    def test_products_list_page(self):
        response = self.client.get('/products/')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Laptop', response.data)

    def test_product_detail_page(self):
        response = self.client.get(
            f'/products/{self.product_id}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Laptop', response.data)

    def test_product_not_found(self):
        response = self.client.get('/products/99999')

        self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main()
