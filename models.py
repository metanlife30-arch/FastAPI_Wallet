from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Wallet(Base):
    __tablename__ = 'Wallet'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    amount = Column(Integer)

class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    login = Column(String, index=True)
    password = Column(String,index=True)


