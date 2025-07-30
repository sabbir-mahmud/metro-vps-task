from django.contrib import admin

from apps.services.models import ExchangeRateLog, Plan, Subscription

admin.site.register([ExchangeRateLog, Plan, Subscription])
