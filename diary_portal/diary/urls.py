from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',
        auth_views.LoginView.as_view(template_name='diary/login.html', redirect_authenticated_user=True),
        name='login'
    ),
    path('logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    path('companies/',
        views.CompanyListView.as_view(),
        name='company_list'
    ),
    path('companies/new/',
        views.CompanyCreateView.as_view(),
        name='company_create'
    ),
    path('companies/placement/<slug>/',
        views.CompanyPlacementRemarksListView.as_view(),
        name='company_placement_remarks_list'
    ),
    path('companies/intern/<slug>/',
        views.CompanyInternRemarksListView.as_view(),
        name='company_intern_remarks'
    ),
    path('companies/<slug>/add_hr',
        views.HRCreateView.as_view(),
        name='create_hr'
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
