from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from labels.models import Label
from tasks.models import Task


class LabelsCRUDTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)
        self.task = Task.objects.get(pk=1)

    def test_anonymous_cannot_access_labels(self):
        urls = [
            reverse('labels_list'),
            reverse('label_create'),
            reverse('label_update', kwargs={'pk': self.label1.id}),
            reverse('label_delete', kwargs={'pk': self.label1.id}),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_labels_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('labels_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.label1.name)
        self.assertContains(response, self.label2.name)

    def test_label_create(self):
        self.client.force_login(self.user)
        url = reverse('label_create')
        data = {'name': 'Документация'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('labels_list'))
        self.assertTrue(Label.objects.filter(name='Документация').exists())

    def test_label_update(self):
        self.client.force_login(self.user)
        url = reverse('label_update', kwargs={'pk': self.label1.id})
        data = {'name': 'Баг критический'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('labels_list'))
        self.label1.refresh_from_db()
        self.assertEqual(self.label1.name, 'Баг критический')

    def test_label_delete_unlinked(self):
        self.client.force_login(self.user)
        url = reverse('label_delete', kwargs={'pk': self.label2.id})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('labels_list'))
        self.assertFalse(Label.objects.filter(pk=self.label2.id).exists())

    def test_label_delete_linked(self):
        self.task.labels.add(self.label1)
        self.client.force_login(self.user)

        url = reverse('label_delete', kwargs={'pk': self.label1.id})
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, reverse('labels_list'))
        self.assertTrue(Label.objects.filter(pk=self.label1.id).exists())
        self.assertContains(response, 'Невозможно удалить метку')