from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.services.api.v1 import views

router = DefaultRouter()

router.register("subscriptions", views.SubscriptionsModelView, basename="subscriptions")

urlpatterns = [
    path("", include(router.urls)),
    path("exchange-rate/", views.ExchangeRateAPIView.as_view(), name="exchange-rate"),
    path(
        "cancel-subscription/",
        views.SubscriptionCancelAPIView.as_view(),
        name="cancel-subscription",
    ),
]
