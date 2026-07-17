from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task
from statuses.models import Status


class TasksCRUDTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.status = Status.objects.get(pk=1)
        self.task = Task.objects.get(pk=1)

    def test_anonymous_cannot_access_tasks(self):
        urls = [
            reverse('tasks_list'),
            reverse('task_create'),
            reverse('task_detail', kwargs={'pk': self.task.id}),
            reverse('task_update', kwargs={'pk': self.task.id}),
            reverse('task_delete', kwargs={'pk': self.task.id}),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_tasks_list_view(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('tasks_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_task_detail_view(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('task_detail', kwargs={'pk': self.task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)
        self.assertContains(response, self.task.description)

    def test_task_create(self):
        self.client.force_login(self.user1)
        url = reverse('task_create')
        data = {
            'name': 'Новая задача',
            'description': 'Ее описание',
            'status': self.status.id,
            'executor': self.user2.id,
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertTrue(Task.objects.filter(name='Новая задача').exists())

    def test_task_update(self):
        self.client.force_login(self.user1)
        url = reverse('task_update', kwargs={'pk': self.task.id})
        data = {
            'name': 'Обновленная задача',
            'description': 'Новое описание',
            'status': self.status.id,
            'executor': self.user2.id,
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('tasks_list'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Обновленная задача')

    def test_task_delete_by_author(self):
        self.client.force_login(self.user1)
        url = reverse('task_delete', kwargs={'pk': self.task.id})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertFalse(Task.objects.filter(pk=self.task.id).exists())

    def test_task_delete_by_stranger(self):
        self.client.force_login(self.user2)
        url = reverse('task_delete', kwargs={'pk': self.task.id})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertTrue(Task.objects.filter(pk=self.task.id).exists())

    def test_filter_tasks_by_status(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('tasks_list'),
                               {'status': self.status.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)
        response = self.client.get(reverse('tasks_list'), {'status': 999})
        self.assertNotContains(response, self.task.name)

    def test_filter_only_own_tasks(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('tasks_list'), {'only_own_tasks': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)
        self.client.force_login(self.user2)
        response = self.client.get(reverse('tasks_list'), {'only_own_tasks': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.task.name)