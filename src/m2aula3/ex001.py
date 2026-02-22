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
    print("\nPDf baixado com sucesso...")
else:
    print("\nPDF já existe, não será baixado novamente.")

# Verifica a existencia antes de download HTML - evitar sobreescrita
if not os.path.exists(html_path):
    r = requests.get(html_url, timeout=60)
    r.raise_for_status()
    with open(html_path, "wb") as f:
        f.write(r.content)
    print("\nHTML baixado com sucesso...")
else:
    print("\nHTML já existe, não será baixado novamente.")

# Exibir os caminhos criados
print(f"\nCaminho PDF: {pdf_path},\nCaminho HTML: {html_path}")

# Carrega o PDF e transforma cada página em um documento LangChain
pdf_loader = PyPDFLoader(file_path=pdf_path)
docs_pdf = pdf_loader.load()
print(f"Número de páginas no PDF: {len(docs_pdf)}")
print("Prévia do conteúdo da primeira página:")
print(docs_pdf[0].page_content[:500])  # primeiros 500 caracteres
print("Metadados da primeira página:")
print(docs_pdf[0].metadata)

# Carrega o HTML usando BeautifulSoup (forçando UTF-8 para evitar erros de encoding)
html_loader = BSHTMLLoader(html_path, open_encoding="utf-8")
docs_html = html_loader.load()
print(f"Número de documentos HTML: {len(docs_html)}")
print(f"Título: {docs_html[0].metadata.get('title')}")

# Dividir documentos em chunks menores para uso nos embeddings e buscas semânticas
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=50, add_start_index=True
)
docs = splitter.split_documents(docs_pdf + docs_html)
print(len(docs), docs[0], metadata)

# Gerar embeddings locais usando HuggingFace (modelo MiniLM-L6-v2)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# test__vec = embeddings.embed_query("Teste rápido de vetor")
# print(test__vec)

# Criar banco vetorial (Chroma) e persiste automaticamente no diretorio criado
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    collection_name="meus_docs",
    persist_directory="./chroma_store",
)

# consulta ao banco
consulta = "Who is alice?"
resultados = vectorstore.similarity_search(consulta, k=3)
for d in resultados:
    print(d.metadata, d.page_content[:100], "\n---")
