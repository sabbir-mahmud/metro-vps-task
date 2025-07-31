from apps.services.utils.fetch_rates import RateFetcher
from metrovps.celery import app


@app.task(name="metrovps.background_exchange_rates_fetch")
def background_exchange_rates_fetch():
    """
    Fetch exchange rates in the background.
    """
    fetcher = RateFetcher()
    fetcher.fetch_rate()
