import logging
import sqlite3 as sql
from time import sleep
import shared_memory as sh
from datetime import datetime

logger = logging.getLogger("STATE")

def State():
    while True:
        sh.startTest.acquire()

        with sh.access:
            sh.STATE = sh.state.RUNNING

        for i in range(sh.parameters.nTimes):
            # Start SSH Module
            sh.startSSH.release()               # Signal to start the SSH client

            # Wait
            sh.sensorReadingsReady.acquire()    # Wait until readings are ready...
            sh.feedbackReady.acquire()          # Wait until feedback is ready...

            # Store data on variable
            

            # Wait interval
            sleep(sh.parameters.interval)

            with sh.access:
                if sh.STATE == sh.state.ABORT:
                    sh.STATE = sh.state.READY
                    break;

        # Store data on the database
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        db = sql.connect("app.db")
        cur = db.cursor()
        cur.execute(f"INSERT INTO tests (button, success, force_val, time_val, date, time) VALUES (\"{sh.feedback['button']}\", {sh.feedback['success']}, \"{sh.readings['val']}\", \"{sh.readings['time']}\", \"{date}\", \"{time}\")")
        db.commit()
        cur.close()
        db.close()

        with sh.access:
            sh.STATE = sh.state.READY