from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional , List
from datetime import datetime
from app.api.crud.hub.board import *
from app.api.database import engine, Base
from app.api.dependencies import get_db
from ..schemas.child_schemas import *
from ..schemas.schemas import *

router = APIRouter(
    prefix="/hub",
    tags=["Capital Hub"])

Base.metadata.create_all(bind=engine)


@router.get("/transactions_full/",response_model= List[TransOverViewBase])
def read_all_transactions(db: Session = Depends(get_db)):
    """
    Retrieve all transactions in the system.

    This endpoint fetches all the transactions recorded in the database, providing a comprehensive overview of all financial activities.
    """
    
    return get_overview(db)

@router.get("/transactions/",response_model= List[TransOverViewBase])
def read_filtered_transactions(
    startdate: datetime = Query(...),
    enddate: datetime = Query(...),
    currency: Optional[str] = Query(None),
    transaction_type: Optional[str] = Query(None),
    account: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Retrieve filtered transactions based on specified parameters.

    This endpoint allows you to filter transactions by date range, currency, transaction type, 
    account, and category.

    Parameters:
    - startdate (datetime): The start date for filtering transactions.
    - enddate (datetime): The end date for filtering transactions.
    - currency (str, optional): The currency to filter transactions by.
    - transaction_type (str, optional): The type of transaction to filter by (e.g., Debit, Credit).
    - account (str, optional): The account to filter transactions by.
    - category (str, optional): The category to filter transactions by.

    Returns:
    - List[TransOverViewBase]: A list of filtered transaction records.
    """
    return get_transactions(db, startdate, enddate, currency, transaction_type, account, category)

@router.get("/transaction/{transaction_id}/", response_model=List[TransOverViewBase])
def read_transaction_by_id(transaction_id:str,
                           db : Session = Depends(get_db)):
    """
    Retrieve a single transaction by its ID.

    This endpoint allows you to fetch the details of a specific transaction using its unique identifier.

    Parameters:
    - transaction_id (str): The unique ID of the transaction to retrieve.
    - db (Session, optional): The database session dependency.

    Returns:
    - TransOverView: The details of the transaction with the specified ID.
    """
    
    return get_transaction_by_id(transaction_id, db)

@router.post("/post_transactions/")
def create_new_transaction(
    booking_date: datetime = Query(...),
    value_date: datetime = Query(...),
    amount: float = Query(...),
    currency: str = Query(...),
    transaction_type: str = Query(...),
    account: str = Query(...),
    category: str = Query(...),
    booking_text: Optional[str] = Query(None, example="Description of the transaction"),
    db: Session = Depends(get_db)
):
    """
    Create a new transaction.

    This endpoint allows you to add a new financial transaction by providing details such as booking date, 
    value date, amount, currency, transaction type, account, category, and an optional booking text.

    Parameters:
    - booking_date (datetime): The date the transaction was booked.
    - value_date (datetime): The value date of the transaction.
    - amount (float): The amount of the transaction.
    - currency (str): The currency in which the transaction was made.
    - transaction_type (str): The type of transaction (e.g., Credit, Debit).
    - account (str): The account associated with the transaction.
    - category (str): The category associated with the transaction.
    - booking_text (str, optional): Additional details or description of the transaction.

    Returns:
    - TransOverViewBase: The newly created transaction record.

    Raises:
    - HTTPException: If the transaction could not be created or if the amount is invalid for the transaction type.
    """
    return perform_new_transaction(
        db=db,
        booking_date=booking_date,
        value_date=value_date,
        amount=amount,
        currency=currency,
        transaction_type=transaction_type,
        account=account,
        category=category,
        booking_text=booking_text
    )

@router.post("/post_transactions_between_accounts/")
def create_transaction_between_accounts(
    booking_date: datetime = Query(...),
    value_date: datetime = Query(...),
    amount: float = Query(...),
    sender_account: str = Query(...),
    receiver_account: str = Query(...),
    currency: str = Query(...),
    fee: Optional[int] = Query(None),
    booking_text: Optional[str] = Query(None, example="Additional Text for reference"),
    db: Session = Depends(get_db)
):
    """
    Create a transaction between two accounts.

    This endpoint allows you to create a transaction that transfers funds from one account 
    to another, with an optional fee and booking text. The transaction creates separate 
    entries for the sender and receiver accounts.

    Parameters:
    - booking_date (datetime): The date the transaction was booked.
    - value_date (datetime): The value date of the transaction.
    - amount (float): The amount being transferred.
    - sender_account (str): The account from which funds are being sent.
    - receiver_account (str): The account to which funds are being received.
    - currency (str): The currency in which the transaction was made.
    - fee (int, optional): An optional fee associated with the transaction.
    - booking_text (str, optional): Additional details or description of the transaction.

    Returns:
    - str: A message indicating the IDs of the transactions created.

    Raises:
    - HTTPException: If the transaction could not be created or if there is an error during processing.
    """
    return perform_transaction_between_accounts(
        db=db,
        booking_date=booking_date,
        value_date=value_date,
        amount=amount,
        sender_account=sender_account,
        receiver_account=receiver_account,
        currency=currency,
        fee=fee,
        booking_text=booking_text
    )

@router.delete("/transactions/{transaction_id}/")
def delete_transaction_id(transaction_id: str,
                          db: Session = Depends(get_db)):
    """
    Delete a transaction by its ID.

    This endpoint allows you to delete a transaction by providing its ID. If the transaction does not exist, 
    it returns a 404 error.

    Parameters:
    - transaction_id (str): The ID of the transaction to be deleted.

    Returns:
    - dict: A dictionary containing the result of the deletion.

    Raises:
    - HTTPException 404: If the transaction with the specified ID does not exist.
    """
    return delete_transaction(db,transaction_id)


@router.put("/update_transaction/{transaction_id}/")
def update_transaction(transaction_id: str,
                       transaction_update: TransactionUpdate,
                       db: Session = Depends(get_db)):
    """
    Endpoint to update a transaction in the TransOverView table.

    Args:
        transaction_id (str): The ID of the transaction to update.
        transaction_update (TransactionUpdate): A Pydantic model containing
                                                the fields to update.
        db (Session): The database session.

    Returns:
        TransOverView: The updated transaction object.
    """
    return perform_transaction_update(transaction_id, transaction_update, db)
