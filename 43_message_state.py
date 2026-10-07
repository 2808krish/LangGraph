from typing import TypedDict
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END

#1 DEFINE STATE

class State(TypedDict):
    messages: list
    
#2  CREATE NODE

def chatbot(state: State):
    messages = state["messages"]
    
    user_message = messages[-1].content
    
    response = f"You said: {user_message}"
    
    return {
        "messages": [
            AIMessage(content=response)
        ]
    }
    
#3 CREATE GRAPH
graph =  StateGraph(State)

graph.add_node("chatbot", chatbot)
graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)

#4 COMPILE
app = graph.compile()

#5 INVOKE GRAPH
result = app.invoke(
    {
        "messages": [
            HumanMessage(
                content= "What is SmartCharge AI?"
            )
        ]
    }
)
#6 PRINT RESULT 
for message in result["messages"]:
    print(
        f"{message.__class__.__name__}:"
        f"{message.content}"
    )