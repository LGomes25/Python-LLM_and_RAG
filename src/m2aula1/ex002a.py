from src.config import get_langchain_model
from rich import print
from typing import TypedDict
from langgraph.graph import StateGraph, END


# Estado da aplicação
class AppState(TypedDict):
    input: str
    resposta_bruta: str
    resposta_final: str


llm = get_langchain_model()


# Nós - cada nó recebe uma função
def receber_input(state: AppState) -> AppState:
    return {"input": state["input"], "resposta_bruta": "", "resposta_final": ""}


def processar_llm(state: AppState) -> AppState:
    prompt = f"Responda de forma breva: {state['input']}"
    out = llm.invoke(prompt).content
    return {"input": state["input"], "resposta_bruta": str(out), "resposta_final": ""}


def formatar_saida(state: AppState) -> AppState:
    final = f"Resposta gerada:\n{state['resposta_bruta']}"
    return {
        "input": state["input"],
        "resposta_bruta": state["resposta_bruta"],
        "resposta_final": final,
    }


# Construção do grafo
graph = StateGraph(AppState)

graph.add_node("Input", receber_input)
graph.add_node("LLM", processar_llm)
graph.add_node("Formatar", formatar_saida)

graph.set_entry_point("Input")
graph.add_edge("Input", "LLM")
graph.add_edge("LLM", "Formatar")
graph.set_finish_point("Formatar")

app = graph.compile()


# Execução do flow_prompt
user_message = input("\nInsira a pergunta: ")
print("\n")

estado_resposta: AppState = {
    "input": user_message,
    "resposta_bruta": "",
    "resposta_final": "",
}

resultado = app.invoke(estado_resposta)

print(resultado["resposta_final"])
