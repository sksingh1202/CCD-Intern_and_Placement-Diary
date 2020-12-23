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
    path('intern_calendar/',
        views.intern_calendar, 
        name='intern_calendar'
    ),
    path('placement_calendar/',
        views.placement_calendar, 
        name='placement_calendar'
    ),
    path('del/<int:item_id>',views.remove,name="del"),
    path('del1/<int:item1_id>',views.remove1,name="del1"),    
    path('companies/<int:year>/',
        views.CompanyListView.as_view(),
        name='company_list'
    ),
    path('companies/filter/',
        views.company_update,
        name='company_update'
    ),
    path('companies/ipfilter/',
        views.company_intern_placement_filter,
        name='company_ipfilter'
    ),
    path('companies/new/',
        views.CompanyCreateView.as_view(),
        name='company_create'
    ),
    path('companies/placement/<slug>/<int:year>/',
        views.CompanyPlacementRemarksListView.as_view(),
        name='company_placement_remarks_list'
    ),
    path('companies/intern/<slug>/<int:year>/',
        views.CompanyInternRemarksListView.as_view(),
        name='company_intern_remarks'
    ),
    path('companies/<slug>/add_hr/',
        views.HRCreateView.as_view(),
        name='create_hr'
    ),
    # path('companies/add_hr/',
    #     views.HRNavCreateView.as_view(),
    #     name='create_nav_hr'
    # ),
    path('companies/<slug>/hrs/',
        views.HRListView.as_view(),
        name='hr_list'
    ),
    path('companies/hrs/',
        views.HRPresentListView.as_view(),
        name='hr_present_list'
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
