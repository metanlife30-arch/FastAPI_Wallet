from sqlalchemy import Column, Integer
from database import Base

# Модель кошелька
class Wallet(Base):
    __tablename__ = 'Wallet'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    amount = Column(Integer)



