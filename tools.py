from langchain.tools import tool
import finnhub
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

# ── Tool 1 — Stock price ───────────────────────────────────────────────────────
@tool
def get_stock_price(ticker: str) -> str:
    """Fetch current stock price and daily performance for a ticker."""
    try:
        # Client created HERE — not at module level
        client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

        quote = client.quote(ticker)
        current = quote["c"]
        previous = quote["pc"]
        change = round(current - previous, 2)
        percent = round((change / previous) * 100, 2)

        return (
            f"Ticker: {ticker}\n"
            f"Current Price: {current}\n"
            f"Previous Close: {previous}\n"
            f"Change: {change}\n"
            f"Change Percent: {percent}%\n"
            f"Day High: {quote['h']}\n"
            f"Day Low: {quote['l']}"
        )
    except Exception as e:
        return f"Could not fetch price: {e}"


# ── Tool 2 — Company fundamentals ─────────────────────────────────────────────
@tool
def get_company_details(ticker: str) -> str:
    """Fetch company profile and key financial metrics for a ticker."""
    try:
        # Client created HERE — not at module level
        client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

        profile = client.company_profile2(symbol=ticker)
        metrics = client.company_basic_financials(ticker, "all")
        data = metrics["metric"]

        return (
            f"Company: {profile.get('name', 'N/A')}\n"
            f"Ticker: {ticker}\n"
            f"Country: {profile.get('country', 'N/A')}\n"
            f"Exchange: {profile.get('exchange', 'N/A')}\n"
            f"Industry: {profile.get('finnhubIndustry', 'N/A')}\n"
            f"P/E Ratio: {data.get('peNormalizedAnnual', 'N/A')}\n"
            f"EPS: {data.get('epsNormalizedAnnual', 'N/A')}\n"
            f"52 Week High: {data.get('52WeekHigh', 'N/A')}\n"
            f"52 Week Low: {data.get('52WeekLow', 'N/A')}"
        )
    except Exception as e:
        return f"Could not fetch fundamentals: {e}"


# ── Tool 3 — Stock news ────────────────────────────────────────────────────────
@tool
def get_stock_news(company: str) -> str:
    """
    Search for the latest news related to a company or stock.

    Examples:
    - Apple
    - Infosys
    - Reliance Industries
    - TCS

    Returns the top 5 recent news articles with title, URL, and short summary.
    """
    try:
        # Client created HERE — not at module level
        tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

        result = tavily.search(
            query=f"Latest stock news about {company}",
            max_results=5
        )

        news = []
        for article in result["results"]:
            news.append(
                f"Title: {article['title']}\n"
                f"URL: {article['url']}\n"
                f"Summary: {article['content'][:300]}"
            )

        return "\n\n--------------\n\n".join(news)
    except Exception as e:
        return f"Could not fetch stock news: {str(e)}"