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

        return value

    def validate_profissao(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "A profissão não pode estar vazia."
            )

        return value

    def validate_endereco(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "O endereço não pode estar vazio."
            )

        return value

    def validate_contato(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "O contato não pode estar vazio."
            )

        return value