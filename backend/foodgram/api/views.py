from django.http import HttpResponse
from recipe.models import IngredientPerRecipe, Ingredients, Recipes, Tag
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAuthorOrAdmin
from .serializers import (IngredientPerRecipeSerializer, IngredientSerializer,
                          RecipeSerializer, RecipeUpdateSerializer,
                          TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet for Recipe model."""

    queryset = Recipes.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    ingredient = IngredientPerRecipeSerializer

    def get_queryset(self):
        """Set additional query line parameters."""
        queryset = super().get_queryset()
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')
        author = self.request.query_params.get('author')
        tags = self.request.query_params.get('tags')

        if is_favorited == '1':
            queryset = queryset.filter(is_favorited=True)

        if is_in_shopping_cart == '1':
            queryset = queryset.filter(is_in_shopping_cart=True)

        if author:
            queryset = queryset.filter(author=author)

        if tags:
            queryset = queryset.filter(tag__slug=tags)

        return queryset

    def get_permissions(self):
        """Set permissions for Recipe-related actions."""
        if self.action == 'destroy' or self.action == 'partial_update':
            permission_classes = [IsAuthorOrAdmin]
        elif self.request.method == 'POST':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """Specify a specific Serializer for POST requests."""
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipeUpdateSerializer

    def perform_create(self, serializer):
        """Create a new recipe based on serializer response."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Update a recipe based on serializer response."""
        serializer.save()

    @action(detail=True, methods=['POST', 'DELETE'], url_path='favorite')
    def favorite(self, request, pk=None):
        """Handle favorite-related actions."""
        recipe = self.get_object()
        user = request.user
        if request.method == 'POST':

            if user in recipe.is_favorited.all():
                return Response(
                    {'errors': 'The recipe is already in favorites'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            recipe.is_favorited.add(user)
            serializer = RecipeSerializer(
                recipe, context={'request': request})
            data = {
                'id': serializer.data['id'],
                'name': serializer.data['name'],
                'image': serializer.data['image'],
                'cooking_time': serializer.data['cooking_time']
            }
            return Response(data=data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':

            if user not in recipe.is_favorited.all():
                return Response(
                    {'errors': 'No such recipe in the favorites'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            recipe.is_favorited.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST', 'DELETE'], url_path='shopping_cart')
    def shopping_cart(self, request, pk=None):
        """Handle actions with shopping cart."""
        recipe = self.get_object()
        user = request.user
        if request.method == 'POST':
            if user in recipe.is_in_shopping_cart.all():
                return Response(
                    {'errors': 'The recipe is already in the shopping cart'},
                    status=status.HTTP_400_BAD_REQUEST)
            recipe.is_in_shopping_cart.add(user)
            serializer = RecipeSerializer(
                recipe, context={'request': request})
            data = {
                'id': serializer.data['id'],
                'name': serializer.data['name'],
                'image': serializer.data['image'],
                'cooking_time': serializer.data['cooking_time']
            }
            return Response(data=data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if user not in recipe.is_in_shopping_cart.all():
                return Response(
                    {'errors': 'Cannot remove, no such recipe in the cart'},
                    status=status.HTTP_400_BAD_REQUEST)
        recipe.is_in_shopping_cart.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(viewsets.ModelViewSet):
    """Handle Ingredient-related actions."""

    queryset = Ingredients.objects.all()
    pagination_class = None
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )


class TagViewSet(viewsets.ModelViewSet):
    """Handle Tag-related actions."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class ShoppingList(APIView):
    """Handle Shopping list printing."""

    def get(self, request, *args, **kwargs):
        """Get all relevant recipes and compile a list."""
        recipes = Recipes.objects.filter(is_in_shopping_cart=True)
        ingredient_list = {}
        recipe_list = []

        for recipe in recipes:
            ingredients = IngredientPerRecipe.objects.filter(
                recipe=recipe)
            recipe_list.append(recipe.name)
            for ingredient in ingredients:
                ingredient_name = ingredient.ingredient
                ingredient_amount = ingredient.amount
                if ingredient_name in ingredient_list:
                    ingredient_list[ingredient_name] += ingredient_amount
                else:
                    ingredient_list[ingredient_name] = ingredient_amount
        final_list = "Shopping list for ' + ',' '.join(recipe_list) + '\n"
        for ingredient, amount in ingredient_list.items():
            ingredient_unit = Ingredients.objects.get(
                name=ingredient).measurement_unit
            final_list += (f'{ingredient} ({ingredient_unit}) - {amount}\n')
        content = final_list
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.txt"'
        )

        return response
