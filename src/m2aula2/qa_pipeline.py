from langchain_core.prompts import ChatPromptTemplate
from rich import print

from src.config import get_langchain_model
from src.m2aula2.data_ingestion import retriever

llm = get_langchain_model()

# Definir prompt de QA
qa_prompt = ChatPromptTemplate.from_template(
    "Responda com base EXCLUSIVA no contexto.\n"
    "Pergunta: {pergunta}\n\n"
    "Contexto:\n{contexto}\n\n"
    "Resposta concisa com fonte no formato [fonte: título]."
)


# Função para formatar documentos
def format_docs(docs):
    blocos = []
    for d in docs:
        titulo = d.metadata.get("title", "Wikipedia")
        blocos.append(f"[{titulo}] {d.page_content}")
    return "\n\n***\n\n".join(blocos)


# Função principal de QA linear
def answer_linear(pergunta: str):
    docs = retriever.invoke(pergunta)  # buscar documentos relevantes

    contexto = format_docs(docs)  # formatar contexto

    msg = qa_prompt.format_messages(pergunta=pergunta, contexto=contexto)
    out = llm.invoke(msg)  # gerar resposta com LLM

    return out.content


# Teste de execução
print(answer_linear("Quais são os principios da LGPD?"))
