from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from rag_pipeline import qa_chain
from LetterGenerator.schemas import LetterResponse, LetterRequest
from LetterGenerator.generator import generate_letter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://localhost:5173",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat_with_charly(question: str = Body(..., embed=True)):
    answer = qa_chain.invoke(question)
    answer_text = str(answer["result"])
    return {"answer": answer_text}

@app.post("/generate-letter", response_model=LetterResponse)
async def generate_letter_route(data: LetterRequest):
    try:
        letter = generate_letter(data)
        return LetterResponse(letter=letter)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))