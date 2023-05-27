from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipe.models import IngredientPerRecipe, Ingredients, Recipes, Tag
from users.serializers import UserSerializer

from .validators import positive_value_validator

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredients."""

    class Meta:
        model = Ingredients
        fields = '__all__'


class IngredientPerRecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for IngredientPerRecipe model.

    (records amount of ingredients per recipe).
    """

    id = serializers.ReadOnlyField(source='ingredient.id', read_only=True)
    name = serializers.ReadOnlyField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')
    amount = serializers.IntegerField(validators=[positive_value_validator])

    class Meta:
        model = IngredientPerRecipe
        fields = ['id', 'name', 'measurement_unit', 'amount']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model."""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientRecipeCreateSerializer(serializers.ModelSerializer):
    """Serializer to add Ingredient amount along with new recipe."""

    amount = serializers.IntegerField(
        write_only=True, validators=[positive_value_validator])
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Ingredients
        fields = [
            'id',
            'amount'
        ]


class RecipeUpdateSerializer(serializers.ModelSerializer):
    """Recipe to handle creation/updates of recipes."""

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=False,
    )
    ingredients = IngredientRecipeCreateSerializer(many=True)
    image = Base64ImageField()
    name = serializers.CharField()
    text = serializers.CharField()
    cooking_time = serializers.CharField(validators=[positive_value_validator])

    class Meta:
        model = Recipes
        fields = ['author', 'tags', 'ingredients',
                  'image', 'name', 'text', 'cooking_time']

    def create(self, validated_data):
        """Handle creation of new recipes."""
        ingredients_data = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipes.objects.create(**validated_data)

        for ingredient_data in ingredients_data:

            ingredient = ingredient_data.get('id')
            amount = ingredient_data.get('amount')
            ingredient_id = Ingredients.objects.get(id=ingredient)
            IngredientPerRecipe.objects.create(
                recipe=recipe, ingredient=ingredient_id, amount=amount)
        recipe.tags.set(tags)
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        """Handle updates of existing recipes."""
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        instance.tags.clear()
        instance.ingredients.clear()
        for tag in tags_data:
            tag_id = tag.id
            tag_object = get_object_or_404(Tag, id=tag_id)
            instance.tags.add(tag_object)
        for ingredient in ingredients_data:
            ingredient_id = ingredient.get('id')
            amount = ingredient.get('amount')
            ingredient_object = get_object_or_404(
                Ingredients, id=ingredient_id)
            instance.ingredients.add(
                ingredient_object,
                through_defaults={'amount': amount}
            )
        instance.save()
        return instance

    def to_representation(self, instance):
        """Handle API response after successful operation."""
        serializer = RecipeSerializer(
            instance,
            context=self.context
        )
        return serializer.data


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer to list recipes."""

    ingredients = IngredientPerRecipeSerializer(
        source='ingredientperrecipe_set', many=True, read_only=True)

    tags = TagSerializer(many=True, read_only=False)
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    def get_is_favorited(self, obj):
        """Handle adding recipes to favorites."""
        user = self.context['request'].user
        if isinstance(obj, Recipes):
            return obj.is_favorited.filter(id=user.id).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        """Handle adding recipes to the shopping cart."""
        user = self.context['request'].user
        if isinstance(obj, Recipes):
            return obj.is_in_shopping_cart.filter(id=user.id).exists()
        return False

    def get_image(self, obj):
        """Return absolute image's url in the API response."""
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

    class Meta:
        model = Recipes
        fields = ['id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time']
