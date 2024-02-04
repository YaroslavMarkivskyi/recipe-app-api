"""
Serializers for the recipe APIs
"""
from rest_framework import serializers

from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']
