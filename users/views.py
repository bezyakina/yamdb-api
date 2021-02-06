from uuid import uuid4

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdminOrSuperUser
from .serializers import (
    ConfirmationCodeSerializer,
    MeSerializer,
    UserEmailSerializer,
    UserSerializer,
)
from .utils import send_message


@permission_classes([IsAdminOrSuperUser])
class UserViewSet(viewsets.ModelViewSet):
    """API для работы с пользователями."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"

    @action(
        detail=False,
        methods=["PATCH", "GET"],
        permission_classes=(IsAuthenticated,),
    )
    def me(
            self,
            request,
    ):
        serializer = MeSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def get_confirmation_code(request):
    """Метод для получение кода подтверждения на email."""

    serializer = UserEmailSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    email = serializer.data.get("email")

    if User.objects.filter(email=email).exists():
        return Response(
            {"Email адрес занят"}, status=status.HTTP_400_BAD_REQUEST
        )

    confirmation_code = uuid4()

    User.objects.create(
        email=email, confirmation_code=confirmation_code
    )

    mail_subject = "Код подтверждения"
    message = f"Ваш код подтверждения: {confirmation_code}"
    send_message(mail_subject, message, email)

    return Response(
        {"Success": f"На почту {email} был выслан код подтверждения"},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def get_jwt_token(request):
    """Метод для получения JWT-API токена."""

    serializer = ConfirmationCodeSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    email = serializer.data.get("email")
    confirmation_code = serializer.data.get("confirmation_code")

    user = get_object_or_404(User, email=email)

    if confirmation_code == user.confirmation_code:
        refresh = RefreshToken.for_user(user)

        return Response(
            {"access": str(refresh.access_token)}, status=status.HTTP_200_OK
        )

    return Response(
        {"confirmation_code": "Неверный код подтверждения"},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_confirmation_code(request):
    """Метод для получение нового кода подтверждения на email."""

    serializer = UserEmailSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    email = serializer.data.get("email")
    confirmation_code = uuid4()

    user = User.objects.get(email=email)
    user.confirmation_code = confirmation_code
    user.save(update_fields=["confirmation_code"])

    mail_subject = "Код подтверждения"
    message = f"Ваш код подтверждения: {confirmation_code}"
    send_message(mail_subject, message, email)

    return Response(
        {"Success": f"На почту {email} был выслан новый код подтверждения"},
        status=status.HTTP_200_OK,
    )
