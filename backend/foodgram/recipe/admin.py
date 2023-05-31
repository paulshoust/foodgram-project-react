from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from users.models import Subscription

from .models import IngredientPerRecipe, Ingredients, Recipes, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('email', 'username')
    search_fields = ('email', 'first_name', 'last_name')


class IngredientsAdmin(admin.ModelAdmin):
    list_filter = ['name']
    list_display = ['name', 'measurement_unit']

class RecipesIngredientInline(admin.TabularInline):
    model = IngredientPerRecipe
    min_num = 1

class RecipesAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'get_favorited_number']
    list_filter = ['author', 'name', 'tags']
    inlines = [RecipesIngredientInline]

    def get_favorited_number(self, obj):
        return obj.is_favorited.count()
    get_favorited_number.short_description = 'Favorited count'


admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(IngredientPerRecipe)
admin.site.register(Tag)
admin.site.register(Subscription)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
