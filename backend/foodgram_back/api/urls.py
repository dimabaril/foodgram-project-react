from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import (
    TagViewSet, IngredientViewSet, RecipeViewSet, )

router = DefaultRouter()
# если во вьюхе геткверисет то надо бэйсенейм явно прописывать
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]
