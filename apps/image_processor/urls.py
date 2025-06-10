from django.urls import path
from .views import process_image, get_task_status
urlpatterns = [
    path('process/', process_image, name='process_image'),
    path('task_status/<str:task_id>', get_task_status, name='task_status'),

]