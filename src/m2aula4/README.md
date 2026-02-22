### Descricao do arquivo

**atvPratica_data_ingestion** (multiuso) ->
O código baixa um artigo científico em PDF e o livro Alice’s Adventures in Wonderland em HTML, carrega ambos como documentos, divide-os em chunks menores, gera embeddings locais com HuggingFace e armazena tudo em um banco vetorial Chroma. Em seguida, configura um retriever para consultas semânticas utilizando a estratégia MMR (Maximal Marginal Relevance), que retorna trechos relevantes e ao mesmo tempo diversos, evitando redundância entre os resultados. Esse fluxo corresponde à etapa de retrieval dentro de um sistema RAG e oferece flexibilidade: o mesmo retriever pode ser integrado tanto a um grafo de QA com LangGraph quanto a um chain de QA com LangChain, permitindo diferentes formas de orquestrar a geração de respostas completas a partir dos documentos recuperados.

**atvPratica_graph_qa_pipeline** (Graph) ->
O código implementa um grafo de QA com LangGraph que organiza o processo de perguntas e respostas em etapas sequenciais. Primeiro, recebe a pergunta do usuário, depois utiliza o retriever para buscar documentos relevantes no banco vetorial, em seguida formata esses trechos em um contexto estruturado e, por fim, invoca um LLM para gerar a resposta. O modelo é instruído a responder de forma concisa e exclusivamente com base nos documentos recuperados, citando a fonte correspondente. Esse design modular torna o fluxo mais transparente e flexível, permitindo controlar cada fase do RAG (retrieval, formatação do contexto e geração da resposta) dentro de um grafo bem definido

**atvPratica_gchain_qa_pipeline** (Chain) ->
O código implementa um fluxo de perguntas e respostas (QA) baseado em RAG (Retrieval-Augmented Generation) utilizando LangChain. Ele inicializa um modelo de linguagem, define um prompt amigável que instrui o LLM a responder exclusivamente com base nos documentos recuperados e a indicar a fonte da informação. Em seguida, usa um retriever previamente configurado para buscar trechos relevantes no banco vetorial, formata esses documentos em um contexto estruturado e passa a pergunta junto com o contexto ao modelo. O LLM gera uma resposta concisa e amigável, exibida ao usuário. Esse pipeline mantém a busca restrita ao retriever, mas organiza o contexto de forma mais clara e acessível, garantindo flexibilidade e confiabilidade na geração das respostas.

### Para Rodar

python -m src.m2aula4.atvPratica_chain_qa_pipeline

python -m src.m2aula4.atvPratica_graph_qa_pipeline
