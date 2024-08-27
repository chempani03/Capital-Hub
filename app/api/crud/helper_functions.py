import pandas as pd
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.inspection import inspect
from .hub.board import get_transactions
from .forex.forex_client import fetch_forex_rate
from ..models.models import *


def verify_input(parameter: str, table_name: str, column_name: str, db: Session):
    model_mapping = {
        'currency': Currency,
        'account': Account,
        'category': Category,
        'transaction_type': TransactionType
    }
    
    model = model_mapping.get(table_name.lower())
    if not model:
        raise HTTPException(status_code=400, detail=f"Invalid table name: {table_name}")

    if column_name not in inspect(model).columns:
        raise HTTPException(status_code=400, detail=f"Invalid column name: {column_name}")

    column = getattr(model, column_name)
    
    if not db.query(model).filter(column == parameter).first():
        accepted_values = [getattr(value, column_name) for value in db.query(model).all()]
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {column_name} value. Accepted values are: {accepted_values}"
        ) 

def get_min_max_dates(db: Session):

    try:
        min_date = db.query(func.min(TransOverView.booking_date)).scalar()
        max_date = db.query(func.max(TransOverView.booking_date)).scalar()
        
        if not min_date or not max_date:
            return None, None
        
        return min_date, max_date

    except Exception as e:
        return None, None
    

def obtain_data_to_convert(currency_of_interest : str,
                           db : Session,
                           start_date : Optional[str] = None,
                           end_date : Optional[str] = None):
    
    table_name_currency = 'currency'
    column_name_currency = 'currency'

    try:
        verify_input(currency_of_interest,table_name_currency,column_name_currency,db)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error verifying parameter: {str(e)}")

    if start_date is not None and end_date is None:
        raise HTTPException(status_code=422, detail="If datetime parameter is provided, both start_date and end_date should be filled out")

    if start_date is not None and end_date is not None:
        
        try:
            data = get_transactions(db=db,startdate=start_date,enddate=end_date)

        except Exception as e:
         raise HTTPException(status_code=400, detail=f"Error fetching data for the specified date range: {str(e)}")

    else:
        try:
            start_date, end_date = get_min_max_dates(db)
            
            data = get_transactions(db=db, startdate=start_date, enddate=end_date)

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error fetching data for the default date range: {str(e)}")

    df = pd.DataFrame([d.__dict__ for d in data])

    if "_sa_instance_state" in df.columns:
        df.drop(columns=["_sa_instance_state"], inplace=True)

    return df


def convert_df_to_currency(df, currency_of_interest,forex_map):

    def convert_row(row):
        curr_to_convert = row['currency']
        if curr_to_convert != currency_of_interest:
            amount_to_convert = row['amount']
            row['amount'] = float(amount_to_convert) * float(forex_map[curr_to_convert])
        return row

    df = df.apply(lambda row: convert_row(row), axis=1)

    return df


def create_map_forex(df,currency_of_interest):

    unique_currencies = df['currency'].unique().tolist()
    map_currency_rate = {}

    for currency in unique_currencies:

        if currency == currency_of_interest:
            continue
        else:
            rate = fetch_forex_rate(currency,currency_of_interest)
        
        map_currency_rate[currency] = rate['exchange_rate']

    return map_currency_rate
