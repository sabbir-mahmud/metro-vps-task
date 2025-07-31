import requests

from apps.services.models import ExchangeRateLog
from metrovps.settings import EXCHANGE_RATE_API_KEY


class RateFetcher:
    def __init__(self, base_currency="USD", target_currency="BDT", store_in_db=True):
        self.base_currency = base_currency.upper()
        self.target_currency = target_currency.upper()
        self.store_in_db = store_in_db

    @property
    def api_url(self):
        return f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/pair/{self.base_currency}/{self.target_currency}"

    def fetch_rate(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()

            rate = data.get("conversion_rate")
            if rate is None:
                return None

            if self.store_in_db:
                self.store_rate(rate)

            return data

        except requests.RequestException as e:
            print(f"Error fetching exchange rate: {e}")
            return None

    def store_rate(self, rate):
        ExchangeRateLog.objects.create(
            base_currency=self.base_currency,
            target_currency=self.target_currency,
            rate=rate,
        )
