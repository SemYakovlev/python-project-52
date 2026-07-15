from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import ProtectedError
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from users.forms import CustomUserCreationForm, CustomUserUpdateForm


class UserPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для изменения.')
        return redirect('users_list')


class UsersListView(ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'


class UserUpdateView(LoginRequiredMixin, UserPermissionMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users_list')
    success_message = 'Пользователь успешно изменен'
    login_url = reverse_lazy('login')


class UserDeleteView(LoginRequiredMixin, UserPermissionMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users_list')
    success_message = 'Пользователь успешно удален'
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(self.request, self.success_message)
            return response
        except ProtectedError:
            messages.error(self.request, 'Невозможно удалить пользователя, потому что он используется')
            return redirect('users_list')


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    success_message = 'Вы залогинены'
    next_page = reverse_lazy('home')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Вы разлогинены')
        return super().dispatch(request, *args, **kwargs)