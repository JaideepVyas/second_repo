from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import User
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'city', 'profile_picture_thumbnail')
    list_filter = ('country', 'state', 'city')
    search_fields = ('user__username', 'user__email', 'phone', 'city')
    readonly_fields = ('profile_picture_thumbnail', 'user')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('phone',)
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'zip_code', 'country')
        }),
        ('Profile Picture', {
            'fields': ('profile_picture', 'profile_picture_thumbnail')
        }),
    )
    
    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'
    
    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'
    
    def profile_picture_thumbnail(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 5px;" />',
                obj.profile_picture.url
            )
        return "No Image"
    
    profile_picture_thumbnail.short_description = 'Profile Picture'
    
    def has_add_permission(self, request):
        # Prevent direct creation of UserProfile through admin
        # Users should be created through the User model
        return False


# Customize the User admin to show profile information
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fields = ('phone', 'address_line1', 'address_line2', 'city', 'state', 'zip_code', 'country', 'profile_picture')
    extra = 0


# Unregister the default User admin and create a custom one
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    inlines = [UserProfileInline]
    
    fieldsets = (
        ('Login Credentials', {
            'fields': ('username', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )