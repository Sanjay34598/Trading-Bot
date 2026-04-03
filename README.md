# Binance Futures Testnet Trading Bot

This is a simplified Python trading bot designed to place Market and Limit orders on the Binance Futures Testnet (USDT-M). It features a robust CLI built with `typer` and `rich` for excellent user experience, thorough input validation, and structured logging.

## Requirements
- Python 3.8+
- Binance Futures Testnet account

## Setup

1. **Clone the repository** (or extract the zip folder):
   ```bash
   cd "Binance task"
   ```

2. **Set up a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Credentials**:
   - Create a file named `.env` in the root directory. You can copy `.env.example`:
     ```bash
     cp .env.example .env
     ```
   - Add your testnet API Key and API Secret to `.env`.

## How to Run Examples

The bot comes with a CLI providing helpful text, validation, and rich output formatting.

**View help and commands:**
```bash
python cli.py --help
python cli.py order --help
```

**Place a Market BUY Order:**
```bash
python cli.py order BTCUSDT BUY MARKET 0.01
```

**Place a Limit SELL Order:**
```bash
python cli.py order BTCUSDT SELL LIMIT 0.01 --price 95000.50
```

## Logging
Logs are saved locally to `bot.log` in the application root in a structured format, containing API requests, responses, order success scenarios, and potential API errors.

## Assumptions
- The Base URL is explicitly configured to `https://testnet.binancefuture.com` using the `python-binance` testnet arguments.
- Users are placing USDT-M futures orders.
- Stop-Loss or Take-Profit orders are not configured by default in this minimal CLI setup but framework supports scaling to handles those based on Binance API.
