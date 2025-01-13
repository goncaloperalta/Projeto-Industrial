import logging
import sqlite3 as sql
from os import system
import shared_memory as sh
from fastapi import FastAPI, Response
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

logger = logging.getLogger("API")

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

############################################################ START/ABORT TEST #########################
class Params(BaseModel):        # Parameters of the test
    pName: str | None = 'None'  # Profile to use
    pressTime: int | None = 0   # Button press time in seconds
    nTimes: int | None = 1      # Number of times to press the button
    interval: int | None = 0    # Interval in seconds between presses
@app.post("/start")
async def start(params: Params, response: Response):
    with sh.access:
        if sh.STATE != sh.state.READY:
            response.status_code = 400
            return {"message": "A test is already running"}

    with open('app.log', 'w'):
        pass

    if params.pName != 'None':
        db = sql.connect("app.db")
        cur = db.cursor()
        profile = cur.execute(f"SELECT * FROM profiles WHERE pName = \"{params.pName}\"").fetchone()
        cur.close()
        db.close()
        if profile == None:
            response.status_code = 404
            return {"message": "Profile not found"}
        params.pressTime = profile[2]
        params.nTimes = profile[3]
        params.interval = profile[4]

    with sh.access:
        sh.parameters.pressTime = params.pressTime
        sh.parameters.nTimes = params.nTimes
        sh.parameters.interval = params.interval

    logger.info(f"Got request with: PressTime: {sh.parameters.pressTime}s, nTimes: {sh.parameters.nTimes}, Interval: {sh.parameters.interval}s")
    sh.startTest.release()

    return {"message": "Test started"}

@app.get("/abort-test")
async def abortTest():
    with sh.access:
        if sh.STATE == sh.state.READY:
            return {"message": "No test to abort"}
        
        sh.STATE = sh.state.ABORT

    return {"message": "Test Aborted"}

@app.get("/get-status")
async def getStatus():
    with sh.access:
        if sh.STATE == sh.state.READY:
            return {"message": "Ready"}
        elif sh.STATE == sh.state.ABORT:
            return {"message": "Aborting the test"}
        else:
            return {"message": "Running a test"}

@app.get("/get-current-parameters")
async def getCurrentParameters():
    with sh.access:
        if sh.STATE != sh.state.READY:
            return {
                "pressTime": sh.parameters.pressTime, 
                "nTimes": sh.parameters.nTimes,
                "interval": sh.parameters.interval
            }
        else:
            return {"message": "Not running a test"}

@app.get("/get-test-data")
async def getTestData():
    system("sqlite3 app.db -cmd \".mode json\" \".output static/data.json\" \"SELECT * FROM tests\" \".output stdout\"")
    return FileResponse("static/data.json", media_type='application/octet-stream',filename="data.json")

############################################################ TEST DATA #########################
@app.get("/get-tests")
async def getTest():
    db = sql.connect("app.db")
    cur = db.cursor()
    res = cur.execute("SELECT * FROM tests ORDER BY date DESC, time DESC")

    tests = {
        "tests": {
            "test": []
        }
    }

    while True:
        row = res.fetchone()
        if row is None: break
        test = {
            "id": row[0],
            "button": row[1],
            "success": row[2],
            "force_val": row[3],
            "time_val": row[4],
            "date": row[5],
            "time": row[6]
        }
        tests["tests"]["test"].append(test)

    cur.close()
    db.close()

    return tests

class Test(BaseModel):
    button: str
    success: int
    force_val: list
    time_val: list
    date: str
    time: str
@app.post("/add-test")
async def addTest(test: Test):
    db = sql.connect("app.db")
    cur = db.cursor()
    cur.execute(f"INSERT INTO tests (button, success, force_val, time_val, date, time) VALUES (\"{test.button}\", {test.success}, \"{test.force_val}\", \"{test.time_val}\", \"{test.date}\", \"{test.time}\")")
    db.commit()
    cur.close()
    db.close()

    return {"message": "Test added to database"}

@app.get("/get-last-test")
async def getLastTest():
    db = sql.connect("app.db")
    cur = db.cursor()
    row = cur.execute("SELECT * FROM tests ORDER BY id DESC LIMIT 1").fetchone()
    cur.close()
    db.close()

    return {
        "id": row[0],
        "button": row[1],
        "success": row[2],
        "force_val": row[3],
        "time_val": row[4],
        "date": row[5],
        "time": row[6]
    }

@app.get("/get-success")
async def getSuccess():
    db = sql.connect("app.db")
    cur = db.cursor()
    res = cur.execute("SELECT success FROM tests")
    val = []
    while True:
        row = res.fetchone()
        if row is None: break
        val.append(row[0])
    db.commit()
    cur.close()
    db.close()

    return val

############################################################ PROFILES #########################
class Profile(BaseModel):
    pName: str
    pressTime: int
    nTimes: int
    interval: int
@app.post("/add-profile")
async def addProfile(profile: Profile, response: Response):
    db = sql.connect("app.db")
    cur = db.cursor()
    try:
        cur.execute(f"INSERT INTO profiles (pName, pressTime, nTimes, interval) VALUES (\"{profile.pName}\", {profile.pressTime}, {profile.nTimes}, {profile.interval})")
    except sql.OperationalError:
        response.status_code = 400
        return {"message": "A profile with that name already exists"}
    db.commit()
    cur.close()
    db.close()

    response.status_code = 201
    return {"message": "Profile added to database"}

class ProfileName(BaseModel):
    pName: str
@app.delete("/delete-profile")
async def deleteProfile(profileName: ProfileName):
    db = sql.connect("app.db")
    cur = db.cursor()
    cur.execute(f"DELETE FROM profiles WHERE pName = \"{profileName.pName}\"")
    db.commit()
    cur.close()
    db.close()

    return {"message": "Profile deleted from database"}

@app.get("/get-profiles")
async def getProfiles():
    db = sql.connect("app.db")
    cur = db.cursor()
    res = cur.execute("SELECT * FROM profiles")
    
    profiles = {
        "profiles": {
            "profile": []
        }
    }

    while True:
        row = res.fetchone()
        if row is None: break
        profile = {
            "id": row[0],
            "pName": row[1],
            "pressTime": row[2],
            "nTimes": row[3],
            "interval": row[4]
        }
        profiles["profiles"]["profile"].append(profile)

    cur.close()
    db.close()

    return profiles