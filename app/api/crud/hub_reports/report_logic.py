import calendar
import pandas as pd
from datetime import datetime
from fastapi.responses import JSONResponse


def get_monthly_dates(date_str):
    date_obj = datetime.strptime(date_str, "%b %Y")
    
    start_date = datetime(date_obj.year, date_obj.month, 1).strftime("%Y-%m-%d")
    end_date = datetime(date_obj.year, date_obj.month, calendar.monthrange(date_obj.year, date_obj.month)[1]).strftime("%Y-%m-%d")
    
    return start_date, end_date

def prepare_ts_data(ts_json):

    if isinstance(ts_json, dict):
        pass
    elif isinstance(ts_json, JSONResponse):
        ts_json = ts_json.media_type  
    else:
        raise TypeError("Expected dict or JSONResponse")

    credit_df = pd.DataFrame(ts_json['credit']).set_index('booking_date')
    debit_df = pd.DataFrame(ts_json['debit']).set_index('booking_date')
    balance_df = pd.DataFrame(ts_json['net_balance']).set_index('booking_date')

    ts_df = pd.DataFrame({
        'credit': credit_df['cumulative_amount'],
        'debit': debit_df['cumulative_amount'],
        'balance': balance_df['cumulative_amount']
    })
    return ts_df


def prepare_muncher_data(muncher_json):

    if isinstance(muncher_json, dict):
        muncher_json = [muncher_json]  
    elif isinstance(muncher_json, JSONResponse):
        muncher_json = muncher_json.json()  
    elif not isinstance(muncher_json, list):
        raise TypeError("Expected dict, list of dicts, or JSONResponse")
    
    series = pd.Series({k: v for item in muncher_json for k, v in item.items()})
    income_munch_df = series[series>0]
    expense_munch_df = series[series<0]

    return income_munch_df, expense_munch_df
