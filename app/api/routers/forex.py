from fastapi import APIRouter
from app.api.crud.forex.forex_client import fetch_forex_rate 
from typing import Optional

router = APIRouter(
    prefix="/api",
    tags=["Forex"],
)

@router.get("/get_forex_rate/", tags=["Forex"])
def get_forex_data(from_currency: str,
                   to_currency: str,
                   get_properties : Optional[bool] = None):
    """
    Retrieve the forex exchange rate between two currencies. FOREX data comes from: https://www.alphavantage.co/
    
    - WARNING: forex data can only have 25 calls per day.

    Parameters:
    - from_currency (str): The base currency.
    - to_currency (str): The target currency.

    Returns:
    - JSON response with the exchange rate information.

    Raises:
    - HTTPException 400: If the request to Alpha Vantage fails.
    """
    return fetch_forex_rate(from_currency, to_currency, get_properties)
