from fastapi import FastAPI, Form, Body
#from fastapi.responses import HTMLResponse
#from logic import calculate_faireness
#from models import RentInput 
#from pydantic import BaseModel
#import rag_pipeline
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from rag_pipeline import qa_chain
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat_with_charly(question: str = Body(..., embed=True)):
    global all_split_docs
    answer = qa_chain.invoke(question)
    answer_text = str(answer["result"])
    return {"answer": answer_text}

