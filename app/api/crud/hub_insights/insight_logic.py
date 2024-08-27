import pandas as pd
from fastapi import HTTPException
from ..forex.forex_client import fetch_forex_rate

def convert_aggregated_amounts(grouped_data,currency_of_interest):
   
    df = pd.json_normalize(grouped_data)
    data_with_currency = df[df['currency'] == currency_of_interest]
    data_without_currency = df[df['currency'] != currency_of_interest]
    
    unique_currencies = data_without_currency['currency'].unique().tolist()
    
    try:
        total_amount = data_with_currency['amount'].values[0]
    
    except IndexError:
        total_amount = 0
    
    aggregated_amount = total_amount

    return get_aggregated_amount(unique_currencies,currency_of_interest,data_without_currency,aggregated_amount)

def get_aggregated_amount(unique_currencies,currency_of_interest, data_wout_curr,amount):
    
    for currency in unique_currencies:

        try:
            amount_to_convert = data_wout_curr[data_wout_curr['currency'] == currency]['amount'].values[0]
        
        except IndexError as e:
            raise e
        
        try:

            rate_data = fetch_forex_rate(currency,currency_of_interest)
            conversion_rate = float(rate_data['exchange_rate'])

            converted_amount = conversion_rate * amount_to_convert
            amount += converted_amount
        
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error fetching conversion rate or converting amount for currency {currency}: {str(e)}")
    
    return amount




def get_credit_debit_data(df):
    cols_of_interest = ['booking_date', 'amount']

    df['booking_date'] = df['booking_date'].apply(lambda x: pd.to_datetime(x))

    cred_df = df[df['transaction_type'] == 'Credit'][cols_of_interest].set_index('booking_date')
    cred_df.index = cred_df.index.normalize()

    debit_df = df[df['transaction_type'] == 'Debit'][cols_of_interest].set_index('booking_date')
    debit_df.index = debit_df.index.normalize()

    cred_df,debit_df = extrapolate_datetime(cred_df,debit_df)
    print(cred_df,debit_df,flush=True)
    return cred_df, debit_df

def extrapolate_datetime(df1, df2):

    all_dates = pd.date_range(start=min(df1.index.min(), df2.index.min()), 
                                end=max(df1.index.max(), df2.index.max()))
    
    def reindex_data(df,indexes):
        df = df.groupby(df.index)['amount'].sum()
        df_full = df.reindex(indexes,fill_value = 0)
        df_full = df_full.ffill().bfill()

        return df_full
    
    df1_full = reindex_data(df1,all_dates)
    df2_full = reindex_data(df2,all_dates)

    return df1_full,df2_full

def aggregate_and_cumulate(df, granularity):

    if granularity == 'daily':
        df_grouped = df.resample('D').agg({'amount': 'sum'}).asfreq('D', fill_value=0).reset_index()
    elif granularity == 'weekly':
        df_grouped = df.resample('W-MON').agg({'amount': 'sum'}).asfreq('W-MON', fill_value=0).reset_index()
    elif granularity == 'monthly':
        df_grouped = df.resample('M').agg({'amount': 'sum'}).asfreq('M', fill_value=0).reset_index()
    else:
        raise ValueError("Invalid granularity. Use 'daily', 'weekly', or 'monthly'.")

    df_grouped['cumulative_amount'] = df_grouped['amount'].cumsum()

    return df_grouped.drop('amount',axis =1)

def convert_timestamps_to_str(df):
    """Convert all Timestamp index in the DataFrame to ISO format strings."""
    if isinstance(df.index, pd.DatetimeIndex):
        df.index = df.index.strftime('%Y-%m-%d')
    
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime('%Y-%m-%d')
            df.rename(columns={col: 'booking_date'}, inplace=True)
    
    return df