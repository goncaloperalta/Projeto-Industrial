from fastapi import FastAPI

app = FastAPI()

@app.get("/start")
async def root():
    return {"message": "Starting control code"}