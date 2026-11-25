from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class HealthCheckTests(APITestCase):

    def setUp(self):
        self.url = reverse("health-check")

    def test_health_check_returns_200(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_health_check_response_data(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.json(),
            {
                "status": "ok",
                "service": "hostelhub",
            },
        )

    def test_health_check_allows_unauthenticated_access(self):
        self.client.credentials()

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_health_check_rejects_post(self):
        response = self.client.post(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_health_check_rejects_put(self):
        response = self.client.put(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_health_check_rejects_patch(self):
        response = self.client.patch(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_health_check_rejects_delete(self):
        response = self.client.delete(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_health_check_allows_options(self):
        response = self.client.options(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )