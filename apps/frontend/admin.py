from django.contrib import admin
from .models import UploadFile

class UploadFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'user', 'created_at')  # Columns shown in list view
    list_filter = ('user', 'created_at')                 # Sidebar filters
    search_fields = ('file', 'user__username')           # Search box
    date_hierarchy = 'created_at'                        # Date navigation
    ordering = ('-created_at',)    

admin.site.register(UploadFile, UploadFileAdmin)
# Register your models here.
