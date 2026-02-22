### Descricao do arquivo

**ex001** ->
O código baixa um artigo científico em PDF e o livro Alice’s Adventures in Wonderland em HTML, carrega ambos como documentos, divide-os em chunks menores, gera embeddings locais com HuggingFace e armazena tudo em um banco vetorial Chroma. Esse banco permite consultas semânticas em linguagem natural, retornando os trechos mais relevantes relacionados à pergunta. Como parte de um fluxo RAG, o código realiza apenas a etapa de retrieval (recuperação dos chunks similares), e a geração de uma resposta completa dependeria da integração com um modelo de linguagem (LLM) que sintetize esses trechos em uma resposta textual.

**atvPratica_loaders** ->
O código demonstra como usar loaders da biblioteca langchain_community para importar dados de diferentes formatos. Ele carrega um PDF e um HTML, converte cada um em documentos estruturados que podem ser usados em fluxos de processamento de linguagem natural, e imprime uma amostra do conteúdo e dos metadados para verificação. É um exemplo simples e direto de ingestão de dados em múltiplos formatos, mostrando como o LangChain facilita a padronização da entrada de documentos para aplicações de IA.

### Para Rodar

python -m src.m2aula3.ex001

python -m src.m2aula3.atvPratica_loaders
