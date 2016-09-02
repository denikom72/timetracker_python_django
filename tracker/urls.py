from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('history/', views.time_history, name='time_history'),
    path('team/', views.team_timesheet, name='team_timesheet'),
    path('export/monthly_timesheet/', views.export_monthly_timesheet, name='export_monthly_timesheet'),
    path('user/<int:user_id>/timesheet/', views.view_user_timesheet, name='view_user_timesheet'),
    path('time_entry/<int:entry_id>/edit/', views.edit_time_entry, name='edit_time_entry'),
    path('time_entry/add/', views.add_time_entry, name='add_time_entry'),
]