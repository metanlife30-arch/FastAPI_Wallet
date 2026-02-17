from fastapi import FastAPI, HTTPException, status
from sqlalchemy import select
from models import Wallet 
from database import  session_local
from schemas import Wallet_Сhange

# Создание экземпляра FastAPI
app = FastAPI()

# Эндпоинт для создание кошешька
@app.post("/api/v1/wallets/create",summary="Create a wallet",tags=["Wallets"])
async def wallet_add():
    # Поиск автора поста по ID
    async with session_local() as session:
        post = Wallet(amount=0)
        session.add(post)
        await session.commit()
        return {f"The wallet was created with an id = {post.id}"}
    
# Эндпоинт для изменение баланса
@app.put("/api/v1/wallets/operation",summary="Changing the balance",tags=["Wallets"])
async def wallet_change(wallet:Wallet_Сhange):
    async with session_local() as session:
        # Условие если пользователь ввёл "DEPOSIT" or "WITHDRAW" идём дальше
        if wallet.operation_type=="DEPOSIT" or "WITHDRAW":  
            # Условие если не был ввёд id кошелька
            if not wallet.id  : 
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The wallet ID was not entered') 
            
            elif wallet.operation_type=="DEPOSIT":
                result = await session.get(Wallet, wallet.id)
                # Условие если не бьл найден кошелёк
                if not result:
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
                # Условие сумма кошелька равна 0    
                elif result.amount==0 :
                    result.amount =  wallet.amount 
                    await session.commit()
                    return {"message: Wallet updated"}
                
                result.amount =  result.amount + wallet.amount  
                await session.commit()
                return {"message: Wallet updated"}
            
            else:
                # Условие если было введенно WITHDRAW
                result = await session.get(Wallet, wallet.id)
                # Условие если не бьл найден кошелёк 
                if not result:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')    

                elif wallet.amount <= result.amount: 
                    result.amount =  result.amount - wallet.amount  
                    await session.commit()
                    return {"message": "Wallet updated"}
                
                # Сумма снятия больше сумме на балансе
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The withdrawal amount is more than what is on the balance')
        # Ошибка на введённый не правильный тип операции                            
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid operation type')

#Эндпоинт для получение суммы кошелька
@app.get("/api/v1/wallets/get/{id}",summary="Getting a balance",tags=["Wallets"])
async def wallet_get(id: int):
    # Поиск кошелька поста по ID
    async with session_local() as session:
        wallet = await session.get(Wallet, id)
        if not wallet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
        return {f"Ваш баланс: {wallet.amount}"}
    


