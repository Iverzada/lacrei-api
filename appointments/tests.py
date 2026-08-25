from datetime import timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from professionals.models import Professional

from .models import Appointment


class AppointmentAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            password="senha123",
        )

        self.token = Token.objects.create(user=self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        self.professional = Professional.objects.create(
            nome_social="Gabriela Silva",
            profissao="Psicóloga",
            endereco="Brasília - DF",
            contato="gabriela@email.com",
        )

        self.future_date = timezone.now() + timedelta(days=1)
        
        self.appointment = Appointment.objects.create(
            data=self.future_date,
            profissional=self.professional,
        )

    def test_list_appointments(self):
        url = reverse("appointment-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 1)

    def test_create_appointment(self):
        url = reverse("appointment-list")

        data = {
             "data": "2026-08-26T15:00:00-03:00",
             "profissional": self.professional.id,
        }

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Appointment.objects.count(),
            2,
        )

    def test_retrieve_appointment(self):
        url = reverse(
            "appointment-detail",
            args=[self.appointment.id],
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_update_appointment(self):
        url = reverse(
            "appointment-detail",
            args=[self.appointment.id],
        )

        data = {
            "data": timezone.now() + timedelta(days=3),
            "profissional": self.professional.id,
        }

        response = self.client.put(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_partial_update_appointment(self):
        url = reverse(
            "appointment-detail",
            args=[self.appointment.id],
        )

        data = {
           "data": timezone.now() + timedelta(days=4),
         }

        response = self.client.patch(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_delete_appointment(self):
        url = reverse(
            "appointment-detail",
            args=[self.appointment.id],
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Appointment.objects.filter(
                id=self.appointment.id
            ).exists()
        )

    def test_filter_appointments_by_professional(self):
        url = reverse("appointment-list")

        response = self.client.get(
            url,
            {
                "profissional": self.professional.id,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 1)

        self.assertEqual(
            response.data[0]["profissional"],
            self.professional.id,
        )

    def test_create_appointment_without_data(self):
        url = reverse("appointment-list")

        data = {
            "profissional": self.professional.id,
        }

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_create_appointment_invalid_professional(self):
        url = reverse("appointment-list")

        data = {
             "data": timezone.now() + timedelta(days=2),
             "profissional": 999999,
        }

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_access_without_authentication(self):
        self.client.credentials()

        url = reverse("appointment-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
    def test_create_appointment_in_the_past(self):
        url = reverse("appointment-list")

        data = {
            "data": timezone.now() - timedelta(days=1),
            "profissional": self.professional.id,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn("data", response.data)

    def test_create_appointment_with_schedule_conflict(self):
        url = reverse("appointment-list")

        data = {
            "data": self.future_date,
            "profissional": self.professional.id,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn("data", response.data)

    def test_different_professionals_can_use_same_datetime(self):
        other_professional = Professional.objects.create(
            nome_social="Marina Souza",
            profissao="Psiquiatra",
            endereco="Brasília - DF",
            contato="marina@email.com",
        )

        url = reverse("appointment-list")

        data = {
            "data": self.future_date,
            "profissional": other_professional.id,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )