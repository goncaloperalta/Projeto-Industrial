import logging
import shared_memory as sh
from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)

class Profile(BaseModel):
    pressTime: str | None = '0'

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.post("/start")
async def root(profile: Profile):
    logger.info(f"Got request with parameter {profile.pressTime}")
    print("\033[92m[API] Got request\033[00m")
    sh.pressTime = int(profile.pressTime)
    sh.sem_api.release()            # Signal to start the SSH server

    sh.sem_readings_ready.acquire() # Wait until readings are ready...
    sh.sem_feedback_ready.acquire() # Wait until feedback is ready...

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    sh.pressTime = 0
    # Send values back to the interface
    print("\033[92m[API] Sending data back\033[00m")
    logger.info("Sending data back")
    return {
        "feedback": sh.feedback,
        "force_val": sh.readings['val'],
        "time_val": sh.readings['time'],
        "date": date,
        "time": time
    }
