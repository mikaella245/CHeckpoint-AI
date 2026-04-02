from pydantic import BaseModel
class RentInput(BaseModel):
    original_rent: float
    current_rent: float
    contract_year: int
    increase_year: int
    renovations: bool
    #renovation_type: str