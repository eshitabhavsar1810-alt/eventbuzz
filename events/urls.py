from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.home, name='home'),
    path('colleges/', views.colleges_page, name='colleges'),
    path('events/', views.events_page, name='events'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register_user, name='register'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('about/', views.about, name='about'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('event/<int:pk>/register/', views.event_register, name='event_register'),
    path('event/<int:pk>/review/', views.event_review, name='event_review'),
    path('my-events/', views.my_events, name='my_events'),

    # Admin panel (separate from Django admin site)
    path('admin-panel/signup/', views.admin_signup, name='admin_signup'),
    path('admin-panel/login/', views.admin_login, name='admin_login'),
    path('admin-panel/logout/', views.admin_logout, name='admin_logout'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/events/new/', views.admin_event_create, name='admin_event_create'),
    path('admin-panel/events/<int:pk>/edit/', views.admin_event_update, name='admin_event_update'),
    path('admin-panel/events/<int:pk>/delete/', views.admin_event_delete, name='admin_event_delete'),
    path('admin-panel/registrations/', views.admin_registrations, name='admin_registrations'),
    path('admin-panel/registrations/export/', views.admin_registrations_export, name='admin_registrations_export'),
]
