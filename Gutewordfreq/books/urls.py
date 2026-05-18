"""
URL routing for books app
Author: Sean Fay
Date: 2026-05-16
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/search-local/', views.search_local, name='search_local'),
    path('api/search-api/', views.search_api_and_fetch, name='search_api'),
    path('api/fetch-manual/', views.fetch_manual_url, name='fetch_manual'),
]