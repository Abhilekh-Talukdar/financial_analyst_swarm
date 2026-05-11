import yfinance as yf
from langchain_core.tools import tool

@tool
def get_stock_metrics(ticker: str) -> str:
    """Fetch current price, P/E ratio, and market cap for a given stock ticker."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
        pe = info.get('trailingPE', 'N/A')
        market_cap = info.get('marketCap', 'N/A')
        
        # Format market cap for readability
        if isinstance(market_cap, (int, float)):
            market_cap = f"${market_cap / 1e9:.2f} Billion"
            
        return f"Metrics for {ticker}:\n- Current Price: ${price}\n- P/E Ratio: {pe}\n- Market Cap: {market_cap}"
    except Exception as e:
        return f"Error fetching data for {ticker}: {e}"
