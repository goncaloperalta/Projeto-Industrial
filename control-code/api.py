import shared_memory as sh
from requests import post
from threading import Semaphore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:5173"] # Allow to receive from the Interface

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/start")
async def root():
    sh.sem_api.release()            # Signal to start reading the sensor

    sh.sem_readings_ready.acquire() # Wait until readings are ready...

    # Send values to the interface
    return {"data": sh.readings}
