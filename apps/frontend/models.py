from django.db import models

# Create your models here.
class UploadFile(models.Model):
    file = models.FileField(upload_to='images/', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='uploads', null=True, blank=True)

    def __str__(self):
        return f"Upload {self.id} - {self.file.name} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    class Meta:
        verbose_name = "Upload File"
        verbose_name_plural = "Upload Files"
        ordering = ['-created_at']  # Order by creation date, newest first