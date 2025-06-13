from django.urls import path, include
from apps.frontend import views
urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
]