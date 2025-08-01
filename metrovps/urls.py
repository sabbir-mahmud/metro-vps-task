from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("apps.authentication.urls")),
    path("services/", include("apps.services.urls")),
    path("", RedirectView.as_view(url="/services/subscriptions/", permanent=False)),
]
