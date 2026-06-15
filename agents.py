# from langchain.agents import create_agent
# from langchain_mistralai import ChatMistralAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from tools import get_company_details,get_stock_news,get_stock_price
# from dotenv import load_dotenv
# import os

# load_dotenv()

# llm = ChatMistralAI(
#     model="mistral-small-2506",
#     temperature=0
# )

# #1st agent
# def build_price_agent():
#     return create_agent(
#         model = llm,
#         tools=[get_stock_price],
#         system_prompt="You are a stock market analyst. Use the get_stock_price tool to fetch accurate price data for the given ticker and summarise what you find."
#     )

# #2nd agent
# def build_news_agent():
#     return create_agent(
#         model = llm,
#         tools = [get_stock_news],
#         system_prompt="You are a financial news analyst. Use the get_stock_news tool to fetch the latest news about the company and summarise the key developments."
#     )

# #3rd agnet
# def build_details_agent():
#     return create_agent(
#         model = llm,
#         tools = [get_company_details],
#         system_prompt="You are a fundamental analyst. Use the get_company_details tool to fetch financial metrics and explain what they mean for investors."
#     )

# #Report writer chains
# report_promt = ChatPromptTemplate.from_messages([
#     (
#         "system",
#         "You are an expert equity research analyst. Write clear, structured, "
#         "and insightful investment research reports."
#     ),
#     (
#         "human",
#         """
# Write a detailed stock research report for the company below.

# Date: {today}

# Ticker:
# {ticker}

# Price Data:
# {price_data}

# Fundamentals:
# {fundamentals}

# Recent News:
# {news}

# Structure:

# - Overview
#   (company name, ticker, current price, day's performance)

# - Fundamental Analysis
#   (valuation, profitability, growth — explain what the numbers mean)

# - News & Sentiment
#   (summarize recent developments and overall sentiment)

# - Risks & Considerations

# - Conclusion
#   (overall outlook: positive, neutral, or cautious — with reasoning)

# Be detailed, factual, and professional. Do not give direct buy/sell financial advice,
# frame it as an analytical perspective only.
# """
#     )
# ])

# report_chain = report_promt | llm | StrOutputParser()

# #critic chain

# critic_promt = ChatPromptTemplate.from_messages([
#      ("system", "You are a sharp and constructive equity research critic. Be honest and specific."),
#     ("human", """Review the stock research report below and evaluate it strictly.

# Report:
# {report}

# Respond in this exact format:
# Score: X/10

# Strengths:
# - ...
# - ...

# Areas to improve:
# - ...
# - ...

# One line verdict:
# ...""")

# ])

# critic_chain = critic_promt | llm | StrOutputParser()


from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import get_company_details, get_stock_news, get_stock_price
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0
)

# ── Universal tool-calling loop ────────────────────────────────────────────────
def run_agent(system_prompt: str, user_message: str, tools: list) -> str:
    tool_map = {t.name: t for t in tools}
    llm_with_tools = llm.bind_tools(tools)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message),
    ]

    while True:
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            break

        for tool_call in response.tool_calls:
            tool_fn = tool_map.get(tool_call["name"])
            if tool_fn:
                result = tool_fn.invoke(tool_call["args"])
                messages.append(ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"]
                ))

    return response.content


# ── Agents ─────────────────────────────────────────────────────────────────────
def build_price_agent():
    def run(ticker: str) -> str:
        return run_agent(
            system_prompt=(
                "You are a stock price analyst. "
                "You MUST use the get_stock_price tool to fetch live data. "
                "Never answer from your own knowledge. "
                "After fetching, write a 3-4 sentence analysis of the price data."
            ),
            user_message=f"Get current price and market data for {ticker}",
            tools=[get_stock_price]
        )
    return run

def build_details_agent():
    def run(ticker: str) -> str:
        return run_agent(
            system_prompt=(
                "You are a fundamental analyst. "
                "You MUST use the get_company_details tool to fetch data. "
                "Never answer from your own knowledge. "
                "After fetching, explain each metric in plain English for investors."
            ),
            user_message=f"Get fundamental and valuation data for {ticker}",
            tools=[get_company_details]
        )
    return run

def build_news_agent():
    def run(company: str) -> str:
        return run_agent(
            system_prompt=(
                "You are a financial news analyst. "
                "You MUST use the get_stock_news tool to fetch real news. "
                "Never answer from your own knowledge or make up news. "
                "After fetching, summarise the key developments and overall sentiment."
            ),
            user_message=f"Get the latest news and sentiment about {company}",
            tools=[get_stock_news]
        )
    return run


# ── Report chain ───────────────────────────────────────────────────────────────
report_prompt = ChatPromptTemplate.from_messages([
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
Ticker: {ticker}

Price Data:
{price_data}

Fundamentals:
{fundamentals}

Recent News:
{news}

Structure your report with these exact sections:

### Overview
(company name, ticker, current price, date, day's performance)

### Fundamental Analysis
(valuation, profitability, growth — explain what the numbers mean)

### News & Sentiment
(summarize recent developments and overall sentiment)

### Risks & Considerations
(list key risks investors should be aware of)

### Conclusion
(overall outlook: positive, neutral, or cautious — with clear reasoning)

Be detailed, factual, and professional. Do not give direct buy/sell financial advice,
frame it as an analytical perspective only.
"""
    )
])

report_chain = report_prompt | llm | StrOutputParser()


# ── Critic chain ───────────────────────────────────────────────────────────────
critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a sharp and constructive equity research critic. Be honest and specific."
    ),
    (
        "human",
        """Review the stock research report below and evaluate it strictly.

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
..."""
    )
])

critic_chain = critic_prompt | llm | StrOutputParser()
