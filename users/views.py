from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny

from users.models import User
from users.permissions import IsOwner
from users.serializers import UserDetailSerializer, UserSerializer


class UserCreateAPIView(CreateAPIView):
    """Регистрация нового пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    """Просмотр всех пользователей"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailAPIView(RetrieveAPIView):
    """Детальный просмотр пользователя"""

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserUpdateAPIView(UpdateAPIView):
    """Изменение данных пользователя"""

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsOwner]


class UserDeleteAPIView(DestroyAPIView):
    """Удаление пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwner]
