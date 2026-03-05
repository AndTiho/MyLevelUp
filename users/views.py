from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import UserSerializer


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
    serializer_class = UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    """Изменение данных пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        # Разрешаем редактировать только свой профиль
        obj = super().get_object()
        if obj != self.request.user:
            self.permission_denied()
        return obj


class UserDeleteAPIView(DestroyAPIView):
    """Удаление пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
