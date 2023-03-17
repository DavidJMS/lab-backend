# From Django
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("api/", include(("apps.accounts.urls", "clients"), namespace="clients")),
    path(
        "api/medical/", include(("apps.medical.urls", "medical"), namespace="medical")
    ),
    path(
        "api/financials/",
        include(("apps.financials.urls", "financials"), namespace="financials"),
    ),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
    show_indexes=True,
)
