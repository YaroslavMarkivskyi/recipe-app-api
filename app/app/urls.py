"""
URL Configuration for the Django Application.

This module defines the URL routing for the application.
The `urlpatterns` list maps URLs to views.

For more information on Django's URL routing, refer to the documentation:
    https://docs.djangoproject.com/en/stable/topics/http/urls/

Examples:
1. Function-based views:
    - Import the view: from my_app import views
    - Add a URL pattern: path('', views.home, name='home')

2. Class-based views:
    - Import the view: from other_app.views import Home
    - Add a URL pattern: path('', Home.as_view(), name='home')

3. Including other URL configurations:
    - Import the include function: from django.urls import include, path
    - Add a URL pattern: path('blog/', include('blog.urls'))
"""

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Admin site URL
    path("admin/", admin.site.urls),
    # API schema endpoint for generating the OpenAPI schema
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    # Swagger UI for API documentation
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    # User-related API endpoints
    path("api/user/", include("user.urls")),
    # Recipe-related API endpoints
    path("api/recipe/", include("recipe.urls")),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
