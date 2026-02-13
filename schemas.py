from pydantic import BaseModel
from typing import  Annotated, Optional
from pydantic import BaseModel, Field

# Модель данных для изменения баланса кошелька
class Wallet_Сhange(BaseModel):
    id: Optional[int]    # id пользователя 
    operation_type : str
    amount:  int

# Модель данных для создания нового поста
#class Wallet_Get(BaseModel):
#    title: str  # Заголовок поста
#    body: str  # Текст поста
#    author_id: int  # ID автора поста

class UserCreate(BaseModel):
    # Используем Annotated для добавления метаданных и валидации
    # Имя пользователя (от 2 до 20 символов), Имя пользователя (от 2 до 20 символов)
    login: Annotated[str, Field(..., title="login", min_length=2, max_length=20)]
    # пароль пользователя (от 5 символов )
    password: Annotated[str, Field(..., title="password", min_length=5)]

