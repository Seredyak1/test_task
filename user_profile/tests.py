# created by Seredyak1

import json

from django.contrib.auth.models import User
from django.test import Client

from rest_framework.test import APITestCase


class TestUserApi(APITestCase):

    def setUp(self):
        """Create client before every test"""
        self.client = Client()

#test user creation with good and wrong data
    def test_user_registration(self):
        """Assert a 201 status code was returned"""
        user_data = {"username": "test_user", "password": "test1234"}

        response = self.client.post('/users/', data=user_data)

        self.assertEqual(201, response.status_code)
        self.assertEqual(user_data['username'], response.data['username'])

    def test_user_registration_with_wrong_data(self):

        user_data = {"username": "", "password": "123"}

        response = self.client.post('/users/', data=user_data)

        self.assertEqual(400, response.status_code)

    def test_get_list_of_users(self):
        """Assert a 201 status code was returned.
        As 1 register user - len(response.data)==1"""
        self.test_user_registration()

        response = self.client.get('/users/')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))

#test user login with JWT token
    def test_user_login_with_right_data(self):
        """Assert a 200 status code was returned. Also token was returned"""
        self.test_user_registration()
        login_data = {"username": "test_user", "password": "test1234"}

        response = self.client.post('/api-token-auth/', data=login_data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(True, 'token' in response.data.keys())

    def test_user_login_with_wrong_data(self):
        """Assert a 400 status code and data without token was returned."""
        self.test_user_registration()
        login_data = {"username": "test_use", "password": "1234"}

        response = self.client.post('/api-token-auth/', data=login_data)

        self.assertEqual(400, response.status_code)
        self.assertEqual(False, 'token' in response.data.keys())

#test reshresh token for auth
    def test_refresh_token_by_auth_user(self):
        """200"""
        self.test_user_registration()
        login_data = {"username": "test_user", "password": "test1234"}

        get_token = self.client.post('/api-token-auth/', data=login_data)
        token = get_token.data['token']

        response = self.client.post('/api-token-refresh/', data={'token': token})

        self.assertEqual(200, response.status_code)

# get user detail if authorized or unauthorized
    def test_get_user_by_id_if_authorized(self):
        """Assert a 201 status code was returned"""
        self.test_user_registration()
        user = User.objects.first()
        self.client.force_login(user)

        response = self.client.get('/users/{}/'.format(user.id))

        self.assertEqual(200, response.status_code)
        self.assertEqual(user.id, response.data['id'])

    def test_get_user_by_id_if_unauthorized(self):
        """Assert a 401 status code was returned"""
        self.test_user_registration()
        user = User.objects.first()

        response = self.client.get('/users/{}/'.format(user.id))

        self.assertEqual(401, response.status_code)
        self.assertEqual('Unauthorized', response.status_text)

#Update. patch and delete user, if owner
    def test_update_user_by_id_if_owner(self):
        """Assert a 200 status code was returned, all parameters is not same"""
        user = User.objects.create(username='test_user')
        self.client.force_login(user)
        update_data = json.dumps({"email": "admin@admin.com", "first_name": "normal",
                                    "last_name": "name", "username": "test_user"})

        response = self.client.put('/users/{}/'.format(user.id),
                                   data=update_data,
                                   content_type='application/json')

        self.assertEqual(200, response.status_code)
        self.assertNotEqual(user.email, response.data['email'])
        self.assertNotEqual(user.first_name, response.data['first_name'])
        self.assertNotEqual(user.last_name, response.data['last_name'])
        self.assertEqual(user.username, response.data['username'])
        self.assertEqual(user.id, response.data['id'])

    def test_patch_data_user_is_owner(self):
        """Assert a 200 status code was returned, field 'first_name' is not same"""
        user = User.objects.create(username='test_user')
        self.client.force_login(user)
        patch_data = json.dumps({"first_name": "test normal name"})

        response = self.client.patch('/users/{}/'.format(user.id),
                                     data=patch_data,
                                     content_type='application/json')

        self.assertEqual(200, response.status_code)
        self.assertNotEqual(user.first_name, response.data['first_name'])

    def test_delete_user_is_owner(self):
        """Assert a 204 status code was returned"""
        user = User.objects.create(username='test_user')
        self.client.force_login(user)

        response = self.client.delete('/users/{}/'.format(user.id))

        self.assertEqual(204, response.status_code)
        self.assertEqual(0, User.objects.count())

#Test permissions for user
    def test_put_user_is_not_owner(self):
        """Assert a 403 status code was returned, user2 cannot put data to user1"""
        user1 = User.objects.create(username='test_user1')
        user2 = User.objects.create(username='test_user2')
        self.client.force_login(user2)
        update_data = json.dumps({"email": "admin@admin.com", "first_name": "normal",
                                  "last_name": "name", "username": "test_user1"})

        response = self.client.put('/users/{}/'.format(user1.id),
                                   data=update_data,
                                   content_type='application/json')

        self.assertEqual(403, response.status_code)

    def test_patch_user_is_not_owner(self):
        """Assert a 403 status code was returned, user2 cannot patch data to user1"""
        user1 = User.objects.create(username='test_user1')
        user2 = User.objects.create(username='test_user2')
        self.client.force_login(user2)
        patch_data = json.dumps({"first_name": "test normal name"})

        response = self.client.patch('/users/{}/'.format(user1.id),
                                     data=patch_data,
                                     content_type='application/json')

        self.assertEqual(403, response.status_code)

    def test_delete_user_is_not_owner(self):
        """Assert a 403 status code was returned, user2 cannot delete user1"""
        user1 = User.objects.create(username='test_user1')
        user2 = User.objects.create(username='test_user2')
        self.client.force_login(user2)

        response = self.client.delete('/users/{}/'.format(user1.id))

        self.assertEqual(403, response.status_code)
        self.assertEqual(2, User.objects.count())
