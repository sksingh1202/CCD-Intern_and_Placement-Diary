"""diary_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from diary import views as diary_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('diary.urls')),
    path('intern_calendar/',diary_views.intern_calendar,name='intern_calendar'),
    path('placement_calendar/',diary_views.placement_calendar,name='placement_calendar'),
]

handler404 = 'diary.views.error_404_view'
