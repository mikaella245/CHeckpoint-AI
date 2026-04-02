from pydantic import BaseModel
from typing import Optional, Literal

LetterType = Literal[
    "rent-increase",
    "rent-decrease",
    "guarantee-return",
    "fault-repair",
    "conciliation",
    "resiliation",
]

PreavisType = Literal["within", "outside"]

class LetterRequest(BaseModel):
    letter_type: LetterType
    tenant_name: str
    landlord_name: str
    landlord_address: str
    address: str
    additional_details: Optional[str] = ""
    preavis_type: Optional[PreavisType] = None

class LetterResponse(BaseModel):
    letter: str