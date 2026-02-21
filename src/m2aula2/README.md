### Descricao do arquivo

**data_ingestion** (Arquivo de apoio com funções específicas)->
Esse código é um pipeline de preparação de dados que coleta artigos da Wikipédia sobre tópicos definidos, divide os textos em pedaços menores para facilitar o processamento, gera embeddings vetoriais desses pedaços e os armazena em um banco vetorial ChromaDB, configurando um retriever capaz de recuperar os trechos mais relevantes em consultas posteriores.

**qa_pipeline** (Arquivo executável)->
Esse código define um fluxo de perguntas e respostas que usa um retriever para buscar documentos relevantes, formata o conteúdo em blocos, aplica um prompt estruturado e invoca um modelo de linguagem para gerar respostas concisas com referências às fontes.

**data_ingestion_user** (Arquivo de apoio com funções específicas)->
Esse arquivo mantém as mesmas funcionalidades do original, ou seja, carrega artigos da Wikipédia, divide os textos em chunks, gera embeddings e armazena tudo em um banco vetorial ChromaDB. A diferença é que agora o processo é interativo: o usuário escolhe os tópicos que deseja carregar, define o tamanho e o overlap dos chunks e decide quantos documentos relevantes serão recuperados pelo retriever. Dessa forma, a ingestão de dados deixa de ser fixa e passa a ser configurável conforme a necessidade de cada consulta.

**qa_pipeline_user** (Arquivo executável)->
Esse arquivo mantém as mesmas funcionalidades do original, a diferença é que a pergunta não está mais pré-definida no código, mas sim fornecida pelo usuário em tempo de execução. Isso torna o fluxo de perguntas e respostas dinâmico, permitindo que qualquer questão seja feita e respondida com base nos documentos carregados anteriormente, respeitando o número de chunks relevantes definido pelo usuário.

**atvPratica_graph_data_ingestion** (Arquivo de apoio com funções específicas)->
Esse arquivo mantém a função original de ingestão de dados: carregar artigos da Wikipédia, dividir em chunks, gerar embeddings e salvar no banco vetorial ChromaDB. A diferença é que agora ele foi preparado para servir como base do grafo, expondo o retriever que será utilizado pelos nós do pipeline. O usuário continua tendo controle sobre os parâmetros principais — tópicos, tamanho e overlap dos chunks, além da quantidade de documentos relevantes (k) — mas o resultado final é um retriever pronto para ser consumido pelo grafo de QA.

**atvPratica_graph_qa_pipeline** (Arquivo executável)->
Esse arquivo continua responsável por estruturar o fluxo de perguntas e respostas, mas agora está organizado como um grafo em LangGraph. Ele define o estado compartilhado (QAState) e cria nós independentes para cada etapa: entrada da pergunta pelo usuário, busca no banco vetorial, formatação do contexto e geração da resposta com o LLM. A execução segue uma ordem linear, com cada nó enriquecendo o estado até chegar à resposta final. A principal mudança em relação ao código anterior é a modularização em nós e o uso do grafo para controlar o fluxo, tornando o pipeline mais visual, escalável e fácil de expandir.

### Para Rodar

python -m src.m2aula2.qa_pipeline

python -m src.m2aula2.qa_pipeline_user

python -m src.m2aula2.atvPratica_graph_qa_pipeline
