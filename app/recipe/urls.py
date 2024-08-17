"""
URL mappings for the recipe app.

This module sets up URL routing for the recipe application using Django's
DefaultRouter to automatically generate URL patterns for the Recipe, Tag,
and Ingredient view sets.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipe import views

# Initialize the DefaultRouter for generating URL patterns
router = DefaultRouter()
router.register("recipes", views.RecipeViewSet, basename="recipe")
router.register("tags", views.TagViewSet, basename="tag")
router.register("ingredients", views.IngredientViewSet, basename="ingredient")

app_name = "recipe"

urlpatterns = [
    path("", include(router.urls)),
]
