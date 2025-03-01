from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4

class Transaction(BaseModel):
    transaction_id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")  # auto-generate a unique ID
    category_id: str
    account_id: str
    date: datetime
    description: str
    balance: float
    payment: float
    receipt: float
