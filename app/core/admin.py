"""
Django admin customizations.

This module defines customizations for the Django admin interface,
including the configuration of admin pages for user management
and the registration of models.

Dependencies:
- django.contrib.admin
- django.contrib.auth.admin.UserAdmin
- django.utils.translation.gettext_lazy
- core.models
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core import models


class UserAdmin(BaseUserAdmin):
    """
    Customize the admin interface for user management.

    This class customizes the admin pages for users,
    including fieldsets, ordering, and displayed fields.
    """

    ordering = ["id"]
    list_display = ["email", "name"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


# Register the User model with the customized UserAdmin
admin.site.register(models.User, UserAdmin)

# Register additional models
admin.site.register(models.Recipe)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)
