import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from bot.orders import create_order
from bot.predict import analyze_and_predict

app = typer.Typer(help="Binance Futures Testnet Trading Bot CLI")
console = Console()

@app.command()
def order(
    symbol: str = typer.Argument(..., help="Trading pair symbol (e.g., BTCUSDT)"),
    side: str = typer.Argument(..., help="Order side: BUY or SELL"),
    order_type: str = typer.Argument(..., help="Order type: MARKET or LIMIT"),
    quantity: float = typer.Argument(..., help="Quantity to trade"),
    price: float = typer.Option(None, "--price", "-p", help="Required if order_type is LIMIT")
):
    """
    Places an order on Binance Futures Testnet.
    """
    console.print(Panel.fit(
        f"Requesting to place [bold cyan]{order_type}[/bold cyan] order:\n"
        f"Side: [bold {'green' if side.upper() == 'BUY' else 'red'}]{side.upper()}[/]\n"
        f"Symbol: [bold yellow]{symbol.upper()}[/bold yellow]\n"
        f"Quantity: {quantity}\n"
        f"Price: {price if price else 'N/A (Market)'}",
        title="Order Request Summary",
        border_style="cyan"
    ))

    with console.status("[bold green]Sending order to Binance Futures Testnet...[/bold green]"):
        result = create_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )

    if result["success"]:
        data = result["data"]
        
        # Display Success Response
        table = Table(title="Order Response Details", show_header=True, header_style="bold magenta")
        table.add_column("Field", style="dim", width=15)
        table.add_column("Value")
        
        table.add_row("Order ID", str(data.get("orderId", "N/A")))
        table.add_row("Status", str(data.get("status", "N/A")))
        table.add_row("Executed Qty", str(data.get("executedQty", "N/A")))
        
        avg_price = data.get("avgPrice")
        if not avg_price or float(avg_price) == 0:
            # If it's a limit order not yet filled, average price might be 0. Show requested price.
            table.add_row("Price", str(data.get("price", "N/A")))
        else:
            table.add_row("Avg Price", str(avg_price))

        console.print(table)
        console.print(f"[bold green]SUCCESS: {result['message']}[/bold green]")

    else:
        # Display Failure Response
        console.print(Panel.fit(
            f"[bold red]ERROR: Failed to place order![/bold red]\n\n{result['message']}",
            title="Error",
            border_style="red"
        ))

@app.command()
def predict(
    symbol: str = typer.Argument(..., help="Trading pair symbol to analyze (e.g., BTCUSDT)")
):
    """
    Predicts the market trend for a specific symbol using live public market data.
    """
    with console.status(f"[bold cyan]Fetching real-time market data for {symbol.upper()}...[/bold cyan]"):
        result = analyze_and_predict(symbol)
        
    if result["success"]:
        data = result["data"]
        
        table = Table(title=f"Market Prediction: {data['symbol']}", show_header=True, header_style="bold yellow")
        table.add_column("Metric", style="dim", width=18)
        table.add_column("Value")
        
        table.add_row("Live Price", f"${data['current_price']:,.2f}")
        table.add_row("7-Hour SMA", f"${data['sma_7']:,.2f}")
        table.add_row("20-Hour SMA", f"${data['sma_20']:,.2f}")
        
        trend_color = "green" if data['trend'] == "BULLISH" else "red" if data['trend'] == "BEARISH" else "yellow"
        table.add_row("Detected Trend", f"[bold {trend_color}]{data['trend']}[/bold {trend_color}]")
        
        action_color = "green" if data['action'] == "BUY" else "red" if data['action'] == "SELL" else "yellow"
        table.add_row("Suggested Action", f"[bold {action_color}]{data['action']}[/bold {action_color}]")
        
        console.print(table)
    else:
        console.print(Panel.fit(
            f"[bold red]Analysis Failed[/bold red]\n\n{result['message']}",
            title="Error",
            border_style="red"
        ))

if __name__ == "__main__":
    app()
