from binance.client import Client
from binance.enums import FuturesType

from bot.config import BINANCE_API_KEY, BINANCE_API_SECRET
from bot.logging_config import logger

def get_binance_client() -> Client:
    """
    Returns a configured python-binance Client for Binance Futures Testnet
    """
    if not BINANCE_API_KEY or not BINANCE_API_SECRET:
        logger.error("API keys missing. Order will fail if authorization is required.")
        
    # testnet=True handles setting the base URL to testnet URL.
    client = Client(
        api_key=BINANCE_API_KEY,
        api_secret=BINANCE_API_SECRET,
        testnet=True
    )
    
    # Verify explicitly that it points to https://testnet.binancefuture.com
    # Just to be completely sure. 
    # With python-binance, testnet=True changes the base REST APIs, 
    # and we specifically want the futures testnet.
    return client
