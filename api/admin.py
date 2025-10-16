from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Organization, User, File, Download


# ----------------------------
# Organization Admin
# ----------------------------
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


# ----------------------------
# User Admin
# ----------------------------
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Organization", {"fields": ("organization",)}),
    )
    list_display = ("username", "email", "organization", "is_staff", "is_superuser")
    list_filter = ("organization", "is_staff", "is_superuser")


admin.site.register(User, UserAdmin)


# ----------------------------
# File Admin
# ----------------------------
@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "organization", "uploaded_by", "uploaded_at", "download_count")
    list_filter = ("organization", "uploaded_at")
    search_fields = ("file", "uploaded_by__username")

    def download_count(self, obj):
        return obj.downloads.count()
    download_count.short_description = "Downloads"


# ----------------------------
# Download Admin
# ----------------------------
@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "user", "downloaded_at")
    list_filter = ("file", "user", "downloaded_at")
    search_fields = ("file__file", "user__username")
