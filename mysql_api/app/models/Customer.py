from sqlalchemy import Boolean, Column, Integer, String
from app.config.database import Base

class Customers(Base):
    __tablename__ = "Customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    is_verified = Column(Boolean, default=False)
    phone = Column(String(20))
    address = Column(String(255))