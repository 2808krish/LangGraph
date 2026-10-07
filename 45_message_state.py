from typing import TypedDict
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage, AIMessage    

#1 CREATE NODE
def chatbot(state: MessagesState):
    messages = state["messages"]
    user_message = messages[-1].content 
    
    response = f"You said: {user_message}"
    
    return {
        "messages": [
            AIMessage(content=response)
        ]
    }   


#3 CREATE GRAPH

graph = StateGraph(MessagesState) 
graph.add_node("chatbot", chatbot)

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)

#5 COMPILE
app = graph.compile()

#6 RUN
result= app.invoke(
    {
        "messages": [
            HumanMessage(
                content="Hello!"
            )
        ]
    }
)

#PRINT
for message in result["messages"]:
    print(f"{message.__class__.__name__}:"
          f"{message.content}"
        )
    
# SECOND MESSAGE
result = app.invoke(
    {
        "messages": [
            HumanMessage(
                content="What is SmartCharge AI?"
            )
        ]
    }
)

#PRINT
for message in result["messages"]:
    print(
        f"{message.__class__.__name__}:"
        f"{message.content}"
    )