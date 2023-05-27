from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import RecipeSerializer, UserSerializer
from recipe.models import Recipes

from .models import Subscription
from .serializers import ChangePasswordSerializer, CurrentUserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Handle user-related actions."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['POST', 'DELETE'])
    def subscribe(self, request, pk=None):
        """Handle subscription-related actions."""
        user = request.user
        author = self.get_object()
        if request.method == 'POST':
            if Subscription.objects.filter(user=user, author=author).exists():
                return Response(
                    {'errors': 'Already subscribed'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if user == author:
                return Response(
                    {'errors': 'Cannot subscribe to yourself'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            Subscription.objects.create(user=user, author=author)
            recipes = author.recipes.all()

            user_serializer = UserSerializer(
                author, context={'request': request})
            recipes_serializer = RecipeSerializer(
                recipes, context={'request': request}, many=True)

            selected_fields = ['id', 'name', 'image', 'cooking_time']
            recipes_data = recipes_serializer.data
            selected_recipes_data = [
                {field: recipe_data[field] for field in selected_fields}
                for recipe_data in recipes_data
            ]
            data = {
                'email': user_serializer.data['email'],
                'id': user_serializer.data['id'],
                'username': user_serializer.data['username'],
                'first_name': user_serializer.data['first_name'],
                'last_name': user_serializer.data['last_name'],
                'recipes': selected_recipes_data,
                'recipes_count': recipes.count()
            }
            return Response(data=data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not Subscription.objects.filter(
                    user=user, author=author).exists():
                return Response(
                    {'errors': 'Subscription not found'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Subscription.objects.filter(user=user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class FollowingListView(APIView):
    """Handle subscription-related actions."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get all followed authors."""
        user = request.user
        subscriptions = Subscription.objects.filter(user=user)

        subscribed_authors_data = []
        for subscription in subscriptions:
            author = subscription.author
            author_data = {
                'email': author.email,
                'id': author.id,
                'username': author.username,
                'first_name': author.first_name,
                'last_name': author.last_name,
                'is_subscribed': True,
            }
            recipes = Recipes.objects.filter(author=author)
            recipe_data = []
            for recipe in recipes:
                recipe_data.append({
                    'id': recipe.id,
                    'name': recipe.name,
                    'image': recipe.image.url,
                    'cooking_time': recipe.cooking_time,
                })
            author_data['recipes'] = recipe_data
            author_data['recipes_count'] = len(recipe_data)
            subscribed_authors_data.append(author_data)

        data = {
            'results': subscribed_authors_data,
        }
        return Response(data=data, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    """Handle 'me' requests."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Reassign method to ensure correct response structure."""
        user = request.user
        serializer = CurrentUserSerializer(user)
        return Response(serializer.data)


class UpdatePasswordView(generics.UpdateAPIView):
    """Handle password change."""

    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)
    allowed_methods = ['POST']

    def get_object(self, queryset=None):
        """Obtain User instance based on credentials."""
        return self.request.user

    def post(self, request, *args, **kwargs):
        """Create a new password."""
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            current_password = serializer.data.get("current_password")
            new_password = serializer.data.get("new_password")

            if not self.object.check_password(current_password):
                return Response(
                    {"current_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            self.object.set_password(new_password)
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    """Handle token requests."""

    def post(self, request, *args, **kwargs):
        """Request a new token."""
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.get(email=email)
        username = user.username

        if email and password:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
        return Response({'error': 'Invalid name/password'}, status=400)


class DeleteTokenView(APIView):
    """Handle token deletion."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Delete the token."""
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response({"null"}, status=status.HTTP_204_NO_CONTENT)
