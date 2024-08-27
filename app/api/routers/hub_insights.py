from fastapi import APIRouter, Depends
from app.api.crud.hub_insights.insight import *
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from typing import Literal

router = APIRouter(
    prefix="/insights",
    tags=["Capital Hub Insights"])

@router.get("/net_balance/")
def net_balance(currency_of_interest: str,
                start_date: str = None,
                end_date: str = None,
                decimal: int = None,
                db: Session = Depends(get_db)):
    """
    Retrieve the net balance for a specified currency of interest.
    
    Parameters:
    - currency_of_interest (str): The currency to get the net balance for.
    - start_date (datetime, optional): The start date for the range.
    - end_date (datetime, optional): The end date for the range.

    Returns:
    - JSON response with the aggregated net balance information.

    Raises:
    - HTTPException 422: If end_date is provided without start_date.
    - HTTPException 400: If there is an error during processing.
    """
    return get_net_balance(currency_of_interest=currency_of_interest,
                           start_date=start_date,
                           end_date=end_date,
                           decimal=decimal,
                           db=db)

@router.get("/category_muncher/")
def category_expenditure(category: str,
                         currency_of_interest: str,
                         start_date: str = None,
                         end_date: str = None,
                         decimal: int = None,
                         db: Session = Depends(get_db)):
    """
    Retrieve the total amount for a specified category within the date range.
    
    Parameters:
    - category (str): The category to get the total amount for.
    - start_date (datetime, optional): The start date for the range.
    - end_date (datetime, optional): The end date for the range.

    Returns:
    - JSON response with the total amount for the category.

    Raises:
    - HTTPException 422: If end_date is provided without start_date.
    - HTTPException 400: If there is an error during processing.
    """
    return get_category_expenditure(category=category,
                                    currency_of_interest=currency_of_interest,
                                    start_date=start_date,
                                    end_date=end_date,
                                    decimal=decimal,
                                    db=db)

@router.get("/muncher_full_overview/")
def full_category_expenditure(currency_of_interest: str,
                              order: Literal['asc','desc'],
                              start_date: str = None,
                              end_date: str = None,
                              decimal: int = None,
                              db: Session = Depends(get_db)):
    """
    Retrieve a full overview of aggregated net amounts by category within an optional date range.

    This endpoint provides a comprehensive view of the net amounts grouped by category 
    for the specified currency. If a date range is provided, only transactions within 
    that range are considered. The results can be sorted in ascending or descending order 
    and rounded to a specified number of decimal places.

    Parameters:
    - currency_of_interest (str): The currency to display the total amounts in.
    - order (str): The order to sort the categories by amount ('asc' for ascending, 'desc' for descending).
    - start_date (datetime, optional): The start date for the transaction range.
    - end_date (datetime, optional): The end date for the transaction range.
    - decimal (int, optional): The number of decimal places to round the amounts to.
    - db (Session): The database session dependency.

    Returns:
    - JSON: A list of dictionaries, each containing a category and its corresponding total amount.

    Raises:
    - HTTPException 422: If end_date is provided without start_date.
    - HTTPException 400: If there is an error during processing or verification.
    """
    return calculate_full_category_expenditure(currency_of_interest=currency_of_interest,
                                               order=order,
                                               start_date=start_date,
                                               end_date=end_date,
                                               decimal=decimal,
                                               db=db)

@router.get("/timeseries/")
def timeseries_finances(currency_of_interest: str,
               granularity : Literal['daily', 'weekly', 'monthly'],
               start_date: str = None,
               end_date: str = None,
               decimal: int = None,
               db: Session = Depends(get_db)):
    """
    Retrieve a cumulative balance time series for transactions within a specified date range, 
    aggregated by the specified granularity.

    This endpoint provides a detailed view of cumulative credit, debit, and net balance amounts over time, 
    grouped by the specified granularity (daily, weekly, or monthly) for the chosen currency. 
    If a date range is provided, only transactions within that range are considered. 
    The cumulative amounts can also be rounded to a specified number of decimal places.

    Parameters:
    - currency_of_interest (str): The currency in which to display the transaction amounts.
    - granularity (str, optional): The level of detail for the time series aggregation.
        - "daily": Aggregate by day.
        - "weekly": Aggregate by week.
        - "monthly": Aggregate by month.
        Defaults to "daily".
    - start_date (str, optional): The start date for the transaction range (format: 'YYYY-MM-DD'). 
        Must be provided if `end_date` is specified.
    - end_date (str, optional): The end date for the transaction range (format: 'YYYY-MM-DD'). 
        Must be provided if `start_date` is specified.
    - decimal (int, optional): The number of decimal places to round the cumulative amounts to.
    - db (Session): The database session dependency.

    Returns:
    - JSONResponse: A JSON object containing the cumulative credit, debit, and net balance time series.
        The response includes the following structure:
        - "credit": A list of records with the booking date, transaction amount, and cumulative amount.
        - "debit": A list of records with the booking date, transaction amount, and cumulative amount.
        - "net_balance": A list of records with the booking date and the cumulative net balance (difference between credit and debit).

    Raises:
    - HTTPException 422: If only one of `start_date` or `end_date` is provided.
    - HTTPException 400: If there is an error during processing, verification, or data retrieval.
    """
    return calculate_timeseries(currency_of_interest=currency_of_interest,
                                granularity=granularity,
                                start_date=start_date,
                                end_date=end_date,
                                decimal=decimal,
                                db=db)
