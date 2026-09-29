from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

#1 DEFINE STATE 
class State(TypedDict):
    name: str 
    count: int 
    message: str
    
#2 DEFNE NODE 
def remember_user(state: State):
    
    count= state["count"]+ 1
    name= state["name"]
    
    print(f"[Node] Interaction number: {count}")
    return{
        "count": count,
        "message": f"Hello {name}. This is interaction #{count}."
    }
    
#3 CREATE GRAPH
graph= StateGraph(State)

#4 ADD NODE
graph.add_node("remember_user", remember_user)

#5 ADD EDGES
graph.add_edge(START, "remember_user")
graph.add_edge("remember_user", END)

#6 CREATE MEMORY
memory= MemorySaver()

#7 COMPILE
app= graph.compile(
    checkpointer= memory
)

#8 CREATE THREAD
config= {
    "configurable": {
        "thread_id": "user_1"
    }
}

#9 FIRST INTERACTION

result1= app.invoke(
    {
        "name": "Krish",
        "count": 0,
        "message": ""
    },
    config= config
)

print("FIRST INTERACTION")
print(result1)

#10 SECOND INTERACTION
result2= app.invoke(
    {
        "name": "Krish"
    },
    config=config
)

#11 READ CURRENT STATE
current_state= app.get_state(config)

print("CURRENT SAVED STATE")
print(current_state.values)