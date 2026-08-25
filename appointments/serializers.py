from django.utils import timezone
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
        validators = ()

    def validate_data(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError(
                "A consulta deve ser agendada para uma data futura."
            )

        return value

    def validate(self, attrs):
        profissional = attrs.get(
            "profissional",
            getattr(self.instance, "profissional", None),
        )

        data = attrs.get(
            "data",
            getattr(self.instance, "data", None),
        )

        if profissional and data:
            appointments = Appointment.objects.filter(
                profissional=profissional,
                data=data,
            )

            if self.instance:
                appointments = appointments.exclude(pk=self.instance.pk)

            if appointments.exists():
                raise serializers.ValidationError(
                    {
                        "data": (
                            "Este profissional já possui uma "
                            "consulta neste horário."
                        )
                    }
                )

        return attrs