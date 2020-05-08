from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import send_confirmation_code, get_jwt_token, UserViewSet, APIUser, CategoryViewSet, TitleViewSet, \
    GenreViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)

urlpatterns = [
    path('v1/auth/email/', send_confirmation_code, name='get_token'),
    path('v1/auth/token/', get_jwt_token, name='send_confirmation_code'),
    path('v1/users/me/', APIUser.as_view()),
    path('v1/', include(router.urls)),
]
