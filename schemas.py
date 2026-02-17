from pydantic import BaseModel
from typing import  Annotated, Optional
from pydantic import BaseModel, Field

# Модель данных для изменения баланса кошелька
class Wallet_Сhange(BaseModel):
    id: Optional[int]    # id пользователя 
    operation_type : str = Field(default="DEPOSIT or WITHDRAW") 
    amount:  int


