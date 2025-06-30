from typing import Union, List

from fastapi import FastAPI, Request, Depends,  HTTPException
from pydantic import BaseModel

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


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

app = FastAPI()
# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@app.post("/students", response_model=StudentResponse)
async def create_student(student: StudentCreated, db: Session = Depends(get_db)):
    db_student = StudentDB(firstName=student.firstName, lastName=student.lastName, age=student.age)
    # db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/{student_id}", response_model=StudentResponse)
async def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
    return db_student

@app.get("/students", response_model=List[StudentResponse])
async def read_students(db: Session = Depends(get_db)):
    db_student = db.query(StudentDB).all()
    return db_student

@app.put("/students/{student_id}", response_model=StudentResponse)
async def update_student(student_id: int, student: StudentCreated, db: Session = Depends(get_db)):
    db_student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in student.model_dump().items():
        setattr(db_student, key, value)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.delete("/students/{student_id}")
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return { "message" : f"Student {student_id} deleted"}
