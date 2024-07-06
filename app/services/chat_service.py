from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache
import re
from app.models.model_singleton import get_model_instance

set_llm_cache(InMemoryCache())

model_local = get_model_instance()
# model_local = ChatOllama(model="mistral")

def create_chat_logic(retriever):
    template = """
    Here are the documents provided from the web:

    Context: {context}
    Question: {question}

    Based on the above context, give the analysis of and buy, sell or hold signal for the stock, give the reasons for you analysis and ultimately conclude by giving asvise to the users what they should do with the stock.
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model_local
        | StrOutputParser()
    )
    return chain

def ask_question(chain, question):
    return chain.invoke(question)

def format_output_to_html(text):
    text = re.sub(r"\n(\d+)\. ", r"<li>", text)
    text = text.replace("1.", "<ol><li>", 1) 
    text = re.sub(r"(?<!ol>)<li>", r"</li><li>", text) 
    text += "</ol>"  

    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)

    text = re.sub(r"(?m)^\s*(?!<li>|<\/?ol>)(.+?)\s*$", r"<p>\1</p>", text)

    return text