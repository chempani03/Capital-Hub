from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException 
from fastapi.responses import JSONResponse
from typing import Optional 
from app.api.crud.hub_metrics.metrics_logic import get_aggregated_amount_by_currency
from app.api.crud.helper_functions import *
from .insight_skeleton import *
from .insight_logic import *
from ...models.models import *

def get_net_balance(currency_of_interest: str,
                    db: Session, 
                    start_date: Optional[str] = None,
                    end_date: Optional[str] = None,
                    decimal: Optional[int] = None):
    
    table_name = 'currency'
    column_name = 'currency'
    
    try:
        verify_input(currency_of_interest, table_name, column_name, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error verifying currency input: {str(e)}")
    
    if start_date is not None and end_date is None:
        raise HTTPException(status_code=422, detail="If datetime parameter is provided, both start_date and end_date should be filled out")
    
    if start_date is not None and end_date is not None:
        try:
            net_data_no_conversion = get_aggregated_amount_by_currency(db=db,
                                                                       startdate=start_date,
                                                                       enddate=end_date)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error fetching data for the specified date range: {str(e)}")
    else:
        try:
            start_date, end_date = get_min_max_dates(db)
            net_data_no_conversion = get_aggregated_amount_by_currency(db=db,
                                                                       startdate=start_date,
                                                                       enddate=end_date)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error getting grouped data: {str(e)}. Dates are: {start_date}, {end_date}")
    
    try:
        total_amount = convert_aggregated_amounts(net_data_no_conversion, currency_of_interest)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error converting aggregated amounts: {str(e)}")
    
    if decimal is not None:
        total_amount = round(total_amount, ndigits=decimal)

    return {f"Total Amount ({currency_of_interest})": total_amount}

def get_category_expenditure(category: str,
                             db: Session,
                            currency_of_interest : str,
                            start_date: Optional[datetime] = None,
                            end_date: Optional[datetime] = None,
                            decimal: Optional[int] = None,
                             ):
    table_name_category = 'category'
    column_name_category = 'category'
    
    table_name_currency = 'currency'
    column_name_currency = 'currency'

    try:
        verify_input(category, table_name_category, column_name_category, db)
        verify_input(currency_of_interest,table_name_currency,column_name_currency,db)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error verifying parameter: {str(e)}")

    if start_date is not None and end_date is None:
        raise HTTPException(status_code=422, detail="If datetime parameter is provided, both start_date and end_date should be filled out")
    
    if start_date is not None and end_date is not None:
        try:
            net_data_no_conversion = get_aggregated_amount_by_currency(db=db,
                                                                            startdate=start_date,
                                                                            enddate=end_date,
                                                                            category=category)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error fetching data for the specified date range: {str(e)}")
    else:
        try:
            start_date, end_date = get_min_max_dates(db)
            net_data_no_conversion = get_aggregated_amount_by_currency(db=db,
                                                                            startdate=start_date,
                                                                            enddate=end_date,
                                                                            category=category)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error fetching data for the default date range: {str(e)}")

    try:
        total_amount = convert_aggregated_amounts(net_data_no_conversion, currency_of_interest)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error converting aggregated amounts: {str(e)}")
    
    if decimal is not None:
        total_amount = round(total_amount, ndigits= 2)

    return {f"Total Amount ({category})": total_amount}

def calculate_full_category_expenditure(currency_of_interest : str,
                                        db: Session,
                                        order : str,
                                        start_date : Optional[datetime] = None,
                                        end_date : Optional[datetime] = None,
                                        decimal : Optional[int] = None):
    order_map = {'asc': True,
                 'desc' : False}

    order_output = order_map[order]

    df = obtain_data_to_convert(currency_of_interest,db,start_date,end_date)

    dict_map_forex = create_map_forex(df,currency_of_interest)

    converted_data = convert_df_to_currency(df,currency_of_interest,dict_map_forex)

    response = full_muncher_skeleton(converted_data,order_output,decimal)

    return JSONResponse(response)

def calculate_timeseries(currency_of_interest : str,
                        db : Session,
                        granularity: str,
                        start_date : Optional[str] = None,
                        end_date : Optional[str] = None,
                        decimal : Optional[int] = None ):
    
    df = obtain_data_to_convert(currency_of_interest,db,start_date,end_date)

    dict_map_forex = create_map_forex(df,currency_of_interest)

    converted_data = convert_df_to_currency(df,currency_of_interest,dict_map_forex)

    response = timeseries_skeleton(converted_data,granularity,decimal)

    return JSONResponse(response)