from django.db import models

# Create your models here.
class ImageModel(models.Model):
    guid = models.CharField(max_length=36, unique=True)
    file_name = models.CharField(max_length=255)
    blob_bucket = models.CharField(max_length=255)
    blob_file_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ['-created_at']  # Order by creation date, newest first

class ImageProcessingResults(models.Model):
    image = models.ForeignKey(ImageModel, on_delete=models.CASCADE)
    blob_bucket = models.CharField(max_length=255, default='thumbnails')
    blob_file_name = models.CharField(max_length=255, blank=True, null=True)
    result = models.CharField(max_length=255)
    error = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    