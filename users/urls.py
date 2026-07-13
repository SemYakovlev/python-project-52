from django.urls import path
from users.views import (
    UsersListView, UserCreateView, UserUpdateView, UserDeleteView,
    UserLoginView, UserLogoutView
)

urlpatterns = [
    path('', UsersListView.as_view(), name='users_list'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
]