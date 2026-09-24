from typing import TypedDict
from langgraph.graph import StateGraph, START, END 

#1 DEFINE STATE 
class State(TypedDict):
    counter: int
    message: str
    
#2 NODE -> INCREMENT COUNTER
def increment_counter(state: State):
    counter= state["counter"] + 1
    print(f"Counter = {counter}")
    
    return{
        "counter": counter,
        "message": f"Counter reached {counter}"
    }
    
#3 ROUTING FUNCTION
def check_counter(state: State):
    if state["counter"] < 5:
        return "increment_counter"
    
    return "end"

#4 CREATE GRAPH
graph= StateGraph(State)

#5 ADD NODE
graph.add_node("increment_counter", increment_counter)

#6 START -> END
graph.add_edge(START, "increment_counter")

#7 CONDITIONAL LOOP
graph.add_conditional_edges("increment_counter", check_counter,
    {
        "increment_counter": "increment_counter",
        "end": END
    }
)

#8 COMPILE 
app = graph.compile()

#9 RUN GRAPH
result= app.invoke({
    "counter": 0,
    "message": ""
})

#9 DISPLAY RESULT
print("Counter Count:", result["counter"])
print("Message:", result["message"])