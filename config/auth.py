from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class CustomAuthToken(ObtainAuthToken):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)

    @extend_schema(
        request=inline_serializer(
            name="TokenLoginRequest",
            fields={
                "username": serializers.CharField(),
                "password": serializers.CharField(write_only=True),
            },
        ),
        responses={
            200: inline_serializer(
                name="TokenLoginResponse",
                fields={
                    "token": serializers.CharField(),
                },
            )
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})