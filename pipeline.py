from agents import build_details_agent,build_news_agent,build_price_agent,report_chain,critic_chain

def run_research_pipeline(ticker: str,company_name: str) -> dict:
    state = {}

    #step1 - price agent
    print("\n" + "=" * 50)
    print("step 1 - price agent is fetching market data...")
    print("=" * 50)

    price_agent = build_price_agent()
    price_result = price_agent.invoke({
        "messages": [("user",f"Get current price and market data for {ticker}")]
    })

    state["price_data"] = price_result["messages"][-1].content

    print("\nprice data\n",state["price_data"])

    #step2 - fundamentals agent(company details)
    print("\n" + "=" * 50)
    print("step 2 - fundamentals agent is analyzing financials...")
    print("=" * 50)

    detail_agent = build_details_agent()
    details_result = detail_agent.invoke({
        "messages":[("user",f"Get fundamental and valuation data for {ticker}")]
    })

    state["funadamental"] = details_result["messages"][-1].content    

    print("\nFundamentals\n",state["funadamental"])

    #step3 - news agent
    print("\n" + "=" * 50)
    print("step 3 - news agent is gathering recent news...")
    print("=" * 50)

    news_agent = build_news_agent()
    news_result = news_agent.invoke({
        "messages": [("user",f"Get the latest news and sentiment about {company_name}")]
    })
    state["news"] = news_result["messages"][-1].content

    print("\nNews\n",state["news"])

    #step4 - writer chain
    print("\n" + "=" * 50)
    print("step 4 - writer is drafting the research report...")
    print("=" * 50)

    state["report"] = report_chain.invoke({
        "ticker": ticker,
        "price_data": state["price_data"],
        "fundamentals": state["funadamental"],
        "news": state["news"]
    })

    print("\nfinal report\n",state["report"])

    #step5 - critic chain
    print("\n" + "=" * 50)
    print("step 5 - critic is reviewing the report...")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\ncritic feedback\n",state["feedback"])

    return state

if __name__ == "__main__":
    ticker = input("\nEnter stock ticker (e.g. AAPL,RELIANCE.NS): ")
    company_name = input("Enter company name (e.g. Apple, Reliance Industries): ")
    run_research_pipeline(ticker,company_name)
