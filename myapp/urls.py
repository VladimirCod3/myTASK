from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:pk>/edit/', views.edit_task, name='edit_task'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='delete_task'),
    path('tasks/<int:task_id>/comment/', views.create_comment, name='create_comment'),
    path('tasks/<int:task_id>/attachment/', views.create_attachment, name='create_attachment'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
]

