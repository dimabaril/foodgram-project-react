from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Subscription, Tag)
from users.models import User
from .filters import RecipeFilter
from .pagination import Page6PageNumberPagination
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (IngredientSerializer, RecipeSerializer,
                          RecipeWriteSerializer, ShortRecipeSerializer,
                          SubscriptionSerializer, TagSerializer)


class CustomUserViewSet(UserViewSet):
    pagination_class = Page6PageNumberPagination
    permission_classes = (AllowAny, )

    def get_queryset(self):
        return User.objects.all()

    @action(detail=True, methods=['post', 'delete', ],
            permission_classes=(IsAuthenticated, ))
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            if user == author:
                return Response({
                    'errors': 'Вы не можете подписываться на себя'
                }, status=status.HTTP_400_BAD_REQUEST)
            if Subscription.objects.filter(user=user, author=author).exists():
                return Response({
                    'errors': 'Вы уже подписаны на данного пользователя'
                }, status=status.HTTP_400_BAD_REQUEST)
            subscription = Subscription.objects.create(
                user=user, author=author)
            serializer = SubscriptionSerializer(
                subscription, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        subscription = Subscription.objects.filter(user=user, author=author)
        if subscription.exists():
            subscription.delete()
            return Response(
                'successfully deleted', status=status.HTTP_204_NO_CONTENT)
        return Response({
                "errors": "Ошибка удаления, вы не подписаны"
                }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', ],
            permission_classes=(IsAuthenticated, ))
    def subscriptions(self, request):
        user = request.user
        subscriptions = Subscription.objects.filter(user=user)
        pages = self.paginate_queryset(subscriptions)
        serializer = SubscriptionSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly, )


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    permission_classes = (IsAdminOrReadOnly, )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    # serializer_class = RecipeSerializer
    pagination_class = Page6PageNumberPagination
    permission_classes = (IsOwnerOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeWriteSerializer

    def add_delete(self, model, request, pk):
        if request.method == 'POST':
            obj, get_status = model.objects.get_or_create(
                recipe_id=pk, user=request.user)
            if get_status:
                serializer = ShortRecipeSerializer(Recipe.objects.get(id=pk))
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
            return Response({
                "errors": "Ошибка добавления, объект уже в базе."
                }, status=status.HTTP_400_BAD_REQUEST)
        obj = model.objects.filter(recipe_id=pk, user=request.user)
        if obj.exists():
            obj.delete()
            return Response(
                'successfully deleted', status=status.HTTP_204_NO_CONTENT)
        return Response({
                "errors": "Ошибка удаления, объекта нет в базе."
                }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete', ],
            permission_classes=(IsAuthenticated, ))
    def favorite(self, request, pk):
        return self.add_delete(Favorite, request, pk)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated, ))
    def shopping_cart(self, request, pk):
        return self.add_delete(ShoppingCart, request, pk)

    @action(detail=False,
            permission_classes=(IsAuthenticated, ))
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__shoppingcarts__user=request.user).values(
                'ingredient__name', 'ingredient__measurement_unit'
                ).annotate(Sum('amount'))
        content = 'N - ingredient - amount, measurement unit\n'
        for num, ingredient in enumerate(ingredients, 1):
            content += (f'{num} - {ingredient["ingredient__name"]} - '
                        f'{ingredient["amount__sum"]}, '
                        f'{ingredient["ingredient__measurement_unit"]}\n')
        response = HttpResponse(content, content_type='application/txt')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.txt"')
        return response
