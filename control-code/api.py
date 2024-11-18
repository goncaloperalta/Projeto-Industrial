import semaphores
from requests import post
from threading import Semaphore
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

class DataModel(BaseModel):
    val: List[int]
    time: List[float]

app = FastAPI()

@app.get("/start")
async def root():
    semaphores.sem_api.release()
    
    
    return {"message": "Starting control code"}

@app.post("/sensor_readings")
async def sensor_readings(data: DataModel):
    print(data.dict())

    post('http://localhost:5173/api/add-readings/', json=data.dict())

    return {"message": "Values obtained"}