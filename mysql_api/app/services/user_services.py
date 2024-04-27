from app.models.Customer import Customers
from fastapi.exceptions import HTTPException
from datetime import datetime
from app.schemas.user_schemas import UserResponse,UserUpdate
from fastapi.encoders import jsonable_encoder
import json
from fastapi import HTTPException
from app.config.security import hash_password
from datetime import datetime
async def create(data,db):
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
        user_response = UserResponse.from_orm(new_user)  # Convert to UserResponse
        payload = {
        "status":200,
        "data":{
            "message":"Customers created successfully",
            "user":user_response.dict()
        }
        }
        return payload

async def get_all(db):
    users = db.query(Customers).all()
    user_models = [UserResponse.from_orm(user) for user in users]
    payload = {
        "status":200,
        "data":{
            "message":"Get all users successfully",
            "users":jsonable_encoder(user_models),
        }
    }
    return payload

async def get_list_users(db,skip, limit):
    # Ví dụ, nếu bạn muốn lấy trang thứ 2 của danh sách người dùng,
    # với mỗi trang có 20 bản ghi, bạn có thể gọi hàm get_list_users(db, skip=20, limit=20).
    # Điều này sẽ bỏ qua 20 bản ghi đầu tiên (trang 1) và trả về 20 bản ghi tiếp theo (trang 2).
    users = db.query(Customers).offset(skip).limit(limit).all()
    user_models = [UserResponse.from_orm(user) for user in users]
    payload = {
        "status":200,
        "data":{
            "message":"Get list users successfully",
            "users":jsonable_encoder(user_models),
        }
    }
    return payload

async def get_user_by_id(id: int,db):
    user = db.query(Customers).filter(Customers.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Customers not found")
    user_response=UserResponse.from_orm(user)
    payload = {
        "status":200,
        "data":{
            "message":"Get all users successfully",
            "users":jsonable_encoder(user_response),
        }
    }
    return payload

async def update(db, id: int, data:UserUpdate):
    db_user = db.query(Customers).filter(Customers.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Customers not found")
    
    user_data = data.dict(exclude_unset=True)  # Tạo dict từ đối tượng data
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    user_response=UserResponse.from_orm(db_user)
    payload = {
        "status":200,
        "data":{
            "message":"Update user successfully",
            "users":jsonable_encoder(user_response),
        }
    }
    return payload

async def delete(db, id: int):
    user = db.query(Customers).filter(Customers.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Customers not found")
    db.delete(user)
    db.commit()
    payload = {
        "status":200,
        "data":{
            "message":"Delete user successfully",
        }
    }
    return payload