from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache
import re
from app.models.model_singleton import get_model_instance

set_llm_cache(InMemoryCache())

model_local = get_model_instance()

def create_query_transformation_logic():
    template = """
    The user has submitted the following query:
    
    {query}

    your task is to convert this query into proper search engine query format that help with deep searches, output only the best transformed query and nothing else
    example:
    what is the best Btech college in India so far?
    Best Btech colleges in India
    
    Give only the Transformed Query as output
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = (
        prompt
        | model_local
        | StrOutputParser()
    )
    return chain

def transform_query(chain, question):
    return chain.invoke({"query": question})
