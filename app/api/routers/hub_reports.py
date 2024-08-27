from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from typing import Literal
from app.api.crud.hub_reports.report import monthly_report

router = APIRouter(
    prefix="/reports",
    tags=["Capital Hub Reports"])

@router.post("/monthly_reports/")
def get_monthy_reports(month : 
                       Literal[
                                    'Jan',
                                    'Feb',
                                    'Mar',
                                    'Apr',
                                    'May',
                                    'Jun',
                                    'Jul',
                                    'Aug',
                                    'Sep',
                                    'Oct',
                                    'Nov',
                                    'Dec'
                                ],
                        year : 
                        Literal[
                            '2024',
                            '2025',
                            '2025'
                        ],
                        currency_of_interest : str,
                        db : Session = Depends(get_db)):
    
    return monthly_report(month,
                          year,
                          currency_of_interest,
                          db)