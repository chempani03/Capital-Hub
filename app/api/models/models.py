from sqlalchemy import Column,String, Float, DateTime, Integer, NVARCHAR, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class TransOverView(Base):
    __tablename__ = 'transaction_overview'

    transaction_id = Column(NVARCHAR(50), primary_key=True)
    booking_date = Column(DateTime(False))
    value_date = Column(DateTime(False))
    amount = Column(Float)
    currency = Column(NVARCHAR(50), ForeignKey('currency.currency'))
    transaction_type = Column(NVARCHAR(50), ForeignKey('transaction_type.transaction_type'))
    account = Column(NVARCHAR(50), ForeignKey('account.account'))
    category = Column(NVARCHAR(50), ForeignKey('category.category'))
    booking_text = Column(NVARCHAR(100))

    # Relationships
    currency_rel = relationship("Currency", back_populates="transactions")
    transaction_type_rel = relationship("TransactionType", back_populates="transactions")
    account_rel = relationship("Account", back_populates="transactions")
    category_rel = relationship("Category", back_populates="transactions")


class Currency(Base):
    __tablename__ = 'currency'

    currency = Column(NVARCHAR(50), primary_key=True)
    currency_id = Column(Integer)
    currency_description = Column(Text)

    # Relationships
    transactions = relationship("TransOverView", back_populates="currency_rel")


class Account(Base):
    __tablename__ = 'account'

    account = Column(NVARCHAR(50), primary_key=True)
    account_id = Column(Integer)
    account_description = Column(Text)

    # Relationships
    transactions = relationship("TransOverView", back_populates="account_rel")


class Category(Base):
    __tablename__ = 'category'

    category = Column(String(50), primary_key=True)
    category_id = Column(Integer)
    category_description = Column(Text)

    # Relationships
    transactions = relationship("TransOverView", back_populates="category_rel")


class TransactionType(Base):
    __tablename__ = 'transaction_type'

    transaction_type = Column(NVARCHAR(50), primary_key=True)
    transaction_type_id = Column(Integer)
    transaction_type_description = Column(Text)

    # Relationships
    transactions = relationship("TransOverView", back_populates="transaction_type_rel")