from fastapi import APIRouter,status,Depends,Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.config.security import oauth2_scheme
from app.services.auth_services import login,get_refresh_token,register,verified_user,verified_email,reset_password_user,forgot_password_user,login_google,google_callback
from app.schemas.user_schemas import CreateUserRequest

router=APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404:{"description":"Not found"}}
)

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)

@router.post("/register",status_code=status.HTTP_201_CREATED)
async def register_user(data:CreateUserRequest,db:Session = Depends(get_db)):
    return await register(data=data,db=db)
    
@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await login(data=data, db=db)

@auth_router.post("/refresh-token",status_code=status.HTTP_200_OK)
async def refresh_token(refresh_token:str=Header(),db:Session=Depends(get_db)):
    return await get_refresh_token(refresh_token=refresh_token, db=db)

@auth_router.post("/verified",status_code=status.HTTP_200_OK)
async def verified(email):
    return await verified_user(email)
@auth_router.get("/verification",status_code=status.HTTP_200_OK)
async def verification(token:str,db:Session=Depends(get_db)):
    return await verified_email(token,db)

@router.post("/forgot-password",status_code=status.HTTP_200_OK)
async def forgot_password(email,db: Session = Depends(get_db)):
    return await forgot_password_user(email,db)

@router.patch("/reset-password",status_code=status.HTTP_200_OK)
async def reset_password(token:str,new_password:str,db:Session=Depends(get_db)):
    return await reset_password_user(token,new_password,db)

@router.get("/login/google",status_code=status.HTTP_200_OK)
async def login_google_user():
    return await login_google()

@router.get("/google/callback")
async def login_google_callback(code: str, db: Session = Depends(get_db)):
    return await google_callback(code,db)
