from requests import post
from threading import Semaphore
from fastapi import FastAPI
from semaphores import sem_api
from pydantic import BaseModel
from typing import List

class DataModel(BaseModel):
    val: List[int]
    time: List[float]

app = FastAPI()

@app.get("/start")
async def root():
    sem_api.release()

    return {"message": "Starting control code"}

@app.post("/sensor_readings")
async def sensor_readings(data: DataModel):
    print(data.val)

    return {"message": "Values obtained"}