from langchain_community.document_loaders import WikipediaLoader
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Carregar artigos da Wikipedia (um por tópico)
topics = [
    "Lei Geral de proteção de Dados",
    "Transformers (NLP)",
    "LangChain",
    "Wikipedia",
]

docs = []

# um artigo por tópico para o BD na instrução load_max_docs=1
for t in topics:
    loader = WikipediaLoader(query=t, lang="pt", load_max_docs=1)
    docs.extend(loader.load())

# Dividir documentos em chunks menores para caber no contexto do modelo
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=50, add_start_index=True
)
splits = splitter.split_documents(docs)

# Gerar embeddings locais usando HuggingFace (modelo MiniLM-L6-v2)
embeddings = HuggingFaceBgeEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Criar banco vetorial (Chroma) e salvar em disco para reuso
vectordb = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    collection_name="wikipedia_pt_reg",
    persist_directory="./chroma_wiki",
)
vectordb.persist()

# Configurar retriever (retorna os 2 documentos mais relevantes)
retriever = vectordb.as_retriever(search_kwargs={"k": 2})
