from fastapi import FastAPI 
from models import RentInput
from logic import calculate_faireness

app= FastAPI()

@app.post("/check_rent")
def check_rent(data: RentInput):
    return calculate_faireness(data)