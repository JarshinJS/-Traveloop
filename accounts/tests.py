from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse


class AccountSettingsTests(TestCase):
    def test_login_redirect_url_points_to_trips(self):
        self.assertEqual(settings.LOGIN_REDIRECT_URL, '/trips/')


class ProfileViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='traveler',
            password='pass12345',
            email='old@example.com',
        )
        self.client.login(username='traveler', password='pass12345')

    def test_profile_update_preserves_missing_language_preference(self):
        response = self.client.post(reverse('profile'), {
            'update_info': '1',
            'first_name': 'Tara',
            'last_name': 'Loop',
            'email': 'tara@example.com',
        })

        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Tara')
        self.assertEqual(self.user.last_name, 'Loop')
        self.assertEqual(self.user.email, 'tara@example.com')
        self.assertEqual(self.user.profile.language_preference, 'en')

    def test_profile_rejects_non_image_avatar_upload(self):
        upload = SimpleUploadedFile(
            'avatar.txt',
            b'not an image',
            content_type='text/plain',
        )

        response = self.client.post(reverse('profile'), {'avatar': upload})

        self.assertEqual(response.status_code, 200)
        self.user.profile.refresh_from_db()
        self.assertFalse(self.user.profile.avatar)


class AccountDeleteViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='delete-me', password='pass12345')
        self.client.login(username='delete-me', password='pass12345')

    def test_account_delete_requires_post(self):
        response = self.client.get(reverse('account_delete'))

        self.assertEqual(response.status_code, 405)
        self.assertTrue(User.objects.filter(username='delete-me').exists())

    def test_account_delete_removes_user(self):
        response = self.client.post(reverse('account_delete'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('dashboard'))
        self.assertFalse(User.objects.filter(username='delete-me').exists())
