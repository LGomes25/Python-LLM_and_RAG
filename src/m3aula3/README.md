### Descricao do arquivo

**rag_pipeline**(recuperação e persistencia no banco) ->
Esse código define o fluxo principal de preparação dos dados para o banco vetorial. Ele começa configurando os caminhos da raiz do projeto, da pasta de dados e da pasta onde o banco Chroma será persistido. Em seguida, há a função load_docs, responsável por criar a pasta de dados caso não exista e carregar documentos de diferentes formatos, como PDF, TXT, Markdown e HTML, utilizando loaders específicos para cada tipo. Depois, a função split_docs divide os documentos em pedaços menores, chamados chunks, para facilitar a criação de embeddings e melhorar a busca semântica. A função build_chroma é a que efetivamente gera o banco vetorial, aplicando embeddings com o modelo HuggingFace e persistindo os dados no diretório configurado. Por fim, no bloco principal, o código executa esse pipeline completo: carrega os documentos, gera os chunks, mostra a quantidade processada e constrói o banco Chroma.

**chatbot_graph**(langgraph)->
Esse código define o funcionamento do chatbot com RAG dentro de um grafo de estados. Ele começa configurando os diretórios e a estrutura de estado que guarda pergunta, mensagens, documentos, contexto e resposta. A função get_retriever conecta ao banco vetorial Chroma usando embeddings do HuggingFace e busca documentos relevantes. O modelo de linguagem é carregado e combinado com um prompt que orienta a forma da resposta. O grafo é composto por quatro nodes principais: o node_init_pipeline, que verifica e cria o banco se necessário; o node_retriever, que busca os documentos; o node_augment, que concatena e limita o contexto; e o node_generate, que usa o modelo para produzir a resposta final. O fluxo começa pelo node de inicialização e segue até a geração da resposta, garantindo que todo o processo esteja integrado e automatizado.

**interface**(StreamLit) ->
Esse código é responsável por montar a interface do chatbot usando Streamlit. Ele configura a página, define o título e cria uma barra lateral com informações sobre o modelo de linguagem e os embeddings, além de permitir ajustar o parâmetro de top‑k e recarregar o retriever. O histórico de mensagens é inicializado com uma mensagem de boas‑vindas e exibido na tela, diferenciando mensagens do usuário e do assistente. Quando o usuário envia uma pergunta, essa entrada é adicionada ao histórico e o grafo do aplicativo é invocado, passando a questão e o histórico como estado. O resultado da execução retorna a resposta do modelo, que é mostrada na interface junto com as fontes utilizadas, exibidas em expansores. Por fim, o histórico é atualizado para incluir a nova resposta, mantendo a conversa contínua dentro da aplicação.

**atiPratica** ->
Baseados no mesmo fluxo dos códigos anteriores, só que com a possibilidade de controle de parametros estáticos (chunks) e dinâmicos pelo front.

### Para Rodar

python -m streamlit run src/m3aula3/interface.py

python -m streamlit run src/m3aula3/atvPratica_interface.py
