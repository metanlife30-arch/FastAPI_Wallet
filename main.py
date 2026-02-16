from fastapi import FastAPI, HTTPException, status, Query,Depends
from typing import  Annotated
from sqlalchemy import select
from models import User,Wallet 
from database import  session_local
from schemas import Wallet_Сhange,UserCreate
from auth import get_current_user, router,get_password_hash
import uvicorn

# Создание экземпляра FastAPI
app = FastAPI()


# Эндпоинт для добавление кошешька
@app.post("/api/v1/wallets/create",summary="Create a wallet",tags=["Wallets"])
async def add_item(token: str = Depends(get_current_user)):
    # Поиск автора поста по ID
    async with session_local() as session:
        post = Wallet(amount=0)
        session.add(post)
        await session.commit()
        return (f"The wallet was created with an id {post.id}")
    
# Эндпоинт для получения изменение баланса
@app.put("/api/v1/wallets/operation",summary="Changing the balance",tags=["Wallets"])
async def items(wallet:Wallet_Сhange,token: str = Depends(get_current_user)):
    async with session_local() as session:
        if wallet.operation_type=="DEPOSIT" or "WITHDRAW": # Условие если пользователь ввёл "DEPOSIT" or "WITHDRAW" идём дальше 

            if not wallet.id  : # Условие если не был ввёд id кошелька
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The wallet ID was not entered') 
            
            elif wallet.operation_type=="DEPOSIT":
                result = await session.get(Wallet, wallet.id)
                print("Здесь",result.amount)
                if not result:
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')    
                elif result.amount==0 :
                    result.amount =  wallet.amount 
                    await session.commit()
                    return {"message": "Wallet updated"}
                
                result.amount =  result.amount + wallet.amount  
                await session.commit()
                return {"message": "Wallet updated"}
            
            else:
                result = await session.get(Wallet, wallet.id) # Условие если было введенно WITHDRAW
                if not result:
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')    

                elif wallet.amount <= result.amount: 
                    result.amount =  result.amount - wallet.amount  
                    await session.commit()

                    return {"message": "Wallet updated"}
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The withdrawal amount is more than what is on the balance')
                                    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid operation type')# Ошибка на введённый не правильный тип операции

#Эндпоинт для получение суммы кошелька
@app.get("/api/v1/wallets/get",summary="Getting a balance",tags=["Wallets"])
async def add_item(id: int,token: str = Depends(get_current_user)):
    # Поиск автора поста по ID
    async with session_local() as session:
        wallet = await session.get(Wallet, id)
        return (f"Ваш баланс: {wallet.amount}")
    

# Эндпоинт для добавления нового пользователя для доступа к Api
@app.post("/user/add",tags=["User"])
async def user_add(user: Annotated[UserCreate, Query(...)]):
    # Генерация нового ID для пользователя
    user.password= get_password_hash(user.password)
    async with session_local() as session:
        user = User(login=user.login, password=user.password)
        session.add(user)
        await session.commit()
        return ("Вы зарегистрировались в системе")  
app.include_router(router)


