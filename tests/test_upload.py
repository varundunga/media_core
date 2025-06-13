import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'media_core.settings')

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.image_processor.models import UploadImage

@pytest.mark.django_db
def test_upload_image_model_creation():
    user = User.objects.create_user(username='testuser', password='testpass')
    image_file = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
    upload = UploadImage.objects.create(file=image_file, user=user)
    assert upload.id is not None
    assert upload.file.name.startswith("images/test.jpg")
    assert upload.user == user

@pytest.mark.django_db
def test_image_upload_viewset_authenticated(client):
    user = User.objects.create_user(username='testuser2', password='testpass2')
    client = APIClient()
    client.force_authenticate(user=user)
    image_file = SimpleUploadedFile("test2.jpg", b"file_content", content_type="image/jpeg")
    response = client.post("/image_processor/upload_image_viewset/", {"file": image_file}, format="multipart")
    assert response.status_code == 201
    assert UploadImage.objects.filter(user=user).exists()

@pytest.mark.django_db
def test_image_upload_viewset_unauthenticated():
    client = APIClient()
    image_file = SimpleUploadedFile("test3.jpg", b"file_content", content_type="image/jpeg")
    response = client.post("/image_processor/upload_image_viewset/", {"file": image_file}, format="multipart")
    assert response.status_code == 401