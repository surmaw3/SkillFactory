import json
from config import keys
import requests


class ConverionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):


        if quote == base:
            raise ConverionException("Валюты должны различаться")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConverionException(f"Не удалось обработать валюту {quote}")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConverionException(f"Не удалось обработать валюту {basw}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConverionException(f"Не удалось обработать количество {amount}")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        total_base = json.loads(r.content)[keys[base]]

        return total_base
