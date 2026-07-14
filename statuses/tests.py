from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from statuses.models import Status


class StatusesCRUDTestCase(TestCase):
    fixtures = ['statuses.json']

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)

    def test_anonymous_cannot_access_statuses(self):
        urls = [
            reverse('statuses_list'),
            reverse('status_create'),
            reverse('status_update', kwargs={'pk': self.status1.id}),
            reverse('status_delete', kwargs={'pk': self.status1.id}),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_statuses_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('statuses_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.status1.name)
        self.assertContains(response, self.status2.name)

    def test_status_create(self):
        self.client.force_login(self.user)
        url = reverse('status_create')
        data = {'name': 'На тестировании'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertTrue(Status.objects.filter(name='На тестировании').exists())

    def test_status_update(self):
        self.client.force_login(self.user)
        url = reverse('status_update', kwargs={'pk': self.status1.id})
        data = {'name': 'Новый Измененный'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('statuses_list'))
        self.status1.refresh_from_db()
        self.assertEqual(self.status1.name, 'Новый Измененный')

    def test_status_delete(self):
        self.client.force_login(self.user)
        url = reverse('status_delete', kwargs={'pk': self.status1.id})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertFalse(Status.objects.filter(pk=self.status1.id).exists())