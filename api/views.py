from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


from .models import User
from .serializers import SendCodeSerializer, CheckConfirmationCodeSerializer, UserSerializer
from .permissions import IsAdmin


@api_view(['POST'])
def send_confirmation_code(request):
    serializer = SendCodeSerializer(data=request.data)
    email = request.data['email']
    if serializer.is_valid():
        user = User.objects.filter(email=email).exists()
        if not user:
            User.objects.create_user(email=email)
        user = get_object_or_404(User, email=email)
        confirmation_code = default_token_generator.make_token(user)
        mail_subject = 'Код подтверждения на Yamdb.ru'
        message = f'Ваш код подтверждения: {confirmation_code}'
        send_mail(mail_subject, message, 'Yamdb.ru <admin@yamdb.ru>', [email], fail_silently=False)
        return Response(f'Код отправлен на адрес {email}', status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = CheckConfirmationCodeSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get('email')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, email=email)
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token':f'{token}'}, status=status.HTTP_200_OK)
        return Response({'confirmation_code':'Неверный код подтверждения'},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', ]


class APIUser(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response('Вы не авторизованы', status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('Вы не авторизованы', status=status.HTTP_401_UNAUTHORIZED)
