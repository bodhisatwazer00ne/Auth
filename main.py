from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from database import engine, Base,get_db
from models import User
from schemas import UserRegister,UserLogin
from auth import hash_password,verify_password,create_access_token,decode_access_token,oauth2_scheme


Base.metadata.create_all(bind=engine)

app=FastAPI()

@app.post("/register")
def register(user:UserRegister,db:Session=Depends(get_db)):
    existing_user=db.query(User).filter(User.username==user.username).first()
    if existing_user:
        raise HTTPException(status_code=409,detail="Username already exists")
    
    new_user=User(username=user.username,password_hash=hash_password(user.password))
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "User created Successfully!"
    }
    
@app.post("/login")
def login(user:UserLogin,db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.username==user.username).first()  
    
    if not db_user:
        raise HTTPException(
            status_code=401
            ,detail="Invalid username or password"
        )  
    
    if not verify_password(user.password,db_user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
        
    access_token=create_access_token(db_user.username)        
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
@app.get("/me")
def get_me(token:str=Depends(oauth2_scheme)):
    try:
        payload=decode_access_token(token)    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
            )

    username=payload.get("sub")
    
    return{
        "username":username
    }