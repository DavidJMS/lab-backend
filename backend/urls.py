from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(
        "api/client/", include(("apps.accounts.urls", "clients"), namespace="clients")
    ),
    path(
        "api/medical/", include(("apps.medical.urls", "medical"), namespace="medical")
    ),
]
