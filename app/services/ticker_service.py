from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache
import re
from app.models.model_singleton import get_model_instance

set_llm_cache(InMemoryCache())

model_local = get_model_instance()

def ticker_extractor():
    # Dictionary mapping company names to their ticker symbols
    ticker_dict = {
        "Microsoft": "MSFT",
        "Tesla" : "TSLA",
        "Apple": "AAPL",
        "Google": "GOOGL",
        "Amazon": "AMZN",
        "Facebook": "FB",
        # Add more mappings as needed
    }

    def extract(query):
        words = query.split()
        for word in words:
            if word in ticker_dict:
                return ticker_dict[word]
        return "Unknown"  # Return "Unknown" or any default value if no ticker symbol is found

    return extract

def extract_ticker(chain, question):
    return chain.invoke({"query": question})
