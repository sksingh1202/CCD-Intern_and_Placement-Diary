from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('',
        auth_views.LoginView.as_view(template_name='diary/login.html', redirect_authenticated_user=True),
        name='login'
    ),
]
