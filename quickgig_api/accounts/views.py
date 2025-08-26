from rest_framework import generics, status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import BaseUser, TaskerProfile
from .serializers import (
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    BecomeTaskerSerializer,
    TaskerProfileSerializer,
    TaskerProfileUpdateSerializer,
    PasswordChangeSerializer
)
from .permissions import (
    IsOwnerOrReadOnly,
    IsTaskerOwnerOrReadOnly,
    IsOwner,
    IsAuthenticatedOrCreateOnly
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """
    View for user registration
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate tokens for the newly created user
            refresh = RefreshToken.for_user(user)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'is_tasker': user.is_tasker,
                'is_client': user.is_client,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom login view with JWT tokens
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            # Get user info to add to response
            email = request.data.get('email')
            user = User.objects.get(email=email)
            
            # Add user info to the existing token response
            response.data.update({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'is_tasker': user.is_tasker,
                    'is_client': user.is_client,
                }
            })
        
        return response


class LogoutView(APIView):
    """
    View for user logout (blacklist refresh token)
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Invalid token or token already blacklisted'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user CRUD operations
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrCreateOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserProfileSerializer

    def get_object(self):
        """
        Override to get current user for 'me' endpoint
        """
        if self.kwargs.get('pk') == 'me':
            return self.request.user
        return super().get_object()

    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
        Get or update current user's profile
        """
        user = request.user
        
        if request.method == 'GET':
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            partial = request.method == 'PATCH'
            serializer = UserUpdateSerializer(user, data=request.data, partial=partial, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            # Return updated profile
            response_serializer = UserProfileSerializer(user)
            return Response({
                'message': 'Profile updated successfully',
                'user': response_serializer.data
            })

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def become_tasker(self, request):
        """
        Convert current user to a tasker
        """
        user = request.user
        
        if user.is_tasker:
            return Response({
                'message': 'User is already a tasker'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BecomeTaskerSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()
        
        # Get the created tasker profile (signal will create it automatically)
        tasker_profile = user.taskerprofile
        profile_serializer = TaskerProfileSerializer(tasker_profile)
        
        return Response({
            'message': 'Successfully became a tasker',
            'tasker_profile': profile_serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        """
        Change user password
        """
        serializer = PasswordChangeSerializer(data=request.data, 
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'message': 'Password changed successfully'
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def delete_account(self, request):
        """
        Delete current user's account
        """
        user = request.user
        user.delete()
        
        return Response({
            'message': 'Account deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


class TaskerProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for tasker profile operations
    """
    queryset = TaskerProfile.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsTaskerOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return TaskerProfileUpdateSerializer
        return TaskerProfileSerializer

    def get_queryset(self):
        """
        Optionally filter taskers by skills or location
        """
        queryset = TaskerProfile.objects.select_related('user').prefetch_related('skills')
        
        # Filter by skills
        skills = self.request.query_params.get('skills')
        if skills:
            skill_ids = [int(x) for x in skills.split(',') if x.isdigit()]
            queryset = queryset.filter(skills__id__in=skill_ids).distinct()
        
        # Filter by location
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(user__location__icontains=location.lower())
        
        return queryset

    @action(detail=False, methods=['get', 'put', 'patch'], 
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
        Get or update current user's tasker profile
        """
        user = request.user
        
        if not user.is_tasker:
            return Response({
                'error': 'User is not a tasker'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            tasker_profile = user.taskerprofile
        except TaskerProfile.DoesNotExist:
            return Response({
                'error': 'Tasker profile not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = TaskerProfileSerializer(tasker_profile)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            partial = request.method == 'PATCH'
            serializer = TaskerProfileUpdateSerializer(
                tasker_profile, 
                data=request.data, 
                partial=partial
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            # Return updated profile
            response_serializer = TaskerProfileSerializer(tasker_profile)
            return Response({
                'message': 'Tasker profile updated successfully',
                'tasker_profile': response_serializer.data
            })


# Additional view for public tasker listing (without authentication required)
class PublicTaskerListView(generics.ListAPIView):
    """
    Public view to list all taskers (read-only)
    """
    queryset = TaskerProfile.objects.select_related('user').prefetch_related('skills')
    serializer_class = TaskerProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Filter taskers by skills or location
        """
        queryset = super().get_queryset()
        
        # Filter by skills
        skills = self.request.query_params.get('skills')
        if skills:
            skill_ids = [int(x) for x in skills.split(',') if x.isdigit()]
            queryset = queryset.filter(skills__id__in=skill_ids).distinct()
        
        # Filter by location
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(user__location__icontains=location.lower())

        # Filter by username
        username = self.request.query_params.get('username')
        if username:
            queryset = queryset.filter(user__username__icontains=username.lower())

        return queryset


class TaskerDetailView(generics.RetrieveAPIView):
    """
    Public view to get a specific tasker's details
    """
    queryset = TaskerProfile.objects.select_related('user').prefetch_related('skills')
    serializer_class = TaskerProfileSerializer
    permission_classes = [permissions.AllowAny]