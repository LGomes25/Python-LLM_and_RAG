from langchain_community.document_loaders import BSHTMLLoader, PyPDFLoader

# Carrega o PDF e transforma cada página em um documento LangChain
loader_pdf = PyPDFLoader("./data/Jupiter_e_sua_Biodiversidade.pdf")
documentos_pdf = loader_pdf.load()

# Carrega o HTML usando BeautifulSoup (forçando UTF-8 para evitar erros de encoding)
loader_html = BSHTMLLoader(
    "./data/Spring_Boot_documentation_DevDocs.html", open_encoding="utf-8"
)
documentos_html = loader_html.load()

# Exibe uma prévia do conteúdo e metadados do primeiro documento PDF
print(documentos_pdf[0].page_content[:500])
print(documentos_pdf[0].metadata)

# Exibe uma prévia do conteúdo e metadados do primeiro documento HTML
print(documentos_html[0].page_content[:500])
print(documentos_html[0].metadata)
