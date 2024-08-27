from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.api.crud.hub_metrics.metrics import *
from typing import Optional
from datetime import datetime

router = APIRouter(
    prefix="/metrics",
    tags=["Capital Hub Metrics"])


@router.get("/aggregated_amount_currency/")
def get_aggregated_amount_currency(currency: str,
                          decimal: Optional[int] = None,
                          db: Session = Depends(get_db)):
    """
    Retrieve the total aggregated transaction amount for a specified currency.

    Parameters:
    - currency (str): The currency code to aggregate transactions for.
    - decimal (Optional[int]): Number of decimal places to round the result to (optional).

    Returns:
    - JSON response with the total aggregated amount for the specified currency.

    Raises:
    - HTTPException 400: If the currency or column is not valid.
    """
    return fillter_get_aggr_curr(currency=currency,db=db,decimal=decimal)

@router.get("/aggregated_amount_filltered_currency/")
def get_aggregated_amount_grouped_by(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    transaction_type: Optional[str] = None,
    account: Optional[str] = None,
    category: Optional[str] = None,
    decimal: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve the total aggregated transaction amount by currency within a date range.
    
    Parameters:
    - start_date (datetime): The start date for filtering transactions.
    - end_date (datetime): The end date for filtering transactions.
    - transaction_type (Optional[str]): The transaction type to filter transactions by (optional).
    - account (Optional[str]): The account to filter transactions by (optional).
    - category (Optional[str]): The category to filter transactions by (optional).
    - decimal (Optional[int]): Number of decimal places to round the result to (optional).

    Returns:
    - JSON response with the total aggregated amount for each currency within the specified date range.
    """
    return get_grouped_data_curr(db=db,
                                 start_date=start_date,
                                 end_date=end_date,
                                 transaction_type=transaction_type,
                                 account=account,
                                 category=category,
                                 decimal=decimal)