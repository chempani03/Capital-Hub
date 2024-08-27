import os
import requests
import logging
from typing import Optional
from fastapi import HTTPException

logger = logging.getLogger("uvicorn.error")

def fetch_forex_rate(from_currency: str,
                     to_currency: str,
                     get_properties : Optional[bool]= None):
    
    logger.info("loading env variables")
    
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY2")
    base_url = os.getenv("ALPHA_VANTAGE_BASE_URL")
    logger.info(f"KEY: {api_key}, URL: {base_url}")
    url = base_url.format(from_currency, to_currency, api_key)
    logger.info(f"URL (FORMATTED): {url}")
    
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch forex data")

    data = response.json()
    logger.info(data)
    
    if "Error Message" in data:
        raise HTTPException(status_code=400, detail=data["Error Message"])

    try:
        output = data["Realtime Currency Exchange Rate"]

    except KeyError as e:
        raise HTTPException(status_code=429, detail= data)  

    try:
        if get_properties:
            return output
        else:
            return {"exchange_rate": output['5. Exchange Rate']}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Cannot parse forex data: {str(e)}")
