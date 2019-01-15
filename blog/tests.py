# created by Seredyak1
import json

from django.contrib.auth.models import User
from django.test import Client

from rest_framework.test import APITestCase

from blog.models import Post


class TestPostApi(APITestCase):
    """Unit tests for Post"""

    def setUp(self):
        """Create client and user before every test"""
        self.client = Client()
        self.user = User.objects.create()

# Tests for CRUDL for Post if user is owner
    def test_create_post_if_authorized(self):
        """Assert a 201 status code was returned"""
        self.client.force_login(self.user)

        response = self.client.post('/posts/',
                                    data={'title': 'Test title', 'body': "Test body"})

        self.assertEqual(201, response.status_code)

    def test_get_list_of_posts_if_authorized(self):
        """Assert 200 status code. Worked if user is owner"""
        self.test_create_post_if_authorized()

        response = self.client.get('/posts/')

        self.assertEqual(200, response.status_code)

    def test_get_one_post_by_id_if_authorized(self):
        """Assert 200 status code. Worked if user is owner"""
        self.test_create_post_if_authorized()
        post = Post.objects.first()

        response = self.client.get('/posts/{}/'.format(post.id))

        self.assertEqual(200, response.status_code)
        self.assertEqual(post.title, response.data['title'])

    def test_update_post_by_id_if_authorized(self):
        """Assert 200 status code. Worked if user is owner"""
        self.test_create_post_if_authorized()
        post = Post.objects.first()

        response = self.client.put('/posts/{}/'.format(post.id),
                                   data=json.dumps({"title": "Another title", "body": "Another body"}),
                                   content_type='application/json')

        self.assertEqual(200, response.status_code)
        self.assertNotEqual(post.body, response.data['body'])

    def test_patch_post_by_id_if_authorized(self):
        """Assert 200 status code. Worked if user is owner"""
        self.test_create_post_if_authorized()
        post = Post.objects.first()

        response = self.client.patch('/posts/{}/'.format(post.id),
                                     data=json.dumps({"body": "Patched_data"}),
                                     content_type='application/json')

        self.assertEqual(200, response.status_code)
        self.assertNotEqual(post.body, response.data['body'])

    def test_delete_post_by_id(self):
        """Assert 204 status code. Worked if user is owner"""
        self.test_create_post_if_authorized()
        post = Post.objects.first()

        response = self.client.delete('/posts/{}/'.format(post.id))

        self.assertEqual(204, response.status_code)
        self.assertEqual(0, Post.objects.count())

#test if user is not unauthorized

    def test_get_list_with_posts_if_unauthorized(self):
        """Assert a 401 status code was returned"""

        response = self.client.get('/posts/')

        self.assertEqual(401, response.status_code)
        self.assertEqual('Unauthorized', response.status_text)

    def test_get_post_if_unauthorized(self):
        """Assert a 401 status code was returned"""
        self.test_create_post_if_authorized()
        self.client.logout()
        post = Post.objects.first()

        response = self.client.get('/posts/{}/'.format(post.id))

        self.assertEqual(401, response.status_code)
        self.assertEqual('Unauthorized', response.status_text)

    def test_update_post_if_unauthorized(self):
        """Assert 401 status code was returned"""
        self.test_create_post_if_authorized()
        self.client.logout()
        post = Post.objects.first()

        response = self.client.put('/posts/{}/'.format(post.id),
                                   data=json.dumps({"title": "Another title", "body": "Another body"}),
                                   content_type='application/json')

        self.assertEqual(401, response.status_code)
        self.assertEqual('Unauthorized', response.status_text)

    def test_patch_post_if_unauthorized(self):
        """Assert 401 status code was returned"""
        self.test_create_post_if_authorized()
        self.client.logout()
        post = Post.objects.first()

        response = self.client.patch('/posts/{}/'.format(post.id),
                                     data=json.dumps({"body": "Patched_data"},),
                                     content_type='application/json')

        self.assertEqual(401, response.status_code)
        self.assertEqual('Unauthorized', response.status_text)

    def test_delete_post_if_unauthorized(self):
        """Assert 401 status code was returned"""
        self.test_create_post_if_authorized()
        self.client.logout()
        post = Post.objects.first()

        response = self.client.delete('/posts/{}/'.format(post.id))

        self.assertEqual(401, response.status_code)
        self.assertEqual('Unauthorized', response.status_text)

#Test permission, when user is no owner

    def test_update_post_is_user_is_not_owner(self):
        """Assert 403 status code was returned"""
        self.test_create_post_if_authorized()
        self.client.logout()
        post = Post.objects.first()

        second_user = User.objects.create(username='second_user')
        self.client.force_login(second_user)

        response = self.client.put('/posts/{}/'.format(post.id),
                                   data=json.dumps({"title": "Another user title", "body": "Another user body"}),
                                   content_type='application/json')

        self.assertEqual(403, response.status_code)

    def test_patch_post_is_user_is_not_owner(self):
        """Assert 403 status code was returned"""
        self.test_create_post_if_authorized()
        self.client.logout()
        post = Post.objects.first()

        second_user = User.objects.create(username='second_user')
        self.client.force_login(second_user)

        response = self.client.put('/posts/{}/'.format(post.id),
                                   data=json.dumps({"body": "Another user body"}),
                                   content_type='application/json')

        self.assertEqual(403, response.status_code)


    def test_delete_post_if_user_is_not_owner(self):
        """Assert 403 status code" was returned"""
        self.test_create_post_if_authorized()
        self.client.logout()
        post = Post.objects.first()

        second_user = User.objects.create(username='second_user')
        self.client.force_login(second_user)

        response = self.client.delete('/posts/{}/'.format(post.id))

        self.assertEqual(403, response.status_code)
        self.assertEqual(1, Post.objects.count())

# Test for likes
    def test_add_like_to_post(self):
        """Assert 200 status code was returned, and check like_count to 1"""
        self.test_create_post_if_authorized()
        post = Post.objects.first()

        add_like = self.client.post('/posts/{}/like/'.format(post.id))

        response = self.client.get('/posts/')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, post.like_count)

    def test_unlike_to_post(self):
        """Check like_count to 1, and after delete this like - like_count is 0"""
        self.test_create_post_if_authorized()
        post = Post.objects.first()

        add_like = self.client.post('/posts/{}/like/'.format(post.id))

        response = self.client.get('/posts/')
        self.assertEqual(1, post.like_count)

        unlike = self.client.delete('/posts/{}/unlike/'.format(post.id))

        response2 = self.client.get('/posts/')

        self.assertEqual(0, post.like_count)

    def test_like_post_by_2_users(self):
        """Add likes by 2 users, like_count is 2"""
        self.test_create_post_if_authorized()
        post = Post.objects.first()

        add_like_by_first_user = self.client.post('/posts/{}/like/'.format(post.id))
        self.client.logout()

        second_user = User.objects.create(username='second_user')
        self.client.force_login(second_user)
        add_like_by_second_user = self.client.post('/posts/{}/like/'.format(post.id))

        response = self.client.get('/posts/')

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, post.like_count)
