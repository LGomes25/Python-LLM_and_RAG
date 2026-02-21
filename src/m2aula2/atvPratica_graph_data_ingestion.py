from langchain_community.document_loaders import WikipediaLoader
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Entrada do usuário: tópicos e parâmetros de chunk
topics = input("\nDigite os tópicos separados por vírgula: ").split(",")
chunk_size = int(input("Defina o tamanho do chunk (<=500 - ex: 500): "))
chunk_overlap = int(input("Defina o overlap entre chunks (<=50 - ex: 50): "))

docs = []

# Carregar artigos da Wikipedia
for t in topics:
    loader = WikipediaLoader(query=t.strip(), lang="pt", load_max_docs=1)
    docs.extend(loader.load())

# Dividir documentos em chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=True
)
splits = splitter.split_documents(docs)

# Gerar embeddings locais
embeddings = HuggingFaceBgeEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Criar banco vetorial persistente
vectordb = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    collection_name="wikipedia_pt_graph",
    persist_directory="./chroma_wiki_graph",
)
vectordb.persist()

# Configurar retriever com k definido pelo usuário
k = int(input("\nQuantos documentos relevantes deseja recuperar (<=3 - ex: 2)? "))
retriever = vectordb.as_retriever(search_kwargs={"k": k})

print("\nBanco vetorial criado e retriever configurado com sucesso!\n")
