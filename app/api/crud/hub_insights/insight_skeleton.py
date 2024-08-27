import pandas as pd
from .insight_logic import *

def full_muncher_skeleton(converted_df,
                          order_output,
                          decimal):
    
    grouped_data = converted_df.groupby('category')['amount'].sum()
    
    if order_output:
        grouped_data = grouped_data.sort_values(ascending=True)
    else:
        grouped_data = grouped_data.sort_values(ascending=False)

    if decimal is not None:
        result = grouped_data.apply(lambda x: round(x, ndigits=decimal))

    result_json = {
        category: amount
        for category, amount in result.items()
    }
    return result_json

def timeseries_skeleton(converted_df,
                        granularity,
                        decimal):
    
    credit_df , debit_df = get_credit_debit_data(converted_df)

    credit_cumsum = aggregate_and_cumulate(credit_df,granularity)
    debit_cumsum = aggregate_and_cumulate(debit_df,granularity)

    credit_cumsum = convert_timestamps_to_str(credit_cumsum)
    debit_cumsum = convert_timestamps_to_str(debit_cumsum)

    net_cumsum = credit_cumsum.copy()
    net_cumsum['cumulative_amount'] = credit_cumsum['cumulative_amount'] + debit_cumsum['cumulative_amount']

    if decimal is not None:
        credit_cumsum['cumulative_amount'] = credit_cumsum['cumulative_amount'].apply(lambda x: round(x, ndigits=decimal))
        debit_cumsum['cumulative_amount'] = debit_cumsum['cumulative_amount'].apply(lambda x: round(x, ndigits=decimal))
        net_cumsum['cumulative_amount'] = net_cumsum['cumulative_amount'].apply(lambda x: round(x, ndigits=decimal))

    json_response = {
        "credit": credit_cumsum.to_dict(orient="records"),
        "debit": debit_cumsum.to_dict(orient="records"),
        "net_balance": net_cumsum.to_dict(orient="records")
    }

    return json_response