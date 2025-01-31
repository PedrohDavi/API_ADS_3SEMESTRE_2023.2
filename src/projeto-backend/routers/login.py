from fastapi import APIRouter, Depends, HTTPException, status
from database import schemas
from sqlalchemy.orm import Session
from models import user_crud, JWTtoken
from database.database import get_db
from typing import List
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta

ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(tags=["Login"])


@router.post("/login")
def login(login: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(email=login.username, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    if not user.password == login.password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = JWTtoken.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
