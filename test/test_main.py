import pytest
from main import app
from httpx import AsyncClient, ASGITransport

client = ASGITransport(app=app)

# Проверяет Эндпоинт для создание кошешька
@pytest.mark.asyncio(loop_scope="module")
async def test_wallet_add():
    async with AsyncClient(transport=client,base_url="http://test") as ac:
        response = await ac.post("/api/v1/wallets/create")
        data = response.json()
        data = data[0]
        data= data.split()[-1]
        assert response.status_code == 200
        assert response.json() == [
            f"The wallet was created with an id = {data}"]

# Проверяет Эндпоинт для получение суммы кошелька
@pytest.mark.asyncio(loop_scope="module")
async def test_wallet_get():
    async with AsyncClient(transport=client,base_url="http://test") as ac:
        response = await ac.get("/api/v1/wallets/get/1")
        data = response.json()
        data = data[0]
        data= data.split()[-1]
        assert response.status_code == 200
        assert response.json() == [
            f"Ваш баланс: {data}"]

# Проверяет Эндпоинт для изменение баланса
@pytest.mark.asyncio(loop_scope="module")
async def test_wallet_change():
    async with AsyncClient(transport=client,base_url="http://test") as ac:
        response = await  ac.put("/api/v1/wallets/operation", json={"id": 1, "operation_type": "DEPOSIT", "amount": 10})
        assert response.status_code == 200
        assert response.json() == ["message: Wallet updated"]