from django.core.urlresolvers import reverse
from django.test import TestCase

from base import testing
from blog.models import Post
from content.scenarios import TestScenariosMixin


class PostUrlTest(TestScenariosMixin, TestCase):
    def test_blog_index(self):
        response = testing.get_public_client().get(reverse('post_index'))
        self.assertEqual(200, response.status_code)

        author = testing.create_user()
        post_a = Post.create_for_testing(author)
        post_a.reviewed = True
        post_a.save()

        post_b = Post.create_for_testing(author)
        post_b.reviewed = False
        post_b.save()

        response = testing.get_public_client().get(reverse('post_index'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context['all_posts']))

        response = testing.get_user_client(author).get(reverse('post_index'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['all_posts']))

        response = testing.get_user_client().get(reverse('post_index'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context['all_posts']))

    def test_approve_post(self):
        self.content_approve(Post)

    def test_review_post(self):
        self.content_review(Post)
