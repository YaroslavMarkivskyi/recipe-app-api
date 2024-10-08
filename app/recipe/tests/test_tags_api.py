"""
Tests for the Tags API.

This module contains tests for the Tags API,
including authentication checks,
CRUD operations,
and filtering of tags.

Dependencies:
- decimal.Decimal
- django.contrib.auth.get_user_model
- django.urls.reverse
- django.test.TestCase
- rest_framework.status
- rest_framework.test.APIClient
- core.models.Tag, Recipe
- recipe.serializers.TagSerializer
"""

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, Recipe
from recipe.serializers import TagSerializer


TAGS_URL = reverse("recipe:tag-list")


def detail_url(tag_id):
    """
    Create and return the URL for a specific tag detail.

    Args:
        tag_id (int): The ID of the tag.

    Returns:
        str: The URL for the tag detail.
    """
    return reverse("recipe:tag-detail", args=[tag_id])


def create_user(email="user@example.com", password="testpass123"):
    """
    Create and return a new user.

    Args:
        email (str): The email address of the user.
        password (str): The password for the user.

    Returns:
        User: The created user instance.
    """
    return get_user_model().objects.create_user(email=email, password=password)


class PublicTagsApiTests(TestCase):
    """
    Tests for unauthenticated API requests to the Tags API.
    """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test that authentication is required for retrieving tags.
        """
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """
    Tests for authenticated API requests to the Tags API.
    """

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """
        Test retrieving a list of tags for an authenticated user.
        """
        Tag.objects.create(user=self.user, name="Vegan")
        Tag.objects.create(user=self.user, name="Dessert")

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """
        Test that the list of tags is limited to the authenticated user.
        """
        user2 = create_user(email="user2@example.com")
        Tag.objects.create(user=user2, name="Fruity")
        tag = Tag.objects.create(user=self.user, name="Comfort Food")

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], tag.name)
        self.assertEqual(res.data[0]["id"], tag.id)

    def test_update_tag(self):
        """
        Test updating a tag for the authenticated user.
        """
        tag = Tag.objects.create(user=self.user, name="After Dinner")

        payload = {"name": "Dessert"}
        url = detail_url(tag.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload["name"])

    def test_delete_tag(self):
        """
        Test deleting a tag for the authenticated user.
        """
        tag = Tag.objects.create(user=self.user, name="Breakfast")

        url = detail_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = Tag.objects.filter(user=self.user)
        self.assertFalse(tags.exists())

    def test_filter_tags_assigned_to_recipes(self):
        """
        Test listing tags that are assigned to recipes.
        """
        tag1 = Tag.objects.create(user=self.user, name="Breakfast")
        tag2 = Tag.objects.create(user=self.user, name="Lunch")
        recipe = Recipe.objects.create(
            title="Green Eggs on Toast",
            time_minutes=10,
            price=Decimal("2.50"),
            user=self.user,
        )
        recipe.tags.add(tag1)

        res = self.client.get(TAGS_URL, {"assigned_only": 1})

        s1 = TagSerializer(tag1)
        s2 = TagSerializer(tag2)
        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_filtered_tags_unique(self):
        """
        Test that filtered tags return a unique list.
        """
        tag = Tag.objects.create(user=self.user, name="Breakfast")
        Tag.objects.create(user=self.user, name="Dinner")
        recipe1 = Recipe.objects.create(
            title="Pancakes",
            time_minutes=5,
            price=Decimal("5.00"),
            user=self.user,
        )
        recipe2 = Recipe.objects.create(
            title="Porridge",
            time_minutes=3,
            price=Decimal("2.00"),
            user=self.user,
        )
        recipe1.tags.add(tag)
        recipe2.tags.add(tag)

        res = self.client.get(TAGS_URL, {"assigned_only": 1})

        self.assertEqual(len(res.data), 1)
