from sqlalchemy import Column, Date, Integer, String, Boolean

from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    date_of_birth = Column(Date)
    gender = Column(String)
    address = Column(String)