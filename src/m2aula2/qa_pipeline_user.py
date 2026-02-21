from langchain_core.prompts import ChatPromptTemplate
from rich import print

from src.config import get_langchain_model
from src.m2aula2.data_ingestion_user import retriever_user

# 1. Inicializar modelo de linguagem
llm = get_langchain_model()

# 2. Definir prompt de QA
qa_prompt = ChatPromptTemplate.from_template(
    "Responda com base EXCLUSIVA no contexto.\n"
    "Pergunta: {pergunta}\n\n"
    "Contexto:\n{contexto}\n\n"
    "Resposta concisa com fonte no formato [fonte: título]."
)


# 3. Função para formatar documentos
def format_docs(docs):
    blocos = []
    for d in docs:
        titulo = d.metadata.get("title", "Wikipedia")
        blocos.append(f"[{titulo}] {d.page_content}")
    return "\n\n***\n\n".join(blocos)


# 4. Função principal de QA
def answer_linear(pergunta: str):
    docs = retriever_user.invoke(pergunta)  # buscar documentos relevantes
    contexto = format_docs(docs)  # formatar contexto
    msg = qa_prompt.format_messages(pergunta=pergunta, contexto=contexto)
    out = llm.invoke(msg)  # gerar resposta com LLM
    return out.content


# 5. Entrada do usuário: pergunta
pergunta = input("\nDigite sua pergunta: ")
response = answer_linear(pergunta)
print(f"\nLLM: {response}")
