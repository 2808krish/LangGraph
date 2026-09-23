from typing import TypedDict
from langgraph.graph import StateGraph, START, END

#1 DEFINE STATE
class State(TypedDict):
    question: str
    answer: str
    
#2 CREATE NODE
def answer_question(state: State):
    question = state["question"]
    answer = f"You asked:{question}"
    
    return{
        "answer": answer
    }
    
#3 CREATE GRAPH
graph= StateGraph(State)

#4 ADD NODE
graph.add_node(
    "answer_question",
    answer_question
)

#5 CONNECT START -> NODE
graph.add_edge(
    START,
    "answer_question"
) 

#6 CONNECT NODE -> END
graph.add_edge(
    "answer_question",
    END
)

#7 COMPILE GRAPH
app = graph.compile()

#8 RUN GRAPH
result= app.invoke(
    {
        "question": "What is SmartCharge AI?",
        "answer": ""
    }
)

# 9 DISPLAY RESULT
print("Question:", result["question"])
print("Answer:", result["answer"])