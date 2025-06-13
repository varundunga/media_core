from django.contrib import admin

from .models import ImageModel, ImageProcessingResults

admin.site.register(ImageModel)
admin.site.register(ImageProcessingResults)

# Register your models here.
