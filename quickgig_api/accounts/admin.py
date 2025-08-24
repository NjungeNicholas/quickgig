from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import BaseUser, TaskerProfile

# --- Custom forms for creating and changing users ---
class BaseUserCreationForm(forms.ModelForm):
    """Form for creating new users with password1 and password2 confirmation"""
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = BaseUser
        fields = ("email", "username", "is_client", "is_tasker", "is_active", "is_staff")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class BaseUserChangeForm(forms.ModelForm):
    """Form for updating users. Replaces password field with a read-only hash field"""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = BaseUser
        fields = ("email", "username", "password", "is_active", "is_staff", "is_client", "is_tasker")

    def clean_password(self):
        # Regardless of what the user provides, return the initial value
        return self.initial["password"]


# --- Admin class ---
@admin.register(BaseUser)
class CustomUserAdmin(UserAdmin):
    add_form = BaseUserCreationForm
    form = BaseUserChangeForm
    model = BaseUser

    list_display = ("email", "username", "is_client", "is_tasker", "is_active", "is_staff")
    search_fields = ("email", "username")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Personal info", {"fields": ("location", "phone_number", "profile_picture")}),
        ("Roles", {"fields": ("is_client", "is_tasker", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "is_client", "is_tasker", "is_active", "is_staff"),
        }),
    )

@admin.register(TaskerProfile)
class TaskerProfileAdmin(admin.ModelAdmin):
    list_display = ("get_username", "bio", "get_skills", "id")
    search_fields = ("user__email", "user__username", "bio")

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = "Username"

    def get_skills(self, obj):
        return ", ".join([skill.name for skill in obj.skills.all()])
    get_skills.short_description = "Skills"
