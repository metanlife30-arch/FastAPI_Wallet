from fastapi import Depends, HTTPException, status,  APIRouter
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy import select
from config import settings
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import User
from typing import  Optional
from database import  session_local

ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

router = APIRouter(prefix="/api/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user( username: str = None):
        async with session_local() as session:
            result= await  session.execute(select(User).where(User.login == username))
            user = result.scalars().first()
            return user
        
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)



def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# create token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# create token
@router.post('/token')
async def get_token(request: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(username=request.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    if not verify_password( request.password,user.password,):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Wrong password')
    access_token = create_access_token(data={'username': user.login})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.login
    }

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authneticate': 'Bearer'}
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        decode_username: str = payload.get('username')

        if decode_username is None:
            raise credentials_exeption
    except JWTError:
        raise credentials_exeption

    # TODO: check if token expires

    user = await get_user( username=decode_username)

    if user is None:
        raise credentials_exeption

    return user

