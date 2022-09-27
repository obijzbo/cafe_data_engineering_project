import uvicorn
from fastapi import FastAPI
from db_query import query

app = FastAPI()

@app.get('/')
async def home():
    return{"message" : "Working"}

@app.post('/query')
async def data_query(location : str, menu : str, price : int):
    results = query(location, menu, price)
    return results