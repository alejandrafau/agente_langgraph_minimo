from langchain_core.messages import SystemMessage
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import ChatOllama
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.tools import tool
from langchain_core.tools.retriever import create_retriever_tool
#from fuente_informacion import this_retriever

###########CREACION DE HERRAMIENTAS##########
#Sea cual sea el sistema RAG que se haya implementado en fuente_informacion.py
#se lo importa (en este caso como this_retriever) y se lo usa para crear una herramienta:
#
############################################

"""
retriever_tool = create_retriever_tool(
    this_retriever,
    "retrieve_infoleg_data",
    "Search and return information of laws in infoleg",
)
"""

def multiply(a: int, b: int) -> int:
    """Multiplies a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b


@tool
def laugh():
    """Generate a laughing onomatopoeia eg: hahahahahahaha"""
    return "hahahahahahaha"




#En esta lista de abajo abría que agregar retriever_tool una vez que esté desarrollado bien
tools = [laugh]

###########INSTANCIA DE MODELO Y BINDING DE TOOLS##########
#Se instancia el modelo ...se usa alguno via API o local via Ollama
#Con bind_tools, se le "notifican" de las herramientas disponibles
############################################

llm = ChatAnthropic(model='claude-3-5-sonnet-20241022')
#llm2 = ChatOllama(model="llama3")
llm_with_tools = llm.bind_tools(tools)

###########CREACIÓN DEL ASISTENTE##########
#El asistente no será otra cosa que la combinación del modelo con herramientas
# el SystemMessage (el prompt de sistema) y el HumanMessage (el prompt de usuario)
############################################


sys_msg = SystemMessage(content="You are a helpful assistant tasked with laughing")
"""
sys_msg = SystemMessage(content=(
    "You are a helpful legal research assistant. "
   "Your role is to analyze user questions or commands, identify references to laws, decrees, or articles, "
    "and extract the relevant information needed to search in the Infoleg database. "
    "If the user mentions a law by number (e.g., 'Ley 20.744') or a decree, capture it precisely. "
    "If no explicit law is mentioned, infer possible keywords to search in Infoleg. "
    "Always prepare the output so it can be used to query Infoleg or a legal knowledge base."
))
"""
def assistant(state: MessagesState):
   return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

###########CREACIÓN DEL FLUJO##########
#Se crea un flujo controlado bajo principios de REACT: el asistente eligirá
#una herramienta si considera pertinente y luego analizará esa misma elección
#-el flujo regresa de nuevo al asistente-minimizando así errores y halucinaciones
############################################

builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "assistant")

graph = builder.compile()

