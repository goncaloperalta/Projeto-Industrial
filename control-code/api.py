import logging
from datetime import datetime
import shared_memory as sh
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)

app = FastAPI()

origins = ["*"] # Allow to receive from the Interface

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/start")
async def root():
    logger.info("Got request")
    print("\033[92m[API] Got request\033[00m")
    sh.sem_api.release()            # Signal to start the SSH server

    sh.sem_readings_ready.acquire() # Wait until readings are ready...
    sh.sem_feedback_ready.acquire() # Wait until feedback is ready...

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    # Send values to the interface
    print("\033[92m[API] Sending data back\033[00m")
    logger.info("Sending data back")
    return {
        "feedback": sh.feedback,
        "force_val": sh.readings['val'],
        "time_val": sh.readings['time'],
        "date": date,
        "time": time
    }
