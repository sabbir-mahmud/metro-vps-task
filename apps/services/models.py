from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel

User = get_user_model()


class ExchangeRateLog(BaseModel):
    base_currency = models.CharField(
        max_length=10,
        verbose_name=_("Base Currency"),
        help_text=_("Currency code, e.g., USD"),
    )
    target_currency = models.CharField(
        max_length=10,
        verbose_name=_("Target Currency"),
        help_text=_("Currency code, e.g., BDT"),
    )
    rate = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        verbose_name=_("Exchange Rate"),
        help_text=_("Exchange rate from base to target currency"),
    )

    fetched_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Fetched At"),
        help_text=_("Timestamp when the exchange rate was fetched"),
    )

    class Meta:
        verbose_name = _("Exchange Rate Log")
        verbose_name_plural = _("Exchange Rate Logs")
        ordering = ["-fetched_at"]

    def __str__(self):
        return f"{self.base_currency} to {self.target_currency}: {self.rate}"


class Plan(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_("Plan Name"))
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Price"),
        help_text=_("Price of the plan in USD"),
    )
    duration_days = models.PositiveIntegerField(
        verbose_name=_("Duration (Days)"),
        help_text=_("Duration of the plan in days"),
    )

    class Meta:
        verbose_name = _("Plan")
        verbose_name_plural = _("Plans")
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Subscription(BaseModel):
    class STATUS_CHOICES(models.TextChoices):
        ACTIVE = "active", _("Active")
        CANCELLED = "cancelled", _("Cancelled")
        EXPIRED = "expired", _("Expired")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name=_("User"),
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name="plan_subscriptions",
        verbose_name=_("Plan"),
    )
    start_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Start Date"))
    end_date = models.DateTimeField(verbose_name=_("End Date"))
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES.choices,
        default=STATUS_CHOICES.ACTIVE,
        verbose_name=_("Status"),
    )

    class Meta:
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")
        ordering = ["-id"]

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} ({self.status})"
