from django.test import TestCase

from models.factories.posts import PostFactory


class PostListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = '/api/posts/'
        cls.post_1 = PostFactory()
        cls.post_2 = PostFactory()

    def test_list_with_min_parameters_status_200(self):
        response = self.client.get(
            self.url,
        )

        self.assertEqual(response.status_code, 200)