### Descricao do arquivo

**chatbot**(LangGraph) ->
O código cria um assistente de chat para uma loja de bicicletas usando LangChain e LangGraph. Ele inicializa o modelo de linguagem, define um prompt de sistema com instruções e tom de voz amigável, monta um template de chat que combina essa mensagem com o histórico da conversa e conecta ao modelo. A função gerar_resposta invoca o modelo com o estado atual e retorna o histórico atualizado. Por fim, o grafo de estados é configurado com um único nó de chat, compilado e disponibilizado para uso no frontend com Streamlit.

**interface**(StreamLit) ->
O código implementa o frontend do chatbot em Streamlit. Ele configura a página com título e ícone, exibe uma mensagem inicial de boas-vindas e mantém o histórico de mensagens em st.session_state. O usuário interage pelo campo st.chat_input, e cada nova entrada é adicionada ao histórico como HumanMessage. Em seguida, o histórico completo é enviado ao backend (app.invoke), que retorna as mensagens atualizadas incluindo a resposta da IA. Por fim, o histórico é exibido na tela em ordem cronológica, diferenciando mensagens do usuário e do assistente com st.chat_message.

**atiPratica**(StreamLit + memo) ->
O código implementa um chatbot em Streamlit com memória e contador de interações. Ele inicializa o modelo de linguagem e cria variáveis persistentes no st.session_state para armazenar tanto o histórico da conversa quanto o número de iterações. A interface apresenta um campo de entrada de texto e dois botões: um para enviar mensagens e outro para limpar o histórico. Quando o usuário envia uma pergunta, o contador é incrementado, a mensagem é adicionada ao histórico e o modelo é invocado com esse histórico completo. A resposta gerada é também armazenada e exibida junto com o número da iteração. Se o botão de limpar for acionado, o histórico e o contador são resetados.

### Para Rodar

python -m streamlit run src/m3aula2/interface.py

python -m streamlit run src/m3aula2/atvPratica.py
