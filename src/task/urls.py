from django.urls import path
from .views import task_list, update_task, remove_task, add_task, complete_task

urlpatterns = [
    path('todo', task_list, name='task-list'),
    path('add-task/', add_task, name='add-task'),
    path('remove-task/', remove_task, name='remove-task'),
    path('update-task/', update_task, name='update-task'),
    path('complete-task/', complete_task, name='complete-task'),
]
