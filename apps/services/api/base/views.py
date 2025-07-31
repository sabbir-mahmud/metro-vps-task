from datetime import datetime, timedelta

from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.utils.paginator import StandardPagination
from apps.services.api.base.serializers import (
    BaseSubscriptionSerializer,
    SubscriptionGETSerializer,
)
from apps.services.models import Plan, Subscription
from apps.services.utils.fetch_rates import RateFetcher


class BaseExchangeRateAPIView(APIView):
    def get(self, request):
        base, target = request.query_params.get(
            "base",
        ), request.query_params.get("target")
        if not base or not target:
            return Response(
                {"error": "Both 'base' and 'target' query parameters are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rate = RateFetcher(base, target).fetch_rate()
        if rate is None:
            return Response(
                {"error": "Failed to fetch exchange rate."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "rate": rate.get("conversion_rate"),
                "base_currency": rate.get("base_code"),
                "target_currency": rate.get("target_code"),
                "last_updated": rate.get("time_last_update_utc"),
            },
            status=status.HTTP_200_OK,
        )


class BaseSubscriptionsModelView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BaseSubscriptionSerializer
    pagination_class = StandardPagination
    queryset = Subscription.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return SubscriptionGETSerializer
        return super().get_serializer_class()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id

        plan = Plan.objects.filter(id=request.data.get("plan")).first()
        if not plan:
            return Response(
                {"error": "Invalid plan id!"},
                status=status.HTTP_404_NOT_FOUND,
            )

        request.data["end_date"] = datetime.now() + timedelta(days=plan.duration_days)
        sr = self.get_serializer(data=request.data)
        sr.is_valid(raise_exception=True)
        obj = sr.save()

        rate = RateFetcher().fetch_rate()
        if rate is None:
            raise transaction.TransactionManagementError(
                "Failed to fetch exchange rate."
            )

        rate = rate.get("conversion_rate")
        amount = "{:.2f}".format(float(obj.plan.price) * rate)

        return Response(
            {
                "message": "Subscription created successfully!",
                "amount": amount,
                "subscription": SubscriptionGETSerializer(obj).data,
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        return Response(
            {"error": "Method not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"error": "Method not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
