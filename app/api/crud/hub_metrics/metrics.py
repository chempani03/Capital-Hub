from typing import Optional
from fastapi.exceptions import HTTPException
from .metrics_logic import *
from app.api.crud.helper_functions import *

def fillter_get_aggr_curr(currency : str,
                          db : Session,
                          decimal : Optional[int] = None
                          ):
    table_name = 'currency'
    column_name = 'currency'
    
    try:
        verify_input(currency, table_name, column_name, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    total_amount = get_total_amount(currency, column_name,db)
    
    if total_amount is None:
        raise HTTPException(status_code=404, detail="No transactions found")
    
    if decimal is not None:
        total_amount = round(total_amount, ndigits=decimal)
    
    return {f"total net amount for currency: {currency}": total_amount}

def get_grouped_data_curr(db: Session,
                          start_date: Optional[datetime] = None,
                        end_date: Optional[datetime] = None,
                        transaction_type: Optional[str] = None,
                        account: Optional[str] = None,
                        category: Optional[str] = None,
                        decimal: Optional[int] = None):
    if start_date is not None and end_date is None:
        raise HTTPException(status_code=422, detail="If datetime parameter is provided, both start_date and end_date should be filled out")
    
    try:
        if start_date is not None and end_date is not None:
            net_data_no_conversion = get_aggregated_amount_by_currency(db=db,
                                                                        startdate=start_date,
                                                                        enddate=end_date,
                                                                        category=category,
                                                                        transaction_type=transaction_type,
                                                                        account=account)
        else:
            start_date, end_date = get_min_max_dates(db)
            net_data_no_conversion = get_aggregated_amount_by_currency(db=db,
                                                                        startdate=start_date,
                                                                        enddate=end_date,
                                                                        category=category,
                                                                        transaction_type=transaction_type,
                                                                        account=account)
        
        if not net_data_no_conversion:
            raise HTTPException(status_code=404, detail="No transactions found for the specified criteria.")
        
        if decimal is not None:
            result = [{"currency": row["currency"], "amount": round(row["amount"], decimal)} for row in net_data_no_conversion]
        else:
            result = [{"currency": row["currency"], "amount": row["amount"]} for row in net_data_no_conversion]
        
        return {"aggregated_amounts": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching data: {str(e)}")
