import requests

from apps.services.models import ExchangeRateLog
from metrovps.settings import EXCHANGE_RATE_API_KEY


class RateFetcher:
    BASE_CURRENCY = "USD"
    API_URL = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/{BASE_CURRENCY}"

    def fetch_rates(self):
        try:
            response = requests.get(self.API_URL)
            response.raise_for_status()
            data = response.json()

            rates = data.get("conversion_rates")
            if not rates:
                return

            self.store_rates(rates)
        except requests.RequestException as e:
            print(f"Failed to fetch exchange rates: {e}")

    def store_rates(self, rates):
        ExchangeRateLog.objects.bulk_create(
            [
                ExchangeRateLog(
                    base_currency=self.BASE_CURRENCY,
                    target_currency=currency,
                    rate=rate,
                )
                for currency, rate in rates.items()
            ]
        )
