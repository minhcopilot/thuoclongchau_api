from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.user_schemas import CreateUserRequest,UserUpdate
from app.services.user_services import get_list_users,create,get_all,get_user_by_id,update,delete
from app.config.security import oauth2_scheme
router = APIRouter(
    prefix="/customers",
    tags=["customers"],
    responses={404: {"description": "User not found"}},
)
user_router = APIRouter(
    prefix="/customers",
    tags=["customers"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)
@user_router.post("",status_code=status.HTTP_201_CREATED)
async def create_user(data:CreateUserRequest,db:Session=Depends(get_db)):
        return await create(data,db)

@router.get("",status_code=status.HTTP_200_OK)
async def get_all_users(db:Session=Depends(get_db)):
    return await get_all(db)

@router.get("/list",status_code=status.HTTP_200_OK)
async def get_list(db:Session=Depends(get_db),skip: int = 0, limit: int = 10):
    return await get_list_users(db,skip, limit)

@router.get("/{id}",status_code=status.HTTP_200_OK)
async def get_user(id: int, db: Session = Depends(get_db)):
    return await get_user_by_id(id, db)

@user_router.patch("/{id}",status_code=status.HTTP_200_OK)
async def update_user(id: int, data: UserUpdate, db: Session = Depends(get_db)):
    return await update(db, id, data)

@user_router.delete("/{id}",status_code=status.HTTP_200_OK)
async def delete_user(id:int, db:Session=Depends(get_db)):
    return await delete(db,id)