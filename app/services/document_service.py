from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders.csv_loader import CSVLoader

def load_documents(urls):
    docs = [WebBaseLoader(url).load() for url in urls]
    return [item for sublist in docs for item in sublist]
    # loader = CSVLoader(file_path="/Users/damodargupta/Desktop/EPICS-PROJECT/Stock pred LLM 3/TSLA_Stock_Data.csv")
    # documents = loader.load()
    # return documents

def process_documents(docs_list):
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
    doc_splits = text_splitter.split_documents(docs_list)
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="rag-chroma",
        embedding=OllamaEmbeddings(model='nomic-embed-text'),
    )
    return vectorstore.as_retriever()