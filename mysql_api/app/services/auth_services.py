from app.models.Customer import Customers
from fastapi import status
from fastapi.exceptions import HTTPException
from app.config.security import verify_password,create_access_token,create_refresh_token,get_token_payload,hash_password
from app.config.settings import get_settings
from datetime import timedelta
from app.schemas.auth_schemas import TokenResponse,EmailSchema
from app.schemas.user_schemas import UserResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime 
from fastapi_mail import FastMail,MessageSchema,ConnectionConfig
from app.config.security import get_google_auth_credentials
import google.auth.transport.requests
import google.oauth2.id_token
import google.oauth2.credentials
import google_auth_oauthlib.flow
import google.auth
import webbrowser


settings=get_settings()

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS
    
)
async def register(data,db):
    user = db.query(Customers).filter(Customers.email == data.email).first()
    if user:
            raise HTTPException(status_code=400, detail={
                "status": 400,
                "message": "Email already exists"
            })
            
    new_user = Customers(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        is_verified=False,
        phone=data.phone,
        address=data.address
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    payload = {
        "id":new_user.id,
        "email":new_user.email,
        "name":new_user.name,
        "phone":new_user.phone,
        "address":new_user.address
    }
    access_token_expires = timedelta(days=settings.JWT_TOKEN_EXPIRE)
    token=await create_access_token(payload,expires_delta=access_token_expires)
    refresh_token_expires = timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE)
    refresh_token= await create_refresh_token(payload,expires_delta=refresh_token_expires)
    user_response = UserResponse.from_orm(new_user)
    return TokenResponse(token=token,refresh_token=refresh_token,token_type="bearer",data={
        "message":"Register successfully",
        "user":user_response.dict()
    })

async def login(data,db):
    user = db.query(Customers).filter(Customers.email == data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Email is not registered with us.",headers={"WWW-Authenticate":"Bearer"})
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password.",headers={"WWW-Authenticate":"Bearer"}) 
    payload = {
        "id":user.id,
        "email":user.email,
        "name":user.name,
        "phone":user.phone,
        "address":user.address
    }
    # _verify_user_access(user=user)
    access_token_expires = timedelta(days=settings.JWT_TOKEN_EXPIRE)
    token=await create_access_token(payload,expires_delta=access_token_expires)
    refresh_token_expires = timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE)
    refresh_token= await create_refresh_token(payload,expires_delta=refresh_token_expires)
    
    user_response = UserResponse.from_orm(user)
    return TokenResponse(token=token,refresh_token=refresh_token,token_type="bearer",data={
        "message":"Login successfully",
        "user":user_response.dict()
    })

async def get_refresh_token(refresh_token,db):
    payload = get_token_payload(refresh_token)
    user_id = payload.get("id",None)
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid refresh token",headers={"WWW-Authenticate":"Bearer"})
    user = db.query(Customers).filter(Customers.id == user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid refresh token",headers={"WWW-Authenticate":"Bearer"})
    return await _get_user_token(user, refresh_token=refresh_token)
   
async def _get_user_token(user:Customers,refresh_token=None):
    payload = {
        "id":user.id,
        "email":user.email,
        "name":user.name,
        "phone":user.phone,
        "address":user.address
    }
    access_token_expires = timedelta(days=settings.JWT_TOKEN_EXPIRE)
    token=await create_access_token(payload,expires_delta=access_token_expires)
    if not refresh_token:
        refresh_token_expires = timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE)
        refresh_token= await create_refresh_token(payload,expires_delta=refresh_token_expires)
    user_response = UserResponse.from_orm(user)
    return TokenResponse(token=token,refresh_token=refresh_token,token_type="bearer",data={
        "message":"Refresh token successfully",
        "user":user_response.dict()
    })

def _verify_user_access(user:Customers):
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Your account is not verified. Please check your email inbox to verify your account.")

