from django.db import models

from professionals.models import Professional


class Appointment(models.Model):
    data = models.DateTimeField()

    profissional = models.ForeignKey(
        Professional,
        on_delete=models.PROTECT,
        related_name="consultas",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.profissional.nome_social} - {self.data}"