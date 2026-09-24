from typing import TypedDict
from langgraph.graph import StateGraph, START, END

#1 DEFINE STATE
class State(TypedDict):
    question: str
    category: str
    answer: str
    
#2 NODE - CLASSIFY QUESTION
def classify_question(state: State):
    print("\n[Node] Classifying question...")
    question= state["question"].lower()
    
    if "ev" in question or "charging" in question:
        category = "ev"
    else:
        category = "general"
        
    return{
        "category": category
    }
    
#3 NODE - EV ANSWER
def ev_answer(state: State):
    print("[Node] EV answer node")
    
    return{
        "answer":"This question is related to EVs or EV charging"
    }
    
#4 NODE - GENERAL ANSWER
def general_answer(state: State):
    print("[Node] General answer node")
    
    return{
        "answer": "This is a general question."
    }
    
#5 ROUTING FUNCTION 
def route_question(state: State):
    if state["category"]=="ev":
        return "ev_answer"
    else:
        return "general_answer"
    
#6 CREATE GRAPH
graph= StateGraph(State)

#7 ADD NODES
graph.add_node("classify_question",  classify_question)
graph.add_node("ev_answer", ev_answer)
graph.add_node("general_answer", general_answer)

#8 CONNECT NODES
graph.add_edge(START, "classify_question")
graph.add_conditional_edges("classify_question", route_question)
graph.add_edge("ev_answer", END)
graph.add_edge("general_answer", END)

#9 COMPILE 
app= graph.compile()

#10 RUN GRAPH
result= app.invoke({
    "question": "Which EV charging station should I use?",
    "category": "",
    "answer": ""
})

#11 DISPLAY RESULT
print("Question:", result["question"])
print("Category:", result["category"])
print("Answer:", result["answer"])