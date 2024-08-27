from fastapi import APIRouter, Depends
from app.api.crud.hub_configs.config import *
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.api.schemas import schemas

router = APIRouter(
    prefix="/config",
    tags=["Capital Hub Configs"])

@router.get("/table_names/")
def read_table_names():
    """
    Retrieve a list of all table names available in the database.

    This endpoint provides the names of tables that can be queried or updated 
    within the MoneyBoard system. These table names are essential for querying 
    or posting data to the correct tables.

    Returns:
    - List[str]: A list of table names as strings.
    """
    return get_table_names()

@router.get("/table_configs/")
def read_table_configs(table_name: str, db: Session = Depends(get_db)):
    """
    Retrieve all configuration records from a specified table.

    This endpoint allows you to fetch all records from a given table 
    within the MoneyBoard system. The table name must be one of the following: 
    ['currency', 'account', 'category', 'transaction_type'].

    Parameters:
    - table_name (str): The name of the table to retrieve records from.
    - db (Session): The database session dependency.

    Returns:
    - List[Dict]: A list of dictionaries representing each record in the table.

    Raises:
    - HTTPException: If the specified table name is invalid.
    """
    return get_table_configs(table_name, db)

@router.post("/post_new_config_account/", 
             response_model=schemas.AccountBase)
def create_account_config(config_name: str,
                          config_descr: str,
                          db: Session = Depends(get_db)):
    """
    Add a new account configuration to the database.

    This endpoint allows the creation of a new account configuration, 
    which includes an account name and description. The account ID is 
    automatically generated.

    Parameters:
    - config_name (str): The name of the new account.
    - config_descr (str): A description of the new account.
    - db (Session): The database session dependency.

    Returns:
    - AccountBase: The newly created account configuration.

    Raises:
    - HTTPException: If the account configuration could not be created.
    """
    return post_new_account_config(config_name,config_descr,db)

@router.post("/post_new_config_category/", 
             response_model=schemas.CategoryBase)
def create_category_config(config_name: str,
                           config_descr: str,
                           db: Session = Depends(get_db)):
    """
    Add a new category configuration to the database.

    This endpoint allows the creation of a new category configuration, 
    which includes a category name and description. The category ID is 
    automatically generated.

    Parameters:
    - config_name (str): The name of the new category.
    - config_descr (str): A description of the new category.
    - db (Session): The database session dependency.

    Returns:
    - CategoryBase: The newly created category configuration.

    Raises:
    - HTTPException: If the category configuration could not be created.
    """
    return commit_new_category(config_name,config_descr,db)

@router.post("/post_new_config_currency/", 
             response_model=schemas.CurrencyBase,
             tags=["Capital Hub Configs"])
def create_currency_config(config_name: str,
                           config_descr: str,
                           db: Session = Depends(get_db)):
    """
    Add a new currency configuration to the database.

    This endpoint allows the creation of a new currency configuration, 
    which includes a currency name and description. The currency ID is 
    automatically generated.

    Parameters:
    - config_name (str): The name of the new currency.
    - config_descr (str): A description of the new currency.
    - db (Session): The database session dependency.

    Returns:
    - CurrencyBase: The newly created currency configuration.

    Raises:
    - HTTPException: If the currency configuration could not be created.
    """
    return commit_new_currency(config_name,config_descr,db)

@router.post("/post_new_transaction_type/",
             response_model=schemas.TransactionTypeBase)
def create_transaction_type_config(config_name: str,
                                   config_descr: str,
                                   db : Session = Depends(get_db)):
    """
    Add a new transaction type configuration to the database.

    This endpoint allows the creation of a new transaction type configuration, 
    which includes a transaction type name and description. The transaction 
    type ID is automatically generated.

    Parameters:
    - config_name (str): The name of the new transaction type.
    - config_descr (str): A description of the new transaction type.
    - db (Session): The database session dependency.

    Returns:
    - TransactionTypeBase: The newly created transaction type configuration.

    Raises:
    - HTTPException: If the transaction type configuration could not be created.
    """
    return commit_new_transaction_type(config_name,config_descr,db)




