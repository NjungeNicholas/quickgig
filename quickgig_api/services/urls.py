from django.urls import path, include
from .views import CategoryListView, ServiceListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('services/', ServiceListView.as_view(), name='services'),
]

"""
Services API Endpoints
======================

Categories
----------
- GET    /api/services/categories/
    List all service categories (public).

Services
--------
- GET    /api/services/services/
    List all services (public).

Notes
-----
- Only admin users can perform write operations (POST, PUT, PATCH, DELETE) if those endpoints are added.
- Currently, only listing (GET) is available for both categories and services.
- Permissions are enforced so that anyone can view, but only admins can modify (if implemented).
"""