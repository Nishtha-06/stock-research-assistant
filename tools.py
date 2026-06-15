from langchain.tools import tool
import yfinance as yf #yfinance is just a Python library not website like tavily
from langchain_mistralai import ChatMistralAI
from tavily import TavilyClient
from dotenv import load_dotenv
import os
import time

load_dotenv()

#1st tool - Fetches real-time stock price and market performance data.
@tool
def get_stock_price(ticker: str) -> dict:
    """
    Fetch current stock price and basic market information.
    """

    try:
        time.sleep(2)

        data = yf.download(
            ticker,
            period="5d",
            interval="1d",
            progress=False,
            threads=False
        )

        if data.empty:
            return f"No price data found for {ticker}"

        latest = data.iloc[-1]

        current_price = float(latest["Close"].iloc[0])

        previous_close = (
            float(data.iloc[-2]["Close"].iloc[0])
            if len(data) > 1
            else current_price
        )

        change = round(current_price - previous_close, 2)

        change_percentage = round(
            (change / previous_close) * 100,
            2
        )


        return (
            f"Ticker: {ticker}\n"
            f"Current Price: {current_price}\n"
            f"Previous Close: {previous_close}\n"
            f"Change: {change}\n"
            f"Change Percent: {change_percentage}%\n"
            f"Day High: {float(latest['High'].iloc[0])}\n"
            f"Day Low: {float(latest['Low'].iloc[0])}\n"
            f"Volume: {int(latest['Volume'].iloc[0])}"
        )


    except Exception as e:
        return f"Could not fetch stock price: {e}"

#get_stock_price.invoke("INFY.NS")

#2nd tool - it shows that company is good or not

@tool
def get_company_details(ticker: str) -> str:
    """
    Fetch company fundamentals.
    """

    try:

        time.sleep(3)

        stock = yf.Ticker(ticker)

        info = stock.get_info()


        return (
            f"Company: {info.get('longName','N/A')}\n"
            f"Ticker: {ticker}\n"
            f"Sector: {info.get('sector','N/A')}\n"
            f"Industry: {info.get('industry','N/A')}\n"
            f"P/E Ratio: {info.get('trailingPE','N/A')}\n"
            f"Forward P/E: {info.get('forwardPE','N/A')}\n"
            f"EPS: {info.get('trailingEps','N/A')}\n"
            f"Revenue Growth: {info.get('revenueGrowth','N/A')}\n"
            f"Profit Margin: {info.get('profitMargins','N/A')}\n"
            f"ROE: {info.get('returnOnEquity','N/A')}\n"
            f"Debt To Equity: {info.get('debtToEquity','N/A')}\n"
            f"Dividend Yield: {info.get('dividendYield','N/A')}"
        )


    except Exception as e:
        return f"Could not fetch fundamentals: {e}"
#get_company_details.invoke("AAPL")


#3rd agent - Collects the latest news and updates related to a company or stock.
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def get_stock_news(company: str) -> str:
    """
    Search for the latest news related to a {company} or stock.

    Examples:
    - Apple
    - Infosys
    - Reliance Industries
    - TCS

    Returns the top 5 recent news articles with title,
    source URL, and short summary.
    """

    try:
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
    

#get_stock_news.invoke("Infosys")

