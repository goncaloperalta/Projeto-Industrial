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
        
        # Set up initial states
        testData = {
            'button': '',
            'success': [],
            'error': '',
            'presses': 0,
            'parameters': [],
            'force_val': [],
            'time_val': [],
            'date': '',
            'time': ''
        }
        with sh.access:
            sh.resetModulesData()
            testData['parameters'] = [sh.parameters.pressTime, sh.parameters.nTimes, sh.parameters.interval]
            sh.STATE = sh.state.RUNNING
            sh.CURRENT_RUN = 0
            sh.ERROR = 'No Error'

        testI2C()
        for i in range(testData['parameters'][1]):
            with sh.access:
                if sh.ERROR != 'No Error':
                    break
            # Start SSH Module
            sh.startSSH.release()               # Signal to start the SSH client
            logger.info(f"Test {i+1}/{testData['parameters'][1]}")

            # Wait until the other modules finish...
            sh.sensorReadingsReady.acquire()
            sh.feedbackReady.acquire()
            logger.info("Storing test data")

            # Store data on variable
            with sh.access:
                testData['button'] = sh.modulesData['button']
                testData['success'].append(sh.modulesData['success'])
                testData['force_val'].append(sh.modulesData['force_val'])
                testData['time_val'].append(sh.modulesData['time_val'])

            # Wait interval
            if testData['parameters'][2]:
                logger.info("Waiting interval between actuations")
                sleep(testData['parameters'][2])

            with sh.access:
                sh.CURRENT_RUN = sh.CURRENT_RUN + 1
                if sh.STATE == sh.state.ABORT:
                    sh.STATE = sh.state.READY
                    break
    
        with sh.access:
            testData['presses'] = sh.CURRENT_RUN
            testData['error'] = sh.ERROR
            
        logger.info("Storing all data on database")
        # Store data on the database
        now = datetime.now()
        testData['date'] = now.strftime("%d-%m-%Y")
        testData['time'] = now.strftime("%H:%M:%S")

        db = sql.connect("app.db")
        cur = db.cursor()
        cur.execute(f"INSERT INTO tests (button, success, error, presses, parameters, force_val, time_val, date, time) VALUES (\"{testData['button']}\", \"{testData['success']}\", \"{testData['error']}\", {testData['presses']}, \"{testData['parameters']}\", \"{testData['force_val']}\", \"{testData['time_val']}\", \"{testData['date']}\", \"{testData['time']}\")")
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
