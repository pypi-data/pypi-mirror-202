import dotenv
from functools import lru_cache
import os


class Configs:

    def __init__(self):

        dotenv.load_dotenv()
        self.API_CONFIGS_URL = os.getenv("API_CONFIGS_URL", "https://api-gateway.smarketsolutions.com.br/v1/atenas")


@lru_cache()
def get_configs():
    """Helper function to get env with lru cache"""
    return Configs()
