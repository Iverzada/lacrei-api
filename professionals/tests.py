from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Professional


class ProfessionalAPITests(APITestCase):

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

    def test_list_professionals(self):
        url = reverse("professional-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 1)

    def test_create_professional(self):
        url = reverse("professional-list")

        data = {
            "nome_social": "João Silva",
            "profissao": "Cardiologista",
            "endereco": "Brasília - DF",
            "contato": "joao@email.com",
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

        self.assertTrue(
            Professional.objects.filter(
                nome_social="João Silva"
            ).exists()
        )

    def test_retrieve_professional(self):
        url = reverse(
            "professional-detail",
            args=[self.professional.id],
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["nome_social"],
            "Gabriela Silva",
        )

    def test_update_professional(self):
        url = reverse(
            "professional-detail",
            args=[self.professional.id],
        )

        data = {
            "nome_social": "Gabriela Silva",
            "profissao": "Psicóloga Clínica",
            "endereco": "Brasília - DF",
            "contato": "novo@email.com",
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

        self.professional.refresh_from_db()

        self.assertEqual(
            self.professional.profissao,
            "Psicóloga Clínica",
        )

    def test_partial_update_professional(self):
        url = reverse(
            "professional-detail",
            args=[self.professional.id],
        )

        data = {
            "contato": "alterado@email.com",
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

        self.professional.refresh_from_db()

        self.assertEqual(
            self.professional.contato,
            "alterado@email.com",
        )

    def test_delete_professional(self):
        url = reverse(
            "professional-detail",
            args=[self.professional.id],
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Professional.objects.filter(
                id=self.professional.id
            ).exists()
        )

    def test_create_professional_without_required_fields(self):
        url = reverse("professional-list")

        data = {
            "nome_social": "Gabriela",
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

        url = reverse("professional-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_create_professional_with_valid_phone(self):
        url = reverse("professional-list")

        data = {
            "nome_social": "João Silva",
            "profissao": "Cardiologista",
            "endereco": "Brasília - DF",
            "contato": "(61) 99999-9999",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_create_professional_with_invalid_contact(self):
        url = reverse("professional-list")

        data = {
            "nome_social": "João Silva",
            "profissao": "Cardiologista",
            "endereco": "Brasília - DF",
            "contato": "contato-invalido",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn("contato", response.data)

    def test_create_professional_with_invalid_address(self):
        url = reverse("professional-list")

        data = {
            "nome_social": "João Silva",
            "profissao": "Cardiologista",
            "endereco": "123",
            "contato": "joao@email.com",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn("endereco", response.data)

    def test_create_professional_with_short_name_and_profession(self):
        url = reverse("professional-list")

        data = {
            "nome_social": "A",
            "profissao": "X",
            "endereco": "Brasília - DF",
            "contato": "joao@email.com",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn("nome_social", response.data)
        self.assertIn("profissao", response.data)