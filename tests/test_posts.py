
import unittest

from app import create_app, db
from app.posts.models import Post


class PostTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_post(self, title='Тестовий пост'):
        post = Post(
            title=title,
            content='Текст тестової публікації.',
            category='news',
            is_active=True,
            author='Test User'
        )
        db.session.add(post)
        db.session.commit()
        return post.id

    def test_create_post(self):
        response = self.client.post(
            '/post/create',
            data={
                'title': 'Новий тестовий пост',
                'content': 'Це тест створення нового поста.',
                'category': 'tech',
                'enabled': 'y',
                'publish_date': '2026-11-12T12:00'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        post = db.session.scalar(
            db.select(Post).where(
                Post.title == 'Новий тестовий пост'
            )
        )

        self.assertIsNotNone(post)
        self.assertEqual(post.category, 'tech')

    def test_list_posts(self):
        self.create_post()

        response = self.client.get('/post/')

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'Тестовий пост'.encode('utf-8'),
            response.data
        )

    def test_post_detail(self):
        post_id = self.create_post()

        response = self.client.get(f'/post/{post_id}')

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'Текст тестової публікації.'.encode('utf-8'),
            response.data
        )

    def test_update_post(self):
        post_id = self.create_post()

        response = self.client.post(
            f'/post/{post_id}/update',
            data={
                'title': 'Оновлений пост',
                'content': 'Оновлений текст публікації.',
                'category': 'publication',
                'enabled': 'y',
                'publish_date': '2026-11-12T13:00'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        post = db.session.get(Post, post_id)

        self.assertEqual(post.title, 'Оновлений пост')
        self.assertEqual(post.category, 'publication')

    def test_delete_post(self):
        post_id = self.create_post()

        response = self.client.post(
            f'/post/{post_id}/delete',
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(db.session.get(Post, post_id))

    def test_post_not_found(self):
        response = self.client.get('/post/99999')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
