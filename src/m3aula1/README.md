### Descricao do arquivo

**ex001** ->
O código implementa uma aplicação simples de chat com IA usando Streamlit. Inicializa um modelo de linguagem configurado via get_langchain_model(), define o título da interface e cria um campo de entrada para o usuário digitar sua pergunta. Ao clicar no botão de envio, o sistema verifica se há texto: se houver, concatena instruções adicionais à pergunta e invoca o modelo, exibindo a resposta na tela; se o campo estiver vazio, apresenta um aviso ao usuário. Esse fluxo permite testar interativamente o modelo dentro de uma interface web leve, controlando entrada e saída diretamente pelo Streamlit. Importante: não existe histórico de perguntas, cada chamada é única.

**atvPratica** ->
Baseado no código anterior, acrescentou-se um subtitulo e um spiner enquanto aguarda a resposta.

### Para Rodar

python -m streamlit run src/m3aula1/ex001.py

python -m streamlit run src/m3aula1/atvPratica.py
