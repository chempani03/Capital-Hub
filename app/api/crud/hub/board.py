import uuid
from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from typing import Optional, List
from ...schemas.schemas import TransOverViewBase
from ...models.models import *
from ...schemas.child_schemas import *

def get_overview(db: Session):
    return db.query(TransOverView).order_by(TransOverView.booking_date.desc()).all()

def perform_new_transaction(db: Session,
                       booking_date : datetime,
                       value_date : datetime,
                       amount : float,
                       currency : str,
                       transaction_type : str,
                       account : str,
                       category : str,
                       booking_text : Optional[str]):
    
    if transaction_type == 'Debit':
        if amount > 0:
            return ValueError("Debit should be negative")
        
    id = uuid.uuid4()
    data_to_add = TransOverViewBase(
        transaction_id= str(id),
        booking_date= booking_date,
        value_date= value_date,
        amount= amount,
        currency=currency,
        transaction_type= transaction_type,
        account= account,
        category= category,
        booking_text= booking_text
    )

    db_transaction = TransOverView(
        transaction_id=data_to_add.transaction_id,
        booking_date=data_to_add.booking_date,
        value_date=data_to_add.value_date,
        amount=data_to_add.amount,
        currency=data_to_add.currency,
        transaction_type=data_to_add.transaction_type,
        account=data_to_add.account,
        category=data_to_add.category,
        booking_text=data_to_add.booking_text
    )
    if db_transaction is None:
        return HTTPException(status_code=400, detail="Transaction could not be created")
    
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def perform_transaction_between_accounts(
    booking_date: datetime,
    value_date: datetime,
    amount: float,
    sender_account: str,
    receiver_account: str,
    currency: str,
    db: Session,
    fee: Optional[int] = None,
    booking_text: Optional[str] = None
) -> List[str]:
    try:
        id_out = str(uuid.uuid4())
        id_in = str(uuid.uuid4())

        text = f"Transaction from {sender_account} to {receiver_account}. Amount Sent: {amount}."
        if booking_text:
            text += f" {booking_text}"

        transaction_type = "Transaction between Accounts"
        category = "Transaction Between Accounts"
        list_ids = []

        transaction_data_account_out = TransOverViewBase(
            transaction_id=id_out,
            booking_date=booking_date,
            value_date=value_date,
            amount=amount * -1,
            currency=currency,
            transaction_type=transaction_type,
            account=sender_account,
            category= category,
            booking_text=text
        )

        db_transaction_out = perform_new_transaction(db, transaction_data_account_out)
        if db_transaction_out is None:
            raise HTTPException(status_code=400, detail="Transaction could not be created")
        list_ids.append(id_out)

        transaction_data_account_in = TransOverViewBase(
            transaction_id=id_in,
            booking_date=booking_date,
            value_date=value_date,
            amount=amount,
            currency=currency,
            transaction_type=transaction_type,
            account=receiver_account,
            category=category,
            booking_text=text
        )
        db_transaction_in = perform_new_transaction(db, transaction_data_account_in)
        if db_transaction_in is None:
            raise HTTPException(status_code=400, detail="Transaction could not be created")
        list_ids.append(id_in)

        # Handle fee if applicable
        if fee is not None:
            id_fee = str(uuid.uuid4())
            fee_text = f"{booking_text} FEE: {fee}" if booking_text else f"FEE: {fee}"
            transaction_data_account_out_fee = TransOverViewBase(
                transaction_id=id_fee,
                booking_date=booking_date,
                value_date=value_date,
                amount=fee * -1,
                currency=currency,
                transaction_type="Debit",
                account=sender_account,
                category=category,
                booking_text=fee_text
            )
            db_transaction_fee = perform_new_transaction(db, transaction_data_account_out_fee)
            if db_transaction_fee is None:
                raise HTTPException(status_code=400, detail="Transaction could not be created")
            list_ids.append(id_fee)

        return f"IDS added {list_ids}"

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_transactions(db: Session, 
                     startdate: datetime, 
                     enddate: datetime, 
                     currency: str = None, 
                     transaction_type: str = None, 
                     account: str = None, 
                     category: str = None):
    
    query = db.query(TransOverView).filter(
        and_(
            TransOverView.booking_date >= startdate,
            TransOverView.booking_date <= enddate
        )
    )

    if currency:
        query = query.filter(TransOverView.currency == currency)
    
    if transaction_type:
        query = query.filter(TransOverView.transaction_type == transaction_type)
    
    if account:
        query = query.filter(TransOverView.account == account)
    
    if category:
        query = query.filter(TransOverView.category == category)
    
    return query.order_by(TransOverView.booking_date.desc()).all()

def get_transaction_by_id(transaction_id : str,
                          db: Session):
    transaction = db.query(TransOverView).filter(TransOverView.transaction_id == transaction_id).first()

    if not transaction:
        raise HTTPException(status_code=404,detail="Transaction ID not found")

    return transaction


def delete_transaction(db: Session, transaction_id: str):
    # Check if the transaction exists
    transaction = db.query(TransOverView).filter(TransOverView.transaction_id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404,detail="Transaction ID not found")

    # Delete the transaction
    db.delete(transaction)
    db.commit()

    return {"message": f"Transaction ID: {transaction_id} deleted successfully"}


def perform_transaction_update(transaction_id : str,
                               transaction_update : TransactionUpdate,
                               db : Session):
    from ...crud.helper_functions import verify_input
    
    db_transaction = db.query(TransOverView).filter(TransOverView.transaction_id == transaction_id).first()
    
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    update_data = transaction_update.dict(exclude_unset=True)
    
    # Validate foreign key fields
    if "currency" in update_data:
        verify_input(update_data["currency"], "currency", "currency", db)
    
    if "transaction_type" in update_data:
        verify_input(update_data["transaction_type"], "transaction_type", "transaction_type", db)
    
    if "account" in update_data:
        verify_input(update_data["account"], "account", "account", db)
    
    if "category" in update_data:
        verify_input(update_data["category"], "category", "category", db)
    
    # Track if any field is actually updated
    is_updated = False

    # Iterate through the fields in the update data
    for key, value in update_data.items():
        if getattr(db_transaction, key) != value:
            setattr(db_transaction, key, value)
            is_updated = True

    # If any updates were made, commit them to the database
    if is_updated:
        db.commit()
        db.refresh(db_transaction)

    return db_transaction