from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

#1 DEFINE STATE
class State(TypedDict):
    name: str
    message: str
    
#2 CREATE NODE
def approval_node(state: State):
    name = state["name"]
    
    decision= interrupt(
        f"Should we continue for {name}? Type YES or NO"
    )
    
    if decision == "YES":
        return {
            "message": "Human approved. Continuing Execution."
        }
        
    return {
        "message": "Human rejected. Stopping execution."
    }
    
#3 CREATE GRAPH
graph= StateGraph(State)

graph.add_node("approval_node", approval_node)

graph.add_edge(START, "approval_node")
graph.add_edge("approval_node", END)

#4 CHECKPOINT MEMORY

memory= MemorySaver()

app = graph.compile(
    checkpointer=memory
)

#5 CREATE THREAD
config= {
    "configurable" : {
        "thread_id": "approval_1"
    }
}

#6 START GRAPH
result = app.invoke(
    {
        "name": "Krish",
        "message": ""
    },
    config=config    
)

#7 GRAPH IS INTERRUPTED
print("GRAPH INTERRUPTED")
print(result)

#8 RESUME GRAPH
decision = input("\nEnter your decision (YES/NO):")
result = app.invoke(
    Command(resume=decision),
    config=config
)

#9 FINAL RESULT

print("FINAL RESULT")
print(result)
