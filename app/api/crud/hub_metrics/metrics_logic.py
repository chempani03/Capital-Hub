from datetime import datetime
from sqlalchemy import and_ , func
from sqlalchemy.orm import Session
from ...models.models import *

def get_total_amount(parameter_of_interest: str,
                    column_name: str,
                    db: Session) -> float:
    
    column = getattr(TransOverView, column_name)
    query = db.query(func.sum(TransOverView.amount)).filter(column == parameter_of_interest)
    
    total_amount = query.scalar() or 0.0
    return total_amount

def get_aggregated_amount_by_currency(db: Session, 
                                      startdate: datetime, 
                                      enddate: datetime, 
                                      transaction_type: str = None, 
                                      account: str = None, 
                                      category: str = None,
                                      decimal: int = None):
    query = db.query(
        TransOverView.currency,
        func.sum(TransOverView.amount).label("amount")
    ).filter(
        and_(
            TransOverView.booking_date >= startdate,
            TransOverView.booking_date <= enddate
        )
    )

    if transaction_type:
        query = query.filter(TransOverView.transaction_type == transaction_type)
    
    if account:
        query = query.filter(TransOverView.account == account)
    
    if category:
        query = query.filter(TransOverView.category == category)
    
    query = query.group_by(TransOverView.currency)
    
    result = query.all()
    
    if decimal:
        aggregated_amounts = [{"currency": row[0], "amount": round(row[1],ndigits=decimal)} for row in result]
    else:
        aggregated_amounts = [{"currency": row[0], "amount": row[1]} for row in result]

    return aggregated_amounts