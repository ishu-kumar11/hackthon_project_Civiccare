from django.urls import path
from . import views

urlpatterns = [
    path('', views.authority_dashboard, name='authority_dashboard'),
    path('issues/', views.authority_issue_list, name='authority_issue_list'),
    path('issue/<int:issue_id>/status/', views.update_issue_status, name='update_issue_status'),
    path('issue/<int:issue_id>/fake/', views.mark_issue_fake, name='mark_issue_fake'),
    path('audit-logs/', views.audit_logs, name='audit_logs'),
]
