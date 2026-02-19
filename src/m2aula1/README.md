### Descricao do arquivo

ex001 ->
O código inicializa um modelo de linguagem do LangChain e define um prompt com variáveis dinâmicas.
Em seguida, cria uma cadeia que combina o template com o modelo para gerar respostas.
Por fim, executa a cadeia passando os valores de tema e pergunta, imprimindo o resultado no console.

ex001a ->
Baseado no código anterior, permite que o usuário defina o tema e a pergunta antes de enviar para o llm, a ideia foi dar flexibilidade ao modelo simples e trazer clareza de funcionamento.

ex002 ->
O código constrói um grafo de estados com três nós que processam entrada, resposta do modelo e formatação.
Cada nó atualiza o estado e passa adiante até o fim do fluxo.
No final, imprime a resposta formatada do modelo de linguagem

ex002a ->
Baseado no código anterior, permite a iteração do usuário com a inserção da pergunta na entrada, mantendo o fluxo anterior de busca na llm, geração de resposta preliminar e formatação de saida. Aresta de saída modificada para otimizar codigo. Bloco de chamada e resposta com separação de funções para clarear a leitura.

### Para Rodar

python -m src.m2aula1.ex001

python -m src.m2aula1.ex001a

python -m src.m2aula1.ex002

python -m src.m2aula1.ex002a
