from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings

from src.config import get_langchain_model

# Inicializar modelo
llm = get_langchain_model()

# Gerar embeddings locais
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Criar documentos locais a partir de texto
docs = [
    Document(
        page_content="A energia solar oferece benefícios ambientais e economicos.",
        metadata={"source": "Artigo 1", "date": "2025-01-10"},
    ),
    Document(
        page_content="O Flamengo é o maior time de futebol do mundo nas estatísticas da FIFA",
        metadata={"source": "Artigo 5", "date": "2024-11-15"},
    ),
    Document(
        page_content="A energia solar reduz a conta de luz por ser uma fonte renovável.",
        metadata={"source": "Artigo 2", "date": "2024-11-15"},
    ),
    Document(
        page_content="O campeonato brasileiro vai para por conta da data FIFA",
        metadata={"source": "Artigo 3", "date": "2023-12-01"},
    ),
    Document(
        page_content="O Flamengo é o maior time do mundo segundo o New York Times",
        metadata={"source": "Artigo 4", "date": "2026-02-20"},
    ),
]

# Salvar documentos no BD
vectorstore_meta = Chroma.from_documents(
    documents=docs, embedding=embeddings, collection_name="energia_solar_meta"
)

# Configurar retriever com k definido pelo usuário
retriever = vectorstore_meta.as_retriever(search_type="mmr", search_kwargs={"k": 2})

# Criação/Personalização do prompt
prompt_exclusivo = """
Você é um especialista em energia limpa e um torcedor fanático pelo flamengo..
Utilize SOMENTE os documentos fornecidos abaixo para responder à pergunta do usuário.
Explique de forma clara e simples, como para um iniciante.
Se não houver informação suficiente nos documentos, responda que não sabe.

Documantos: {context}
Pergunta: {question}
Resposta:
"""
prompt_baseado = """
Você é um professor de engenharia e um torcedor fanático pelo flamengo..
Com base nos documentos fornecidos abaixo responda à pergunta do usuário.
Explique de forma detalhada, como para um aluno de engenharia.
Se não houver informação suficiente nos documentos, responda que não sabe.

Documantos: {context}
Pergunta: {question}
Resposta:
"""
prompt_livre = """
Você é um entusiasta em energia limpa mas principalmente um torcedor fanático pelo flamengo.
Responda à pergunta do usuário sem a obrigação de usar os documentos.
Explique de forma clara e simples, para um público leigo
Se não houver informação suficiente nos documentos, utilize o conhecimento acumulado.

Documantos: {context}
Pergunta: {question}
Resposta:
"""
print("\nEscolha o prompt:")
print("1 - Exclusivo (especialista em energia limpa)")
print("2 - Baseado (professor de engenharia)")
print("3 - Livre (entusiasta e torcedor)")

opcao = input("Digite o número da opção desejada: ")

if opcao == "1":
    prompt = PromptTemplate.from_template(prompt_exclusivo)
elif opcao == "2":
    prompt = PromptTemplate.from_template(prompt_baseado)
elif opcao == "3":
    prompt = PromptTemplate.from_template(prompt_livre)
else:
    print("Opção inválida, usando prompt padrão (livre).")
    prompt = PromptTemplate.from_template(prompt_livre)


# Função auxiliar para formatar os documentos em texto concatenado.
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# Pipeline que conecta retriever → formatação → prompt → LLM → parser.
qa_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Chamada a llm
pergunta1 = "Qual é o maior time do mundo?"
pergunta2 = "Quais são os beneficios da energia solar?"

print("\nEscolha a pergunta:")
print("1 - Qual é o maior time do mundo?")
print("2 - Quais são os beneficios da energia solar?")

opcao = input("Digite o número da opção desejada: ")

if opcao == "1":
    resposta = qa_chain.invoke(pergunta1)
elif opcao == "2":
    resposta = qa_chain.invoke(pergunta2)
else:
    print("Opção inválida, usando pergunta 1.")
    resposta = qa_chain.invoke(pergunta1)

print(f"\nLLM -> {resposta}")
