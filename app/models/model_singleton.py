from langchain_community.chat_models import ChatOllama
from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache

set_llm_cache(InMemoryCache())

class ModelSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating the model instance")
            cls._instance = super(ModelSingleton, cls).__new__(cls)
            cls._instance.model = ChatOllama(model="llama3")
        return cls._instance.model

def get_model_instance():
    return ModelSingleton()
