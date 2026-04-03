from binance.client import Client
from bot.logging_config import logger

def analyze_and_predict(symbol: str) -> dict:
    """
    Fetches real public market data from Binance Futures Testnet and calculates
    a basic Simple Moving Average (SMA) trend analysis to predict market direction.
    """
    logger.info(f"Running prediction analysis for {symbol}...")
    
    # Public endpoints do not require API keys
    client = Client(testnet=True)
    
    try:
        # Get live ticker price
        ticker = client.futures_symbol_ticker(symbol=symbol)
        current_price = float(ticker['price'])
        
        # Get recent hourly candles (klines) - fetching the last 24 candles
        klines = client.futures_klines(symbol=symbol, interval='1h', limit=24)
        
        if not klines or len(klines) < 20:
            return {"success": False, "message": "Not enough historical market data to predict."}
            
        # Extract closing prices
        prices = [float(k[4]) for k in klines]
        
        # Calculate moving averages
        sma_7 = sum(prices[-7:]) / 7
        sma_20 = sum(prices[-20:]) / 20
        
        # Simple logical predictor
        if sma_7 > sma_20 and current_price > sma_7:
            trend = "BULLISH"
            action = "BUY"
        elif sma_7 < sma_20 and current_price < sma_7:
            trend = "BEARISH"
            action = "SELL"
        else:
            trend = "NEUTRAL"
            action = "WAIT (No clear trend)"
            
        return {
            "success": True,
            "data": {
                "symbol": symbol.upper(),
                "current_price": current_price,
                "sma_7": round(sma_7, 2),
                "sma_20": round(sma_20, 2),
                "trend": trend,
                "action": action
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to fetch market data for prediction: {e}")
        return {"success": False, "message": f"Market Data Error: {e}"}
