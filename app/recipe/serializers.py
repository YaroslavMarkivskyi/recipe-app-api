"""
Serializers for the recipe APIs.

This module contains serializers for Recipe, Tag, and Ingredient models.
It includes serializers for creating, updating, and viewing recipe details,
as well as handling image uploads.
"""

from rest_framework import serializers

from core.models import Recipe, Tag, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for ingredients.

    This serializer is used for representing ingredients in the API responses
    and for deserializing ingredient data for API requests.
    """

    class Meta:
        model = Ingredient
        fields = ["id", "name"]
        read_only_fields = ["id"]


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for tags.

    This serializer is used for representing tags in the API responses
    and for deserializing tag data for API requests.
    """

    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for recipes.

    This serializer handles the representation and deserialization of recipes,
    including their associated tags and ingredients.
    """

    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "time_minutes",
            "price",
            "link",
            "tags",
            "ingredients"
            ]
        read_only_fields = ["id"]

    def _get_or_create_tags(self, tags, recipe):
        """
        Handle getting or creating tags as needed.

        Args:
            tags (list): List of tags data to be processed.
            recipe (Recipe): Recipe instance to which tags are to be added.
        """
        auth_user = self.context["request"].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredients(self, ingredients, recipe):
        """
        Handle getting or creating ingredients as needed.

        Args:
            ingredients (list): List of ingredients data to be processed.
            recipe (Recipe): Recipe instance
            to which ingredients are to be added.
        """
        auth_user = self.context["request"].user
        for ingredient in ingredients:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient,
            )
            recipe.ingredients.add(ingredient_obj)

    def create(self, validated_data):
        """
        Create a new recipe instance.

        Args:
            validated_data (dict): Data validated for creating a recipe.

        Returns:
            Recipe: The newly created recipe instance.
        """
        tags = validated_data.pop("tags", [])
        ingredients = validated_data.pop("ingredients", [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        """
        Update an existing recipe instance.

        Args:
            instance (Recipe): The recipe instance to be updated.
            validated_data (dict): Data validated for updating the recipe.

        Returns:
            Recipe: The updated recipe instance.
        """
        tags = validated_data.pop("tags", None)
        ingredients = validated_data.pop("ingredients", None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """
    Serializer for recipe detail view.

    This serializer extends the RecipeSerializer to include additional fields
    for detailed recipe view.
    """

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description", "image"]


class RecipeImageSerializer(serializers.ModelSerializer):
    """
    Serializer for uploading images to recipes.

    This serializer is used for handling image uploads for recipes.
    """

    class Meta:
        model = Recipe
        fields = ["id", "image"]
        read_only_fields = ["id"]
        extra_kwargs = {"image": {"required": True}}
