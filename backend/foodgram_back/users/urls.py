from rest_framework.routers import DefaultRouter
from django.urls import include, path
# from rest_framework.authtoken import views
# from djoser.views import UserViewSet
from api.views import (CustomUserViewSet, )  # SubscriptionViewSet, )

router = DefaultRouter()

# router.register('users', UserViewSet, basename='users')
# router.register('users/subscriptions', SubscriptionViewSet, basename='users/subscriptions')
router.register('users', CustomUserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    # path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    # path('auth/token/login/', views.obtain_auth_token),
    # path('', include('djoser.urls.jwt')),
]
