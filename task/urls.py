from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path("login/", views.login_view, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("home/", views.home, name="home"),
    path('task/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:task_id>/delete/', views.task_delete, name='task-delete'),
    
    # Add login view and other views if needed
]

