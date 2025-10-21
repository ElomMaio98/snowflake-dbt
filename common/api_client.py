import os
from dotenv import load_dotenv
import requests 
from typing import Dict, List, Optional

load_dotenv()

class CoinGeckoClient:
    BASE_URL = os.getenv('BASE_URL')

    def __init__(self, rate_limit_delay: float = 1.0):
        self.rate_limit_delay = rate_limit_delay

    def get_market_data(self, vs_currency: str ='brl', per_page: int = 50, page: int = 1):
        url = f"{self.BASE_URL}/coins/markets"
        params = {
            'vs_currency': vs_currency,
            'order': 'market_cap_desc',
            'per_page': per_page,
            'page': page,
            'sparkline': False,
            'price_change_percentage': '24h,7d,30d'
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception (f"Falha em conseguir os dados: {e}")

    def get_price_history(self, coin_id: str, Days: int=7):
        url = f"{self.BASE_URL}/coins/{coin_id}/market_chart"
        params = {
            'vs_currency': 'brl',
            'days': Days,
            'interval': 'daily'
        }
        try:
            response = requests.get(url,params=params,timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception (f"Falha em obter dados para moeda {coin_id}: {e}")
        
    def ping(self):
        url = f"{self.BASE_URL}/ping"
        try:
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            return False         
