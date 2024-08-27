from sqlalchemy import inspect
from app.api.database import engine
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from app.api.crud.hub_configs.config_helper import *
from app.api.crud.hub_configs.config import *
from ...schemas.schemas import CategoryBase, CurrencyBase, TransactionTypeBase, AccountBase


def get_table_names():
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    return table_names
    
def get_table_configs(table_name : str, 
                      db:Session):
   
    model, id_col = map_table_param(table_name)
    
    return db.query(model).order_by(id_col.asc()).all()

def post_new_account_config(config_name : str,
                            config_descr : str,
                            db : Session ):
    last_id = get_last_id(model=Account, column='account_id', db=db)
    new_id = last_id + 1 if last_id is not None else 1  
    
    config_data = AccountBase(
        account=config_name,
        account_id=new_id,
        account_description=config_descr
    )
    config_insertion = post_config_account(db, config_data)
    
    if config_insertion is None:
        raise HTTPException(status_code=400, detail="Transaction could not be created")
    
    return config_insertion

def commit_new_category(config_name : str,
                        config_descr : str,
                        db : Session):
    last_id = get_last_id(model=Category, column='category_id', db=db)
    new_id = last_id + 1 if last_id is not None else 1  
    
    config_data = CategoryBase(
        category=config_name,
        category_id=new_id,
        category_description=config_descr
    )
    config_insertion = post_config_category(db, config_data)
    
    if config_insertion is None:
        raise HTTPException(status_code=400, detail="Transaction could not be created")
    
    return config_insertion

def commit_new_currency(config_name : str,
                        config_descr : str,
                        db : Session):
    last_id = get_last_id(model=Currency, column='currency_id', db=db)
    new_id = last_id + 1 if last_id is not None else 1  
    
    config_data = CurrencyBase(
        currency=config_name,
        currency_id=new_id,
        currency_description=config_descr
    )
    config_insertion = post_config_currency(db, config_data)
    
    if config_insertion is None:
        raise HTTPException(status_code=400, detail="Transaction could not be created")
    
    return config_insertion

def commit_new_transaction_type(config_name : str,
                                config_descr : str,
                                db : Session):
    last_id = get_last_id(model=TransactionType, column="transaction_type_id", db=db)
    new_id = last_id + 1 if last_id is not None else 1  
    
    config_data = TransactionTypeBase(
        transaction_type=config_name,
        transaction_type_id=new_id,
        transaction_type_description=config_descr
    )
    config_insertion = post_config_transaction_type(db,config_data)
    if config_insertion is None:
        raise HTTPException(status_code=400, detail="Transaction could not be created")
    return config_insertion
