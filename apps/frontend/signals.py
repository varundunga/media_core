from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UploadFile

@receiver(post_save, sender=UploadFile)
def process_uploaded_file(instance, **kwargs):
    # Placeholder for processing logic
    print(f"Processing file: {instance.file.name}")