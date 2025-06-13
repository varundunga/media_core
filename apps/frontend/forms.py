from django import forms
from django.contrib.auth.models import User

from .models import UploadFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ["file"]
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': False}),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check content type
            if not file.content_type.startswith('image/'):
                raise forms.ValidationError("Only image files are allowed.")
            # Optionally, check file extension
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
            import os
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError("Unsupported file extension.")
        return file
    
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError('Passwords don\'t match.')
        return cd.get('password2')
