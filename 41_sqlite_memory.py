import sqlite3
from typing import TypedDict
from langgraph.graph import StateGraph, START, END 
from langgraph.checkpoint.sqlite import SqliteSaver

#1 DEFINE STATE
class State(TypedDict):
    name: str
    count: int
    message: str
    
#2 DEFINE NODE
def remember_user(state: State):
    count= state["count"]+ 1
    name= state["name"]
    
    print(f"[Node] Interaction number: {count}")
    return{
        "count": count,
        "message": f"Hello {name}. This is iinteraction #{count}."
    }
    
#3 CREATE GRAPH
graph= StateGraph(State)
graph.add_node("remember_user", remember_user)
graph.add_edge(START, "remember_user")
graph.add_edge("remember_user", END)

#4 CREATE SQLITE CONNECTION
conn= sqlite3.connect(
    "checkpoints.db",
    check_same_thread=False
)
    
#5 CREATE SQLITE CHECKPOINTER
memory= SqliteSaver(conn)

app= graph.compile(
    checkpointer=memory
)

config= {
    "configurable":{
        "thread_id": "user_1"
    }
}

#6 FIRST INTERACTION
result1= app.invoke(
    {
        "name":"Krish",
        "count": 0,
        "message": ""
    },
    config= config
)
print("FIRST INTERACTION")
print(result1)

#8 SECOND INTERACTION
result2= app.invoke(
    {
        "name": "Krish"
    },
    config= config
)
print("SECOND INTERACTION")
print(result2)

#9 CURRENT STATE
current_state= app.get_state(config)
print("CURRENT SAVED STATE")
print(current_state.values)

#10 CLOSE DATABASE
conn.close()