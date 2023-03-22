import logging, time
from collections import deque #

# interface to crazyflie
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper
# motion coommand system
from cflib.positioning.motion_commander import MotionCommander
# the following is for logging vars
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger

uri = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

phat = [0.,0.,0.]
vhat = 0.
ofxm = 0
pm = 0
tofxm = 0 # translation-induced optic flow
tofxm_smoothed = 0 # filtered version of tofx
go = 0 # mask variable

# time, x, y, z, vx, OFx
logger = LogConfig(name='state_and_meas', period_in_ms=30)
logger.add_variable('stateEstimate.x', 'float')
logger.add_variable('stateEstimate.y', 'float')
logger.add_variable('stateEstimate.z', 'float')
logger.add_variable('stateEstimate.vx', 'float')
logger.add_variable('kalman_pred.measNX', 'float') # optic flow
logger.add_variable('controller.r_pitch', 'float') # gyro pitch rate

of_scale_factor = 4.0926/2 # convert from pixels/s to rad/s
# translational optic flow in x direction
tofxm_data = [0,0,0,0,0,0,0,0,0,0] # create a queue for running average


def log_callback(timestamp, data, logconf):
    "print out state estimate, sensor values, and set them as global variables"
    global phat, vhat, ofxm, pm, tofxm, tofxm_smoothed # vars changed in this func
    phat = [data['stateEstimate.x'], data['stateEstimate.y'], data['stateEstimate.z']]
    vhat = data['stateEstimate.vx']
    ofxm = -data['kalman_pred.measNX'] * of_scale_factor
    pm = -data['controller.r_pitch'] # minus sign needed to fit convention
    tofxm = ofxm - pm
    # tofxm moving average: remove old, add new, and then compute
    tofxm_data.pop(0)
    tofxm_data.append(tofxm)
    tofxm_smoothed = sum(tofxm_data)/len(tofxm_data)

    print(f"{timestamp/1000:.3f},{phat[0]:.3f},{phat[1]:.3f},{phat[2]:.3f},{vhat:.3f},{ofxm:.3f},{pm:.3f},{tofxm:.3f},"
          f"{tofxm_smoothed:.3f},{go}")


# Initialize the low-level drivers
cflib.crtp.init_drivers()

dt = 1
gain = 0.7
altitude = 0.5

# the following with statement automatically takes care of closing connection if
# something goes wrong
with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
    scf.cf.log.add_config(logger)
    logger.data_received_cb.add_callback(log_callback)
    logger.start()
    with MotionCommander(scf, default_height=altitude) as mc:
        time.sleep(2)
        mc.start_forward(velocity=0.3) # move to excite dynamics
        time.sleep(1)

        ### your code here
        t0 = time.time()
        while (time.time() - t0) < 8:
            go = 1
            mc.start_forward(velocity=gain*tofxm_smoothed)
            time.sleep(dt)
        ###

        go = 0
        mc.start_forward(velocity=-0.3) # return to initial position
        time.sleep(1)
        mc.stop()
    time.sleep(0.5)
    logger.stop()
