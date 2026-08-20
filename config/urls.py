from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from config.auth import CustomAuthToken

urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "api/v1/professionals/",
        include("professionals.urls"),
    ),

    path(
        "api/v1/appointments/",
        include("appointments.urls"),
    ),

    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),

    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        "api/v1/auth/token/",
        CustomAuthToken.as_view(),
        name="api-token-auth",),
]
