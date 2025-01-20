import logging
import sqlite3 as sql
from time import sleep
from smbus2 import SMBus # type: ignore
import shared_memory as sh
from datetime import datetime

logger = logging.getLogger("STATE")

def testI2C():
    with SMBus(1) as bus:
        try:
            bus.read_i2c_block_data(0x28, 0, 2)
        except OSError:
            with sh.access:
                sh.ERROR = "Couldn't connect to the force sensor"
                sh.feedback = {
                    'button': 'No feedback',
                    'success': 0
                }
                sh.readings['val'] = [0, 0, 0] 
                sh.readings['time'] = [0, 0, 0]
                sh.feedbackReady.release()
                sh.sensorReadingsReady.release()
    
def State():
    while True:
        # State Loop
        # 1 - Wait for start
        # 2 - Get parameters of the test
        # 3 - Start the SSH module
        # 4 - Wait until Sensor and SSH finish
        # 5 - Store the modules data
        # 6 - Wait the interval between actuations
        # 7 - Repeat for nTimes
        # 8 - Store data on the database
        # Repeat

        sh.startTest.acquire()
        logger.info("Starting a test")

        rowID = 0
        
        with sh.access:
            sh.resetModulesData()
            n = sh.parameters.nTimes
            wait = sh.parameters.interval
            sh.STATE = sh.state.RUNNING
            sh.CURRENT_RUN = 0
            sh.ERROR = 'No Error'

            db = sql.connect("app.db")
            cur = db.cursor()
            
            rowID = cur.execute(f"INSERT INTO tests (success, parameters, force_val, time_val) VALUES (\"[\", \"{[sh.parameters.pressTime, sh.parameters.nTimes, sh.parameters.interval]}\", \"[\", \"[\")").lastrowid
            
            db.commit()
            cur.close()
            db.close()
        

        testI2C()
        
        for i in range(n):
            with sh.access:
                if sh.ERROR != 'No Error':
                    break
            # Start SSH Module
            sh.startSSH.release()
            logger.info(f"Starting actuation: {i+1}/{n}")

            # Wait until the other modules finish...
            sh.sensorReadingsReady.acquire()
            sh.feedbackReady.acquire()
            logger.info("Storing test data on database")

            # Store data on variable
            with sh.access:
                db = sql.connect("app.db")
                cur = db.cursor()
        
                if i == 0:
                    cur.execute(f"UPDATE tests SET success = success || \"{sh.modulesData['success']}\", force_val = force_val || \"{sh.modulesData['force_val']}\", time_val = time_val || \"{sh.modulesData['time_val']}\" WHERE id = {rowID}")
                else:
                    cur.execute(f"UPDATE tests SET success = success || \", {sh.modulesData['success']}\", force_val = force_val || \", {sh.modulesData['force_val']}\", time_val = time_val || \", {sh.modulesData['time_val']}\" WHERE id = {rowID}")
                
                db.commit()
                cur.close()
                db.close()

            if i != n-1:
                logger.info(f"Waiting interval between actuations: {wait}s")
                sleep(wait)

            with sh.access:
                sh.CURRENT_RUN = sh.CURRENT_RUN + 1
                if sh.STATE == sh.state.ABORT:
                    logger.warning("Aborting current test")
                    sh.STATE = sh.state.READY
                    break
    
        
        logger.info("Test finished. Storing last parameters on database")
        # Store data on the database
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        time = now.strftime("%H:%M:%S")
        
        with sh.access:
            db = sql.connect("app.db")
            cur = db.cursor()

            cur.execute(f"UPDATE tests SET button = \"{sh.modulesData['button']}\", success = success || \"]\", error = \"{sh.ERROR}\", presses = {sh.CURRENT_RUN}, force_val = force_val || \"]\", time_val = time_val || \"]\", date = \"{date}\", time = \"{time}\" WHERE id = {rowID}")

            db.commit()
            cur.close()
            db.close()

        with sh.access:
            sh.STATE = sh.state.READY
            sh.CURRENT_RUN = 1
            sh.parameters.pressTime = 0
            sh.parameters.interval = 0
            sh.parameters.nTimes = 1

        logger.info("Test finished")
