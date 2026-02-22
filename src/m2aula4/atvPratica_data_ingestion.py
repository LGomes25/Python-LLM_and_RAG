import os
from importlib import metadata

import requests
from langchain_community.document_loaders import BSHTMLLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Criacao de pastas e download de arquivo PDF e HTML
os.makedirs("data", exist_ok=True)
os.makedirs("chroma_store", exist_ok=True)

pdf_url = "https://arxiv.org/pdf/1706.03762.pdf"  # Attention is all you need (arXiv)
html_url = (
    "https://www.gutenberg.org/files/11/11-h/11-h.htm"  # Alice (Project Gutemberg)
)

pdf_path = "data/attention_is_all_you_need.pdf"
html_path = "data/alice"

# Verifica a existencia antes de download PDF - evitar sobreescrita
if not os.path.exists(pdf_path):
    r = requests.get(pdf_url, timeout=60)
    r.raise_for_status()
    with open(pdf_path, "wb") as f:
        f.write(r.content)
else:
    print("\nPDF já existe, não será baixado novamente.")

# Verifica a existencia antes de download HTML - evitar sobreescrita
if not os.path.exists(html_path):
    r = requests.get(html_url, timeout=60)
    r.raise_for_status()
    with open(html_path, "wb") as f:
        f.write(r.content)
else:
    print("\nHTML já existe, não será baixado novamente.")


# Carrega o PDF e transforma cada página em um documento LangChain
pdf_loader = PyPDFLoader(file_path=pdf_path)
docs_pdf = pdf_loader.load()

# Carrega o HTML usando BeautifulSoup (forçando UTF-8 para evitar erros de encoding)
html_loader = BSHTMLLoader(html_path, open_encoding="utf-8")
docs_html = html_loader.load()

# Dividir documentos em chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=50, add_start_index=True
)
docs = splitter.split_documents(docs_pdf + docs_html)

# Gerar embeddings locais
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Criar banco vetorial persistente
vectordb = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    collection_name="pdf_html_load",
    persist_directory="./chroma_store",
)


# Configurar retriever com k definido pelo usuário
retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 4})

print("\nBanco vetorial criado e retriever configurado com sucesso!\n")
