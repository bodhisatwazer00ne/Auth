import os
import jwt

from fastapi.security import OAuth2PasswordBearer

from datetime import datetime,timedelta,timezone
from dotenv import load_dotenv
from pwdlib import PasswordHash

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

password_hash=PasswordHash.recommended()

def hash_password(password:str):
    return password_hash.hash(password)

def verify_password(plain_password:str,hashed_password:str):
    return password_hash.verify(plain_password,hashed_password)

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM="HS256"

def create_access_token(username:str):
    expire=datetime.now(timezone.utc)+timedelta(minutes=30)
    
    payload={
        "sub":username,
        "exp":expire
    }

    token=jwt.encode(
        payload,
        SECRET_KEY,
        ALGORITHM)
    
    return token


#token verifivation function 
def decode_access_token(token: str):

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    return payload 

