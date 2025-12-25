from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Issue, UserProfile


# -----------------------------
# Issue Admin
# -----------------------------
@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'status', 'created_at')
    list_filter = ('category', 'status', 'location')
    search_fields = ('title', 'description', 'location')
    ordering = ('-created_at',)


# -----------------------------
# UserProfile Inline (inside User)
# -----------------------------
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0
    verbose_name_plural = 'User Profile'


# -----------------------------
# Custom User Admin
# -----------------------------
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

    # Optional: cleaner user list
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')


# -----------------------------
# Re-register User with profile
# -----------------------------
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
