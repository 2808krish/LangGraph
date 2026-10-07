from typing import TypedDict
from langgraph.graph import StateGraph, START, END

#1 DEFINE STATE
class State(TypedDict):
    numbers: list
    
#2 FIRST NODE
def add_first_number(state: State):
    
    return{
        "numbers": [1]
    }
    
#3 SECOND NODE
def add_second_number(state: State):
    
    return{
        "numbers": [2]
    }
    
#4 CREATE GRAPH
graph = StateGraph(State) 
graph.add_node("add_first_number", add_first_number)
graph.add_node("add_second_number", add_second_number)

graph.add_edge(START, "add_first_number")
graph.add_edge("add_first_number", "add_second_number")
graph.add_edge("add_second_number", END)

#5 COMPILE
app = graph.compile()

#6 RUN
result= app.invoke(
    {
        "numbers": []
    }
)

#PRINT
print("Final numbers:", result["numbers"])