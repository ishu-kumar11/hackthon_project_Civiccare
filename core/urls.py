from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('report/', report_issue, name='report_issue'),
    path('success/<str:complaint_id>/', success, name='success'),
    path('track/', track_issue, name='track_issue'),
    path('public-issues/', public_issues, name='public_issues'),
    path('verify-otp/<int:issue_id>/', verify_otp, name='verify_otp'),

    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('vote/<int:issue_id>/', vote_issue, name='vote_issue'),
    path('api/pincode/', pincode_lookup, name='pincode_lookup'),

    path('dashboard/', user_dashboard, name='user_dashboard'),
    

    path("map-data/", issue_map_data, name="issue-map-data"),
    path("map/", issue_map_view, name="issue-map"),

]


