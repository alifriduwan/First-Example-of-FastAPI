from typing import Union

from fastapi import FastAPI, Request
from pydantic import BaseModel

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session



app = FastAPI()

# ตั้งค่าและเชื่อมต่อกับฐานข้อมูล SQLite
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# สร้างโมเดลสำหรับฐานข้อมูล
class StudentDB(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String, index=True)
    lastName = Column(String, index=True)
    age = Column(Integer, nullable=False)

# สร้างฐานข้อมูล
Base.metadata.create_all(bind=engine)

# Pydantic Model
class Student(BaseModel):
    firstName : str
    lastName: str
    age : int

class StudentCreated(Student):
    pass

class StudentResponse(Student):
    id: int
    class Config:
        from_attributes = True


@app.get("/")
def hello_world():
    return { "message" : "Hello World" }

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/items")
async def create_item(request: Request):
    body = await request.json()
    return { "request body" : body }

@app.post("/students")
def create_student(student: Student):
    return { "request body" : student }

@app.put("/students/{student_id}")
def edit_student(student_id: int, student: Student):
    return { "id" : student_id, "request body" : student}

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    return { "message" : f"Student {student_id} deleted"}
