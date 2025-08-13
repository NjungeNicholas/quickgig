from django.db import models
from services.models import Service
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    
class BaseUser(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    location = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)

    # roles
    is_client = models.BooleanField(default=True)
    is_tasker = models.BooleanField(default=False)

    # status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email}"
    
    def save(self, *args, **kwargs):
        # Handle location to always be lowercase
        if self.location:
            self.location = self.location.lower()

        # Handle profile picture
        # If profile picture is empty, assign default picture
        if not self.profile_picture:
            # Ensure default picture path is correct
            default_picture_path = 'profile_pictures/default-avatar.jpg'
            self.profile_picture.name = default_picture_path
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class TaskerProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    skills = models.ManyToManyField(Service, blank=True)

    def __str__(self):
        return f"Profile of {self.user.email}"
    
    class Meta:
        verbose_name = 'Tasker'
        verbose_name_plural = 'Taskers'