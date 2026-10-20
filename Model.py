from sqlalchemy import Column, Integer, String
from database import Base

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    roll_no = Column(String(30), unique=True, nullable=False, index=True)
    name = Column(String(120), nullable=False, index=True)
    department = Column(String(100), nullable=False)
    semester = Column(String(30), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    phone = Column(String(30), nullable=True)
    gender = Column(String(30), nullable=True)
    address = Column(String(300), nullable=True)
