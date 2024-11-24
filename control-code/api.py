import shared_memory as sh
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
    print("\033[92m[API] Got request\033[00m")
    sh.sem_api.release()            # Signal to start the SSH server

    sh.sem_readings_ready.acquire() # Wait until readings are ready...
    sh.sem_feedback_ready.acquire() # Wait until feedback is ready...

    # Send values to the interface
    print("\033[92m[API] Sending data back\033[00m")
    return {"sensor": sh.readings,
            "but_feedback": sh.feedback}
