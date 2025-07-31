from rest_framework import serializers

from apps.authentication.api.base.serializers import UserSerializer
from apps.services.models import Plan, Subscription


class BasePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["id", "name", "price", "duration_days"]


class BaseSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
        extra_kwargs = {
            "end_date": {"allow_null": True, "required": False},
            "user": {"allow_null": True, "required": False},
        }


class SubscriptionGETSerializer(BaseSubscriptionSerializer):
    user = UserSerializer(read_only=True)
    plan = BasePlanSerializer(read_only=True)


class SubscriptionCancelSerializer(serializers.Serializer):
    reason = serializers.CharField(required=False, allow_null=False, allow_blank=False)
    plan = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.all(), required=True
    )
