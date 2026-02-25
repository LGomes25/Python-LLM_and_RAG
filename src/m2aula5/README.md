### Descricao do arquivo

**ex001** (Factor K)->
O código demonstra um fluxo simples de RAG local: gera embeddings com HuggingFace, cria documentos de texto com metadados, armazena-os em um banco vetorial Chroma e realiza buscas semânticas variando o parâmetro top_k para comparar a quantidade e diversidade de resultados retornados em consultas, lembrando que valores maiores de k podem trazer ruído ao incluir documentos menos relevantes.

**ex002** (Similaridade)->
O código demonstra um fluxo de RAG local: gera embeddings com HuggingFace, cria documentos de texto com metadados, armazena-os em um banco vetorial Chroma e realiza buscas semânticas com pontuação de relevância, aplicando diferentes limiares de score para filtrar os resultados e avaliar a qualidade dos documentos retornados

**ex003** (metadata - data limite)->
O arquivo demonstra um fluxo de RAG local com filtro temporal: primeiro gera embeddings com HuggingFace, cria documentos com metadados (incluindo datas), e armazena-os em um banco vetorial Chroma. Em seguida, define uma função de busca que recebe uma consulta e um limite de data. O processo segue duas etapas: (1) realiza uma busca semântica inicial (similarity_search), retornando até k documentos mais próximos da query, mesmo que alguns tenham baixa relevância; (2) aplica um filtro adicional sobre os resultados, selecionando apenas os documentos cuja data seja posterior ao limite definido. Essa sequência explica por que, em casos onde não há similaridade contextual, ainda podem aparecer documentos irrelevantes — eles entram no conjunto retornado pela busca semântica e passam no filtro de data, resultando em “ruído” nos resultados finais

**ex004** (prompt customizado)->
O arquivo implementa um fluxo de RAG local com seleção dinâmica de prompt e escolha de pergunta pelo usuário. Inicializa um modelo de linguagem configurado, gera embeddings locais com HuggingFace e cria documentos contendo texto e metadados (fonte e data). Esses documentos são armazenados em um banco vetorial Chroma e consultados por um retriever configurado com busca semântica (mmr) e limite de k=2. O usuário pode escolher, via terminal, entre três prompts distintos (especialista, professor ou entusiasta/torcedor), que definem o estilo e a profundidade da resposta. Os documentos recuperados são formatados e inseridos no prompt selecionado, compondo um pipeline que conecta retriever → formatação → prompt → LLM → parser. Por fim, o usuário também escolhe a pergunta a ser respondida pelo terminal, e o sistema retorna a resposta contextualizada de acordo com os documentos e o prompt escolhido.

**ex005** (temperatura)->
O arquivo demonstra um fluxo de RAG local com variação de temperatura: gera embeddings com HuggingFace, cria documentos com texto e metadados e os armazena em um banco vetorial Chroma. Um retriever com busca semântica (mmr, k=4) recupera os documentos relevantes, que são formatados e inseridos em um prompt especializado. O pipeline conecta retriever → formatação → prompt → LLM → parser. Em seguida, um loop inicializa o modelo com diferentes temperaturas (0.0, 0.5, 1.0) e executa a mesma pergunta, permitindo comparar como a criatividade e consistência das respostas variam conforme o parâmetro.

### Para Rodar

python -m src.m2aula5.ex001

python -m src.m2aula5.ex002

python -m src.m2aula5.ex003

python -m src.m2aula5.ex004

python -m src.m2aula5.ex005
