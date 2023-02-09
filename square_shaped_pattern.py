# basic script to take off and land the crazyflie while logging data
# Sawyer B. Fuller 2023.01.29

import logging
import time

# interface to crazyflie
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper
# motion command system
from cflib.positioning.motion_commander import MotionCommander
# the following is for logging vars
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger

uri = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

phat = [0.,0.,0.]
vhat = 0.
ofx = 0

# time, x, y, z, vx, OFx
logger = LogConfig(name='state_and_meas', period_in_ms=100)
logger.add_variable('stateEstimate.x', 'float')
logger.add_variable('stateEstimate.y', 'float')
logger.add_variable('stateEstimate.z', 'float')
logger.add_variable('stateEstimate.vx', 'float')
logger.add_variable('kalman_pred.measNX', 'float') # optic flow


def log_callback(timestamp, data, logconf):
    "print out state estimate, sensor values, and set them as global variables"
    global phat, vhat, ofx
    phat = [data['stateEstimate.x'], data['stateEstimate.y'], data['stateEstimate.z']]
    vhat = data['stateEstimate.vx']
    ofx = data['kalman_pred.measNX']
    print("%.3f,%1.3f,%1.3f,%1.3f,%1.3f,%d"%\
        (timestamp/1000, phat[0], phat[1], phat[2], vhat, ofx))


# Initialize the low-level drivers
cflib.crtp.init_drivers()

# the following with statement automatically takes care of closing connection if
# something goes wrong
with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
    scf.cf.log.add_config(logger)
    logger.data_received_cb.add_callback(log_callback)
    logger.start()
    with MotionCommander(scf, default_height=1) as mc:

        # ADD YOUR MOTION COMMANDS HERE

        time.sleep(1)
        mc.forward(0.5)
        time.sleep(1)
        mc.left(0.5)
        time.sleep(1)
        mc.back(0.5)
        time.sleep(1)
        mc.right(0.5)
        time.sleep(1)

        ##

        mc.stop()
    time.sleep(0.5)
    logger.stop()