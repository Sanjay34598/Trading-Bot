from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from pydantic import ValidationError
import time

from bot.client import get_binance_client
from bot.logging_config import logger
from bot.validators import OrderModel
from bot.config import MOCK_BINANCE

def create_order(symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> dict:
    """
    Validates and places an order on Binance Futures Testnet.
    Returns a dictionary with success status, message, and optimal order data.
    """
    logger.info(f"Received order request: {symbol} {side} {order_type} qty={quantity} price={price}")

    # 1. Validate Input
    try:
        validated_order = OrderModel(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "message": f"Validation failed: {e}", "data": None}

    # 2. Get Client
    from bot.config import BINANCE_API_KEY, BINANCE_API_SECRET
    if not MOCK_BINANCE and (not BINANCE_API_KEY or not BINANCE_API_SECRET):
        logger.error("API keys missing, cannot submit live order.")
        return {"success": False, "message": "API Keys missing. Please generate your Testnet keys and save them in the .env file to run live orders.", "data": None}
        
    client = get_binance_client()
    
    # 3. Prepare parameters for Futures order
    # Note: python-binance uses `futures_create_order` for USD-M Futures
    params = {
        'symbol': validated_order.symbol,
        'side': validated_order.side,
        'type': validated_order.order_type,
        'quantity': validated_order.quantity,
    }
    
    if validated_order.order_type == 'LIMIT':
        params['timeInForce'] = 'GTC'
        params['price'] = validated_order.price

    # 4. Place Order
    logger.info(f"Sending API request to Futures testnet with params: {params}")
    try:
        if MOCK_BINANCE:
            logger.info("MOCK_BINANCE is True: Simulating successful API response.")
            response = {
                "orderId": int(time.time() * 1000),
                "symbol": validated_order.symbol,
                "status": "NEW" if validated_order.order_type == "LIMIT" else "FILLED",
                "clientOrderId": "mocked_id",
                "price": str(validated_order.price if validated_order.price else 0),
                "avgPrice": "0.00000" if validated_order.order_type == "LIMIT" else str(params.get('price', 90000)),
                "origQty": str(validated_order.quantity),
                "executedQty": "0" if validated_order.order_type == "LIMIT" else str(validated_order.quantity),
                "cumQuote": "0",
                "type": validated_order.order_type,
                "side": validated_order.side,
                "updateTime": int(time.time() * 1000)
            }
        else:
            response = client.futures_create_order(**params)
        logger.info(f"Successful order response: {response}")
        return {
            "success": True,
            "message": "Order placed successfully.",
            "data": response
        }

    except BinanceAPIException as e:
        logger.error(f"Binance API Exception: Status={e.status_code}, Message={e.message}")
        return {"success": False, "message": f"Binance API Error: {e.message}", "data": None}
    except BinanceRequestException as e:
        logger.error(f"Binance Request Exception: {e}")
        return {"success": False, "message": f"Network/Request Error: {e}", "data": None}
    except Exception as e:
        logger.exception(f"Unexpected error occurred: {e}")
        return {"success": False, "message": f"Unexpected Error: {e}", "data": None}
