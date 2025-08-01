from django.urls import include, path

from apps.services import views

urlpatterns = [
    path("api/v1/", include("apps.services.api.v1.urls")),
    path("subscriptions/", views.subscriptions, name="subscriptions"),
]
