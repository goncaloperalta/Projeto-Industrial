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
                sh.ERROR = 'SENSOR'
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
        sh.startTest.acquire()
        logger.info("Starting a test")
        
        # Set up initial states
        n = 0
        interval = 0
        readingsValData = []
        readingsTimeData = []
        feedbackButtonData = 'No Feedback'
        feedbackSuccessData = []
        with sh.access:
            n = sh.parameters.nTimes
            interval = sh.parameters.interval
            sh.STATE = sh.state.RUNNING
            sh.CURRENT_RUN = 0
            sh.ERROR = ''

        for i in range(n):
            with sh.access:
                if sh.ERROR != '':
                    break
            # Start SSH Module
            sh.startSSH.release()               # Signal to start the SSH client
            logger.info(f"Test {i+1}/{n}")

            # Wait until the other modules finish...
            sh.sensorReadingsReady.acquire()
            sh.feedbackReady.acquire()
            logger.info("Storing test data")

            # Store data on variable
            with sh.access:
                readingsValData.append(sh.readings['val'])
                readingsTimeData.append(sh.readings['time'])
                if sh.feedback['button'] != 'No Feedback' and sh.feedback['button'] != 'Not pressed':
                    feedbackButtonData = sh.feedback['button'] 
                print("Success ", sh.feedback['success'])
                feedbackSuccessData.append(sh.feedback['success'])

            # Wait interval
            if interval:
                logger.info("Waiting interval between actuations")
                sleep(interval)

            with sh.access:
                sh.CURRENT_RUN = sh.CURRENT_RUN + 1
                if sh.STATE == sh.state.ABORT:
                    sh.STATE = sh.state.READY
                    break
        
        logger.info("Storing all data on database")
        # Store data on the database
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        db = sql.connect("app.db")
        cur = db.cursor()
        cur.execute(f"INSERT INTO tests (button, success, force_val, time_val, date, time) VALUES (\"{feedbackButtonData}\", \"{feedbackSuccessData}\", \"{readingsValData}\", \"{readingsTimeData}\", \"{date}\", \"{time}\")")
        db.commit()
        cur.close()
        db.close()

        with sh.access:
            sh.STATE = sh.state.READY
            sh.CURRENT_RUN = 1
            sh.parameters.pressTime = 0
            sh.parameters.interval = 0
            sh.parameters.nTimes = 1

        logger.info("Test done")
