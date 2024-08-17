"""
Database models for the application.

This module defines the database models for the application,
including user management, recipes, tags, and ingredients.
It also includes custom file path generation for recipe images.

Dependencies:
- uuid
- os
- django.conf.settings
- django.db.models
- django.contrib.auth.models.AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
"""

import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


def recipe_image_file_path(instance, filename):
    """
    Generate file path for new recipe image.

    Args:
        instance: The instance of the model (Recipe)
        that the image is related to.
        filename: The original file name of the uploaded image.

    Returns:
        str: The file path for the new recipe image.
    """
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"

    return os.path.join("uploads", "recipe", filename)


class UserManager(BaseUserManager):
    """
    Manager for handling user operations.

    Provides methods to create regular users and superusers.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a new user with an email address.

        Args:
            email (str): The email address of the user.
            password (str, optional): The password for the user.
            **extra_fields: Additional fields for the user.

        Returns:
            User: The created user instance.
        """
        if not email:
            raise ValueError("Users must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Create and return a new superuser with admin privileges.

        Args:
            email (str): The email address of the superuser.
            password (str): The password for the superuser.

        Returns:
            User: The created superuser instance.
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model representing a user in the system.

    Inherits from AbstractBaseUser and PermissionsMixin
    to provide user authentication and permission features.
    """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Recipe(models.Model):
    """
    Recipe model representing a cooking recipe.

    Includes fields for
    title,
    description,
    cooking time,
    price, and associated tags and ingredients.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField("Tag")
    ingredients = models.ManyToManyField("Ingredient")
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    Tag model for filtering recipes.

    Tags are used to categorize recipes.
    """

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Ingredient model representing an
    ingredient used in recipes.

    Ingredients are associated with
    recipes through many-to-many relationships.
    """

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.name
