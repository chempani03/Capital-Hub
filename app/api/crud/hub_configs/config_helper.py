from sqlalchemy.orm import Session
from ...models.models import *
from ...schemas.schemas import CategoryBase, CurrencyBase, TransactionTypeBase, AccountBase

def map_table_param(table_name):
    model_map = {
        'currency' : [Currency, Currency.currency_id],
        'account' : [Account, Account.account_id],
        'category' : [Category, Category.category_id],
        'transaction_type' : [TransactionType, TransactionType.transaction_type_id]
    }
    try:
        model = model_map[table_name][0]
        id_col = model_map[table_name][1]
    except KeyError:
        raise ValueError("Table name not recognized")
    
    return model, id_col

def get_last_id(model, column, db):
    result = db.query(model).order_by(getattr(model, column).desc()).first()
    if result:
        return getattr(result, column)
    else:
        return None

def post_config_account(db: Session, overv: AccountBase):
    config_account = Account(
        account=overv.account,
        account_id=overv.account_id,
        account_description=overv.account_description
    )
    db.add(config_account)
    db.commit()
    db.refresh(config_account) 
    return config_account

def post_config_category(db: Session, overv: CategoryBase):
    config_account = Category(
        category=overv.category,
        category_id=overv.category_id,
        category_description=overv.category_description
    )
    db.add(config_account)
    db.commit()
    db.refresh(config_account) 
    return config_account

def post_config_currency(db: Session, overv: CurrencyBase):
    config_account = Currency(
        currency=overv.currency,
        currency_id=overv.currency_id,
        currency_description=overv.currency_description
    )
    db.add(config_account)
    db.commit()
    db.refresh(config_account)  
    return config_account

def post_config_transaction_type(db: Session, overv: TransactionTypeBase):
    config_trans_type = TransactionType(
        transaction_type = overv.transaction_type,
        transaction_type_id = overv.transaction_type_id,
        transaction_type_description = overv.transaction_type_description
    )
    db.add(config_trans_type)
    db.commit()
    db.refresh(config_trans_type)
    return config_trans_type