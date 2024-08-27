import json
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from ..hub_reports.report_generator import plot_monthly_report
from ..hub_reports.report_logic import *
from ..hub_insights.insight_skeleton import *
from ..helper_functions import *


def monthly_report(month : str,
                    year : str,
                    currency_of_interest : str, 
                    db : Session):
    
    date_str = month + " " + year
    start_date, end_date = get_monthly_dates(date_str)

    data = obtain_data_to_convert(currency_of_interest=currency_of_interest,
                                  db=db,
                                  start_date=start_date,
                                  end_date=end_date)
    if data.empty:
        raise HTTPException(status_code=204, detail= f"No Data Found for date : {date_str}")
    
    forex_map = create_map_forex(data,currency_of_interest)

    converted_data = convert_df_to_currency(data,currency_of_interest,forex_map)

    timeseries_json = timeseries_skeleton(converted_data,
                                          granularity='daily',
                                          decimal=2)
    ts_df = prepare_ts_data(timeseries_json)

    category_muncher_json = full_muncher_skeleton(converted_df=converted_data,
                                          order_output='desc',
                                          decimal=2)
    income_munch_df , expense_munch_df = prepare_muncher_data(category_muncher_json)

    with open('app/api/crud/hub_reports/report_style.json', 'r') as f:
        style_json = json.load(f)

    buffer = plot_monthly_report(ts_df,income_munch_df,expense_munch_df,style_json,date_str,currency_of_interest)

    filepath_date_str = date_str.lower().replace(' ', '_')

    buffer.seek(0)

    return StreamingResponse(buffer, media_type="application/pdf", headers={
        "Content-Disposition": f"attachment;filename=financial_metrics_report_{filepath_date_str}_.pdf"
    })
