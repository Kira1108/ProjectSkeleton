from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

class DbUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(256))
    email = Column(String(50))


