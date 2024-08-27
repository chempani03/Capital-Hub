from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionUpdate(BaseModel):
    booking_date: Optional[datetime] = None
    value_date: Optional[datetime] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    transaction_type: Optional[str] = None
    account: Optional[str] = None
    category: Optional[str] = None
    booking_text: Optional[str] = None
