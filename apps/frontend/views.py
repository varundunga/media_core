from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import UploadFileForm, UserRegistrationForm
from .models import UploadFile 
# Create your views here.
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user
            upload.save()
            request.session['last_uploaded_file'] = upload.file.name  # Store the last uploaded file in session
            return render(request, 'upload_success.html', {'form': form})
        else:
            return render(request, 'upload_form.html', {'form': form})
    else:
        form = UploadFileForm()
    return render(request, 'upload_form.html', {'form': form})

@login_required
def user_dashboard(request):
    uploads = UploadFile.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_dashboard.html', {'uploads': uploads})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('upload_file')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        print(form.errors)
        if form.is_valid():
            print("Form is valid")
            user = form.get_user()
            login(request, user)
            return redirect('user_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            return render(request, 'password_reset_done.html')
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout
