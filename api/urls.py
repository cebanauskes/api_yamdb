from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import send_confirmation_code, UserViewSet, APIUser


router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='send_confirmation_code'),
    path('v1/auth/email/', send_confirmation_code, name='get_token'),
    path('v1/users/me/', APIUser.as_view()),
    path('v1/', include(router.urls)),   
]
