from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Appointment.objects.select_related(
            "profissional"
        ).order_by("data", "id")

        profissional_id = self.request.query_params.get(
            "profissional"
        )

        if profissional_id:
            queryset = queryset.filter(
                profissional_id=profissional_id
            )

        return queryset
