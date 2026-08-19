from rest_framework import serializers

from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    profissional_nome = serializers.CharField(
        source="profissional.nome_social",
        read_only=True,
    )

    class Meta:
      model = Appointment
      fields = (
        "id",
        "data",
        "profissional",
        "profissional_nome",
    )
    read_only_fields = (
        "id",
        "profissional_nome",
    )