from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserRegistrationView,
    CustomTokenObtainPairView,
    LogoutView,
    UserViewSet,
    TaskerProfileViewSet,
    PublicTaskerListView,
    TaskerDetailView
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'tasker-profiles', TaskerProfileViewSet, basename='tasker-profiles')

urlpatterns = [
    # Authentication URLs
    path('auth/register/', UserRegistrationView.as_view(), name='user-register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='user-login'),
    path('auth/logout/', LogoutView.as_view(), name='user-logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
        
    # Public tasker URLs (no authentication required)
    path('public/taskers/', PublicTaskerListView.as_view(), name='public-taskers'),
    path('public/taskers/<int:pk>/', TaskerDetailView.as_view(), name='public-tasker-detail'),
    
    # Include router URLs
    path('', include(router.urls)),
]

"""
API Endpoints Summary:

AUTHENTICATION:
- POST /auth/register/ - User registration
- POST /auth/login/ - User login (get JWT tokens)
- POST /auth/logout/ - User logout (blacklist refresh token)
- POST /auth/token/refresh/ - Refresh access token

USER MANAGEMENT:
- GET /users/me/ - Get current user profile
- PUT /users/me/ - Update current user profile (full update)
- PATCH /users/me/ - Update current user profile (partial update)
- POST /users/me/become_tasker/ - Convert user to tasker
- POST /users/me/change_password/ - Change user password
- DELETE /users/me/delete_account/ - Delete user account
- GET /users/{id}/ - Get specific user profile (read-only for others)

TASKER PROFILES:
- GET /tasker-profiles/ - List all tasker profiles (with filtering by skills, location)
- POST /tasker-profiles/ - Create tasker profile (if not using become_tasker)
- GET /tasker-profiles/{id}/ - Get specific tasker profile
- PUT /tasker-profiles/{id}/ - Update tasker profile (only owner)
- PATCH /tasker-profiles/{id}/ - Partial update tasker profile (only owner)
- DELETE /tasker-profiles/{id}/ - Delete tasker profile (only owner)
- GET /tasker-profiles/me/ - Get current user's tasker profile
- PUT /tasker-profiles/me/ - Update current user's tasker profile
- PATCH /tasker-profiles/me/ - Partial update current user's tasker profile

PUBLIC ENDPOINTS (No authentication required):
- GET /public/taskers/ - List all taskers (with filtering)
- GET /public/taskers/{id}/ - Get specific tasker details

FILTERING PARAMETERS:
- ?skills=1,2,3 - Filter taskers by skill IDs
- ?location=nairobi - Filter taskers by location
- ?username=johnsmith - Filter tasker by username
"""