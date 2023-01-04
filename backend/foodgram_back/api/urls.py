from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import (
    TagViewSet, IngredientViewSet, RecipeViewSet, )
    # Recipe_IngredientsViewSet, SubscriptionViewSet, )  # UserViewSet)

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
# если во вьюхе геткверисет то надо бэйсенейм явно прописывать
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
#router.register(
#    'recipe_ingredients', Recipe_IngredientsViewSet,
#    basename='recipe_ingredients')
# router.register('subscriptions', SubscriptionViewSet, basename='subscriptions')


urlpatterns = [
    path('', include(router.urls)),
]
