from langchain.tools import tool
import yfinance as yf #yfinance is just a Python library not website like tavily
from langchain_mistralai import ChatMistralAI
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

#1st tool - Fetches real-time stock price and market performance data.
@tool
def get_stock_price(ticker: str) -> dict:
    """
    Fetch current stock price and basic market information for a stock {ticker}.

    Supports both US and Indian stocks.

    Examples:
    - AAPL
    - MSFT
    - RELIANCE.NS
    - TCS.NS

    Returns current price, previous close, price change,
    day's range, market cap, and trading volume.
    """

    try:
        #create yahoo finance object
        stock = yf.Ticker(ticker)

        #Get stock information
        info = stock.info

        current_price = info.get("currentPrice")
        previous_close = info.get("previousClose") #where it ended yesterday
        
        #Calculate change and percentage change
        if current_price is not None and previous_close is not None:
            change = round(current_price - previous_close,2)
            change_percentage = round(
                (change/previous_close) * 100,2)
            
        else:
            change = "N/A"
            change_percentage = "N/A"

        # Format output as readable text for the agent
        return (
            f"Company: {info.get('longName','N/A')}\n"
            f"Ticker: {ticker}\n"
            f"Current Price: {current_price} {info.get('currency', '')}\n"
            f"Previous Close: {previous_close}\n"
            f"Change: {change}\n"
            f"Change Percent: {change_percentage}%\n"
            f"Day High: {info.get('dayHigh', 'N/A')}\n"
            f"Day Low: {info.get('dayLow', 'N/A')}\n" #the lowest price the stock touched today.
            f"52 Week High: {info.get('fiftyTwoWeekHigh', 'N/A')}\n" #the highest price in the last 1 year (52 weeks)
            f"52 Week Low: {info.get('fiftyTwoWeekLow', 'N/A')}\n"
            f"Market Cap: {info.get('marketCap', 'N/A')}\n"
            f"Volume: {info.get('volume', 'N/A')}\n" #number of shares traded today.
            f"Exchange: {info.get('exchange', 'N/A')}" # which stock market it's listed on (e.g., NSE, NASDAQ, NYSE, BSE).

        )
    
    except Exception as e:
        return f"Could not fetch stock price data: {str(e)}"

#get_stock_price.invoke("INFY.NS")

#2nd tool - it shows that company is good or not

@tool
def get_company_details(ticker: str) -> str:
    """
    Fetch important fundamental information for a stock {ticker}.

    Returns valuation metrics, profitability metrics,
    growth metrics, and company details.
    """

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        return(
            f"Company: {info.get('longName', 'N/A')}\n"
            f"Ticker: {ticker}\n"
            f"Sector: {info.get('sector', 'N/A')}\n"
            f"Industry: {info.get('industry', 'N/A')}\n"
            f"P/E Ratio: {info.get('trailingPE', 'N/A')}\n"
            f"Forward P/E: {info.get('forwardPE', 'N/A')}\n"
            f"EPS: {info.get('trailingEps', 'N/A')}\n"
            f"Revenue Growth: {info.get('revenueGrowth', 'N/A')}\n"
            f"Profit Margins: {info.get('profitMargins', 'N/A')}\n"
            f"Return on Equity: {info.get('returnOnEquity', 'N/A')}\n"
            f"Debt to Equity: {info.get('debtToEquity', 'N/A')}\n"
            f"Dividend Yield: {info.get('dividendYield', 'N/A')}"
        )
    
    except Exception as e:
        return f"Could not fetch fundamentals: {str(e)}"
    
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
