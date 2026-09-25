from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

#1  DEFINE STATE

class State(TypedDict):
    name: str
    message: str
    
#2 DEFINE NODE 
def greet_user(state: State):
    print("[Node] Running greet_user...")
    
    name= state["name"]
    return{
        "message": f"Hello {name}"
    }
    
#3 CREATE GRAPH
graph= StateGraph(State)

#4 ADD NODE
graph.add_node("greet_user", greet_user)

#5 ADD EDGES
graph.add_edge(START, "greet_user")
graph.add_edge("greet_user", END)

#6 CREATE CHECKPOINT
memory= MemorySaver()

#7 COMPILE GRAPH WITH MEMORY
app= graph.compile(
    checkpointer= memory
)

#8 CREATE THREAD
config= {
    "configurable": {
        "thread_id": "user_1"
    }
}

#9 FIRST RUN
result1= app.invoke(
    {
        "name": "Krish",
        "message": ""
    },
    config= config
)

print("Name:", result1["name"])
print("Message:", result1["message"])