from typing import TypedDict
from langgraph.graph import StateGraph, START, END

#1 DEFINE STATE
class State(TypedDict):
    question: str
    processed_question: str
    answer: str
    
#2 NODE 1 -> GET QUESTION
def get_question(state: State):
    print("\n[Node 1] Getting question...")
    return {
        "question": state["question"]
    }
    
#3 NODE 2 -> PROCESS QUESTION
def process_question(state: State):
    print("\n[Node 2 ] Processing question...")
    
    question = state["question"]
    processed_question = question.strip().lower()
    
    return{
        "processed_question":processed_question
    }
    
#4 NODE 3 -> GENERATE ANSWER
def generate_answer(state: State):
    print("\n[Node 3] Generating answer...")
    
    processed_question = state["processed_question"]
    answer = f"You asked about:{processed_question}" 
    
    return{
        "answer": answer
    }
    
#5 CREATE GRAPH
graph = StateGraph(State)

#6 ADD NODES
graph.add_node("get_question", get_question)
graph.add_node("process_question", process_question)
graph.add_node("generate_answer", generate_answer)

#7 CONNECT NODES
graph.add_edge(START, "get_question")
graph.add_edge("get_question", "process_question")
graph.add_edge("process_question", "generate_answer")
graph.add_edge("generate_answer", END)

#8 COMPILE GRAPH
app = graph.compile()

#9 RUN GRAPH

result = app.invoke({
    "question": "What is SmartChargeAI? ",
    "processed_question":"",
    "answer":""
})

#10 DISPLAY FINAL STATE
print("Question:", result["question"])
print("Processed Question:", result["processed_question"])
print("Answer:", result["answer"])