"""
Views for the user API.
"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to create a new user.

        Args:
            request (HttpRequest):
            The request object containing user data.

        Returns:
            Response: The response object
            containing the newly created user data.
        """
        return self.create(request, *args, **kwargs)


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for the user."""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to create an authentication token.

        Args:
            request (HttpRequest):
            The request object containing user credentials.

        Returns:
            Response: The response object containing the auth token.
        """
        return super().post(request, *args, **kwargs)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """
        Retrieve and return the authenticated user.

        Returns:
            User: The authenticated user instance.
        """
        return self.request.user
