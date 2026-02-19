import os
from langchain_openai import ChatOpenAI
from openai import OpenAI

# Configuração comum
BASE_URL = "http://127.0.0.1:1234/v1"
API_KEY = "lm-studio"
MODEL_NAME = "meta-llama-3.1-8b-instruct"

os.environ["OPENAI_API_KEY"] = API_KEY


def get_langchain_model():  # <= nome da função a ser importada
    """Retorna modelo configurado para uso com LangChain."""
    return ChatOpenAI(
        model=MODEL_NAME,
        base_url=BASE_URL,
        temperature=0.2,
        max_completion_tokens=500,
        streaming=True,
    )


def get_openai_client():  # <= nome da função a ser importada
    """Retorna cliente OpenAI para chamadas diretas."""
    return OpenAI(
        base_url=BASE_URL,
        api_key=API_KEY,
    )
