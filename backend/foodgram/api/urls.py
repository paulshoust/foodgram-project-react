from django.urls import include, path, re_path
from rest_framework import routers

from users.views import (CurrentUserView, CustomAuthToken, DeleteTokenView,
                         FollowingListView, UpdatePasswordView, UserViewSet)

from .views import IngredientViewSet, RecipeViewSet, ShoppingList, TagViewSet

router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'users', UserViewSet, basename='user')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('auth/token/login/', CustomAuthToken.as_view(),
         name='obtain_token'),
    path('users/subscriptions/', FollowingListView.as_view(),
         name='subscriptions'),
    path('users/set_password/', UpdatePasswordView.as_view(),
         name='change_password'),
    path('auth/token/logout/', DeleteTokenView.as_view(),
         name='delete_token'),
    path('users/me/', CurrentUserView.as_view(),
         name='current-user'),
    path('recipes/download_shopping_cart/',
         ShoppingList.as_view(), name='shopping_list_download'),
    re_path(r'', include(router.urls)),
]