async def verified_user(email:EmailSchema):
    try:
        token_data ={
            "email":email
        }
        
        access_token_expires = timedelta(days=settings.JWT_TOKEN_EXPIRE)
        token=await create_access_token(token_data,expires_delta=access_token_expires)
        template =f"""
           <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <title>Document</title>
            </head>
            <body>
                <div style="padding: 1rem; margin-top: 5vh; margin-bottom: 5vh">
                <h3>Xác thực tài khoản</h3>

                <p>
                    Cảm ơn bạn đã đăng ký tài khoản của website chúng tôi! Hãy nhấn vào nút
                    phía dưới để xác thực tài khoản
                </p>
                <div style="margin-top: 2rem;">
                    <a
                    style="
                    margin-top: 1rem;
                    padding: 1rem;
                    border-radius: 0.5rem;
                    font-size: 1.2rem;
                    text-decoration: none;
                    background-color: #0275d8;
                    color: white;
                    "
                    href="http://localhost:8000/auth/verification/?token={token}"
                    >Xác thực Email</a
                </div>
                </div>
            </body>
            </html>
        """
        message =MessageSchema(
            subject="Xác thực tài khoản",
            recipients=[email],
            body=template,
            subtype="html"
        )
        fm=FastMail(conf)
        await fm.send_message(message=message)
        return {"status":200,"message": "Email sent successfully"}
    except Exception as e:
        return {"error":str(e)}
    
async def verified_email(token,db):
    user = get_token_payload(token)
    user_db=db.query(Customers).filter(Customers.email == user.get("email")).first()
    if not user_db:
        raise HTTPException(status_code=400, detail="Invalid token")
    if user_db and not user_db.is_verified:
        user_db.is_verified = True
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        return {"status":200,"message": "Email verified successfully"}
    raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired token",
            headers={"WWW-Authenticate":"Bearer"} 
        )
    

async def forgot_password_user(email:EmailSchema,db):
    try:
        token_data ={
            "email":email
        }
        
        user_db=db.query(Customers).filter(Customers.email == email).first()
        if not user_db:
            return {"status":404,"message": "Email not found"}
        token=await create_access_token(token_data)
        template =f"""
           <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <title>Document</title>
            </head>
            <body>
                <div style="padding: 1rem; margin-top: 5vh; margin-bottom: 5vh">
                <h3>Quên mật khẩu</h3>

                <p>
                    Bạn đã yêu cầu cấp lại mật khẩu mới với website chúng tôi! Hãy nhấn bạn trong nút phải dưới để cập nhập mật khẩu mới
                </p>
                <div style="margin-top: 2rem;">
                    <a
                    style="
                    margin-top: 1rem;
                    padding: 1rem;
                    border-radius: 0.5rem;
                    font-size: 1.2rem;
                    text-decoration: none;
                    background-color: #0275d8;
                    color: white;
                    "
                    href="http://localhost:8000/auth/reset-password/?token={token}"
                    >Đặt lại mật khẩu</a
                </div>
                </div>
            </body>
            </html>
        """
        message =MessageSchema(
            subject="Quên mật khẩu",
            recipients=[email],
            body=template,
            subtype="html"
        )
        fm=FastMail(conf)
        await fm.send_message(message=message)
        return {"status":200,"message": "Email sent successfully"}
    except Exception as e:
        return {"error":str(e)}
    
async def reset_password_user(token,new_password,db):
    user = get_token_payload(token)
    user_db=db.query(Customers).filter(Customers.email == user.get("email")).first()
    if not user_db:
        raise HTTPException(status_code=400, detail="Invalid token")
    if user_db:
        user_db.password = hash_password(new_password)
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        user_response=UserResponse.from_orm(user_db)
        payload = {
            "status":200,
            "data":{
                "message":"Reset password successfully",
                "user":jsonable_encoder(user_response),
            }
        }
        return payload
    raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired token",
            headers={"WWW-Authenticate":"Bearer"} 
        )

async def login_google():
    client_secrets = {
        "web": {
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.CLIENT_SECRET,
            "redirect_uris": ["http://localhost:8000/auth/google/callback"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }

    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        client_secrets,
        scopes=["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"],
        redirect_uri="http://localhost:8000/auth/google/callback"
    )

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    
    # return {"authorization_url": authorization_url}
    return webbrowser.open(authorization_url)

async def google_callback(code: str, db):
    credentials = get_google_auth_credentials(code)

    id_info = google.oauth2.id_token.verify_oauth2_token(
            credentials.id_token,
            google.auth.transport.requests.Request(),
            audience=settings.CLIENT_ID)
    # Lấy thông tin người dùng từ id_info
    email = id_info.get("email")
    # picture = id_info.get("picture")
    name = id_info.get("name")
    # last_name = id_info.get("family_name")
    

    user = db.query(Customers).filter(Customers.email == email).first()
    if not user:
        user = Customers(email=email,name=name,is_verified=True)
        db.add(user)
        db.commit()
        db.refresh(user)
    user_response = UserResponse.from_orm(user)  # Convert to UserResponse
    payload = {
        "status":200,
        "data":{
            "message":"Customers created successfully",
            "user":jsonable_encoder(user_response)
        }
        }
    return payload