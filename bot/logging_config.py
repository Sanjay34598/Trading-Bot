import logging
import sys

def setup_logging():
    logger = logging.getLogger("binance_bot")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler("bot.log", mode='a')
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        
        # Console handler - optional, as Typer/Rich will handle user-facing output
        # But helpful for debugging
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.ERROR) # Only show errors in console from logger, rich handles the rest

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

logger = setup_logging()
