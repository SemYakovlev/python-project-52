from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
from tasks.models import Task
from tasks.forms import TaskForm


class AuthorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != request.user:
            messages.error(request, 'Задачу может удалить только ее автор')
            return redirect('tasks_list')
        return super().dispatch(request, *args, **kwargs)


class TasksListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/tasks_list.html'
    context_object_name = 'tasks'
    login_url = reverse_lazy('login')


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    login_url = reverse_lazy('login')


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks_list')
    success_message = 'Задача успешно создана'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks_list')
    success_message = 'Задача успешно изменена'
    login_url = reverse_lazy('login')


class TaskDeleteView(LoginRequiredMixin, AuthorRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks_list')
    success_message = 'Задача успешно удалена'
    login_url = reverse_lazy('login')