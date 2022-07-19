from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from unittest.mock import patch
from core.models import User
from urllib.parse import urlsplit, parse_qs, urlparse
from django.http import HttpResponse

class TestLogin(TestCase):

    def setUp(self):
        self.client = Client()

    def test_pre_auth(self):
        pass

    @patch('core.views.redirect')
    @patch('core.views._fetch_spotify_user_data')
    @patch('core.views._exchange_code_for_token_data')
    def test_post_auth(self, token_mock, user_mock, redirect_mock):
        self.assertFalse(User.objects.exists())

        token_mock.return_value = {
            'access_token': 'hereisanaccesstoken',
            'scope': '',
            'expires_in': 3600,
            'refresh_token': 'test_refresh_token'
        }
        user_mock.return_value = {
            'id': '1',
            'email': 'test@test.com',
            'display_name': 'test_display_name',
            'images': [{'url': 'test_url'}]
        }
        redirect_mock.return_value = HttpResponse("")

        code = 'code=NApCCg..BkWtQ&state=34fFs29kd09'
        url = reverse('post_auth') + f'?code={code}'
        self.client.get(url)

        self.assertEqual(1, User.objects.count())
        user = User.objects.first()
        self.assertEqual(user_mock.return_value['id'], user.id)
        self.assertEqual(user_mock.return_value['email'], user.email)
        self.assertEqual(user_mock.return_value['display_name'],
                         user.display_name)
        self.assertEqual(user_mock.return_value['images'][0]['url'],
                         user.avatar_url)

        arg_url = redirect_mock.call_args.args[0]
        parsed_arg_url = urlparse(arg_url)

        base_url_from_arg = parsed_arg_url.netloc
        scheme = parsed_arg_url.scheme
        self.assertEqual(settings.NOSHUFF_FE_REDIRECT_URI,
                         f'{scheme}://{base_url_from_arg}')

        param_dict = parse_qs(parsed_arg_url.query)
        token = param_dict['noshuff_access_token'][0]
        user_from_token = User.get_user_from_auth_token(token)

        self.assertEqual(user, user_from_token)
        self.assertEqual(user.id, param_dict['user_id'][0])
        self.assertEqual(user.display_name, param_dict['display_name'][0])
        self.assertEqual(user.avatar_url, param_dict['avatar_url'][0])

        with self.subTest('Existing user'):
            self.client.get(url)
            self.assertEqual(1, User.objects.count())

        with self.subTest('Existing user data change'):
            original = user_mock.return_value['display_name']
            user_mock.return_value['display_name'] = 'new_test_display_name'
            self.client.get(url)
            self.assertEqual(1, User.objects.count())
            user = User.objects.first()
            self.assertEqual('new_test_display_name', user.display_name)
            self.assertNotEqual(original, user.display_name)
