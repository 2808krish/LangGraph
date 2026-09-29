import sqlite3
from typing import TypedDict
from langgraph.graph import StateGraph, START, END 
from langgraph.checkpoint.sqlite import SqliteSaver

#1 DEFINE STATE
class State(TypedDict):
    name: str
    count: int
    message: str
    
#2 CREATE NODE
def remember_user(state: State):
    count= state["count"]+ 1
    name= state["name"]
    
    print(f"[Node] {name} -> Interaction #{count}")
    
    return{
        "count": count,
        "message": f"Hello {name}. This is interaction #{count}."
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

#6 COMPILE GRAPH
app= graph.compile(
    checkpointer=memory
)

#7 CREATE TWO THREADS
thread_1= {
    "configurable":{
        "thread_id": "user_1"
    }
} 

thread_2={
    "configurable":{
        "thread_id": "user_2"
    }
}

#6 USER 1 - FIRST INTERACTION
result= app.invoke(
    {
        "name":"Krish",
        "count": 0,
        "message": ""
    },
    config= thread_1
)
print("\nUSER 1")
print(result)

#8 USER 1 - SECOND INTERACTION
result= app.invoke(
    {
        "name": "Krish"
    },
    config= thread_1
)
print("\nUSER 1 AGAIN")
print(result)

#9 USER 2 - FIRST INTERACTION
result= app.invoke(
    {
        "name":"Rahul",
        "count": 0,
        "message": ""
    },
    config= thread_2
)
print("\nUSER 2")
print(result)

#8 USER 1 - SECOND INTERACTION
result= app.invoke(
    {
        "name": "Rahul"
    },
    config= thread_2
)
print("\nUSER 2 AGAIN")
print(result)

#9 CHECK USER 1 STATE
state_1 = app.get_state(thread_1)
print("USER 1 SAVED STATE")
print(state_1.values)

#10 CHECK USER 2 STATE
state_2 = app.get_state(thread_2)
print("USER 2 SAVED STATE")
print(state_2.values)

#10 CLOSE DATABASE
conn.close()