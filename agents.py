from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import get_company_details,get_stock_news,get_stock_price
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0
)

#1st agent
def build_price_agent():
    return create_agent(
        model = llm,
        tools=[get_stock_price],
        system_prompt="You are a stock market analyst. Use the get_stock_price tool to fetch accurate price data for the given ticker and summarise what you find."
    )

#2nd agent
def build_news_agent():
    return create_agent(
        model = llm,
        tools = [get_stock_news],
        system_prompt="You are a financial news analyst. Use the get_stock_news tool to fetch the latest news about the company and summarise the key developments."
    )

#3rd agnet
def build_details_agent():
    return create_agent(
        model = llm,
        tools = [get_company_details],
        system_prompt="You are a fundamental analyst. Use the get_company_details tool to fetch financial metrics and explain what they mean for investors."
    )

#Report writer chains
report_promt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert equity research analyst. Write clear, structured, "
        "and insightful investment research reports."
    ),
    (
        "human",
        """
Write a detailed stock research report for the company below.

Date: {today}

Ticker:
{ticker}

Price Data:
{price_data}

Fundamentals:
{fundamentals}

Recent News:
{news}

Structure:

- Overview
  (company name, ticker, current price, day's performance)

- Fundamental Analysis
  (valuation, profitability, growth — explain what the numbers mean)

- News & Sentiment
  (summarize recent developments and overall sentiment)

- Risks & Considerations

- Conclusion
  (overall outlook: positive, neutral, or cautious — with reasoning)

Be detailed, factual, and professional. Do not give direct buy/sell financial advice,
frame it as an analytical perspective only.
"""
    )
])

report_chain = report_promt | llm | StrOutputParser()

#critic chain

critic_promt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive equity research critic. Be honest and specific."),
    ("human", """Review the stock research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:
Score: X/10

Strengths:
- ...
- ...

Areas to improve:
- ...
- ...

One line verdict:
...""")

])

critic_chain = critic_promt | llm | StrOutputParser()



