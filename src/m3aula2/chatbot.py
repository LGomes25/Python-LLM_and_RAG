from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import MessagesState, StateGraph

from src.config import get_langchain_model

# Inicializa modelo de linguagem
llm = get_langchain_model()

# Prompt inicial (tom de voz e instruções do assistente)
prompt = """
Você é um assistente de IA que ajuda os usuários a encontrar informações sobre produtos de uma loja de bicicleta. Você deve ser amigável, útil e fornecer respostas precisas. Se vocÊ não souver a resposta, diga que não sabe. O usuário pode fazer perguntas sobre produtos, serviços, preçoes e disponibilidade. Você deve sempre tentar ajudar o usuário da melhor maneira possível.
# Tom de voz
Seja amigável e prestativo. Se possivel, use emojis para tornar a conversa mais leve e divertida. Por exemplo, se o usuário perguntar sobre bicicletas, você pode responder com algo como: "Claro! Temos uma ótima seleção e faça trocadilhos com bicicletas
"""

# Template de chat: inclui mensagem de sistema + histórico
chat_template = ChatPromptTemplate.from_messages(
    [("system", prompt), ("placeholder", "{messages}")]
)

# Pipeline: aplica template e envia ao modelo
llm_with_prompt = chat_template | llm


# Função de geração de resposta
def gerar_resposta(state: MessagesState):
    resposta = llm_with_prompt.invoke({"messages": state["messages"]})
    return {"messages": state["messages"] + [resposta]}


# Define grafo de estados da conversa
graph = StateGraph(MessagesState)
graph.add_node("chat", gerar_resposta)
graph.set_entry_point("chat")
graph.set_finish_point("chat")

# Compila aplicação para uso no frontend (Streamlit)
app = graph.compile()
