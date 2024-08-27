from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransOverViewBase(BaseModel):
    transaction_id: str
    booking_date: datetime
    value_date: datetime
    amount: float
    currency: str
    transaction_type: str
    account: str
    category: str
    booking_text: str

    class Config:
        from_attributes = True

class CurrencyBase(BaseModel):
    currency: str
    currency_id: int
    currency_description: Optional[str]

    class Config:
        from_attributes = True

class AccountBase(BaseModel):
    account_id: int
    account: str
    account_description: Optional[str]

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    category_id: int
    category: str
    category_description: Optional[str]

    class Config:
        from_attributes = True

class TransactionTypeBase(BaseModel):
    transaction_type_id: int
    transaction_type: str
    transaction_type_description: Optional[str]

    class Config:
        from_attributes = True
