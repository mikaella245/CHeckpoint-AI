from fastapi import APIRouter
from models import RentInput
from logic import calculate_faireness

router = APIRouter()

@router.post("/check_rent")
def check_rent(data: RentInput):
    return calculate_faireness(data)
