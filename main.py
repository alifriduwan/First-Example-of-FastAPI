from typing import Union

from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
    firstName : str
    lastName: str
    age : int

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
