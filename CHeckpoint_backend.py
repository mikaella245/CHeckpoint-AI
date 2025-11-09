from fastapi import FastAPI, Form 
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    content = """
    <h1>CHeckpoint Prototype</h1>
    <form action="/feedback" method="post">
        <textarea name="message" placeholder="Your feedback"></textarea>
        </form>
    """
    return content

@app.post("/feedback")
async def feedback(message: str = Form(...)):
    print("Received feedback:", message)
    return {"status": "ok"}