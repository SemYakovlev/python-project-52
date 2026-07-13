from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UsersCRUDTestCase(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)

    def test_users_list_view(self):
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user2.username)

    def test_user_registration(self):
        url = reverse('user_create')
        data = {
            'first_name': 'Ned',
            'last_name': 'Stark',
            'username': 'ned_stark',
            'password1': 'WinterIsComing123',
            'password2': 'WinterIsComing123',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='ned_stark').exists())

    def test_user_update_by_owner(self):
        self.client.force_login(self.user1)
        url = reverse('user_update', kwargs={'pk': self.user1.id})
        data = {
            'first_name': 'TirionUpdated',
            'last_name': 'Lannister',
            'username': 'tirion_updated',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('users_list'))
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, 'TirionUpdated')

    def test_user_update_by_stranger(self):
        self.client.force_login(self.user1)
        url = reverse('user_update', kwargs={'pk': self.user2.id})
        data = {
            'first_name': 'Hacker',
            'last_name': 'Man',
            'username': 'hacker_man',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('users_list'))
        self.user2.refresh_from_db()
        self.assertNotEqual(self.user2.first_name, 'Hacker')

    def test_user_delete_by_owner(self):
        self.client.force_login(self.user1)
        url = reverse('user_delete', kwargs={'pk': self.user1.id})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('users_list'))
        self.assertFalse(User.objects.filter(pk=self.user1.id).exists())

    def test_user_delete_by_stranger(self):
        self.client.force_login(self.user1)
        url = reverse('user_delete', kwargs={'pk': self.user2.id})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('users_list'))
        self.assertTrue(User.objects.filter(pk=self.user2.id).exists())