from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import process_image, get_task_status, ImageUploadViewSet

router = DefaultRouter()
router.register(r'upload_image_viewset', ImageUploadViewSet, basename='upload_image_viewset')
urlpatterns = [
    path('process/', process_image, name='process_image'),
    path('task_status/<str:task_id>', get_task_status, name='task_status'),
    path('', include(router.urls)),

]