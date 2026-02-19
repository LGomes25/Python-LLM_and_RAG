from src.config import get_langchain_model
from rich import print
from langchain_core.prompts import ChatPromptTemplate

# Inicializa modelo de linguagem
llm = get_langchain_model()

# Define oum template de prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Você é um assistente especializado em {tema}. Explique de forma clara para um público iniciante: {pergunta}",
        ),
    ]
)

tema = "Inteligência Artificial"
pergunta = "O que é um modelo de linguagem"

# Encadeia prompt com o modelo
qna_chain = prompt | llm

# Executa a cadeia
response = qna_chain.invoke(
    {
        "tema": tema,
        "pergunta": pergunta,
    }
)

print(response.content)
