from typing import Union

from fastapi import FastAPI, Request

app = FastAPI()


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