from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from labels.models import Label
from labels.forms import LabelForm


class LabelsListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/labels_list.html'
    context_object_name = 'labels'
    login_url = reverse_lazy('login')


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels_list')
    success_message = 'Метка успешно создана'
    login_url = reverse_lazy('login')


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels_list')
    success_message = 'Метка успешно изменена'
    login_url = reverse_lazy('login')


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/label_confirm_delete.html'
    success_url = reverse_lazy('labels_list')
    success_message = 'Метка успешно удалена'
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tasks.exists():
            messages.error(self.request, 'Невозможно удалить метку')
            return redirect('labels_list')
        return super().post(request, *args, **kwargs)