from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('report/', report_issue, name='report_issue'),
    path('success/<str:complaint_id>/', success, name='success'),
    path('track/', track_issue, name='track_issue'),
    path('public-issues/', public_issues, name='public_issues'),
    path('verify-otp/<int:issue_id>/', verify_otp, name='verify_otp'),

]


