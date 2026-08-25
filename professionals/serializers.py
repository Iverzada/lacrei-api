import re

from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from rest_framework import serializers

from .models import Professional


class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = (
            "id",
            "nome_social",
            "profissao",
            "endereco",
            "contato",
        )
        read_only_fields = ("id",)

    def validate_nome_social(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "O nome social não pode estar vazio."
            )

        if len(value) < 2:
            raise serializers.ValidationError(
                "O nome social deve possuir pelo menos 2 caracteres."
            )

        return value

    def validate_profissao(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "A profissão não pode estar vazia."
            )

        if len(value) < 2:
            raise serializers.ValidationError(
                "A profissão deve possuir pelo menos 2 caracteres."
            )

        return value

    def validate_endereco(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "O endereço não pode estar vazio."
            )

        if len(value) < 5:
            raise serializers.ValidationError(
                "O endereço deve possuir pelo menos 5 caracteres."
            )

        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError(
                "O endereço deve conter informações textuais válidas."
            )

        return value

    def validate_contato(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "O contato não pode estar vazio."
            )

        try:
            validate_email(value)
            return value
        except DjangoValidationError:
            pass

        if not re.fullmatch(r"[+\d\s().-]+", value):
            raise serializers.ValidationError(
                "Informe um e-mail ou telefone válido."
            )

        digits = re.sub(r"\D", "", value)

        if not 10 <= len(digits) <= 13:
            raise serializers.ValidationError(
                "Informe um e-mail ou telefone válido."
            )

        return value