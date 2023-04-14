'''This module holds constants and enums that are not intended to change'''
import numpy as np
from enum import Enum

DEFAULT_BAUD_RATE = 230400
TARGET_FREQ = 200
MAX_ANKLE_ANGLE = 95  # 83  # degrees, plantarflexion
MIN_ANKLE_ANGLE = -63  # -60  # degrees, dorsiflexion

# These polynomials are derived from the calibration routine (calibrate.py), analyzed with transmission_analysis.py
LEFT_ANKLE_TO_MOTOR = np.array(
    [4.93809841e-06, -9.37236976e-04, -1.91799432e-02,  1.49927256e+00,
    5.50444115e+02,  1.48885144e+04])
# [-7.46848531e-06,  6.16855504e-04,  7.54072228e-02,  7.50135291e-01,
#  -7.03196238e+02, -3.95156221e+04])
RIGHT_ANKLE_TO_MOTOR = np.array(
    [-7.58737033e-06,  1.26704441e-03,  1.43450629e-02, -2.14108179e+00,
    -5.47623518e+02,  9.62346598e+03])
# These points are used to create a Pchip spline, which defines the transmission ratio as a function of ankle angle
ANKLE_PTS = np.array([-60, -30, -20, 0, 15, 30, 40, 45.6, 55, 80])  # Deg
TR_PTS = np.array([23, 11.5, 11, 12,12.5, 12, 10, 8, 3, -9])  # Nm/Nm

#LEFT_ANKLE_ANGLE_OFFSET = -89.25  # deg 
LEFT_ANKLE_ANGLE_OFFSET = -95.55  # deg 

RIGHT_ANKLE_ANGLE_OFFSET = 91.5  # deg

# Add to these lists if dev_ids change, or new exos or actpacks are purchased!
RIGHT_EXO_DEV_IDS = [65295, 3148, 4648, 4923, 1234]
LEFT_EXO_DEV_IDS = [63086, 2873, 4632, 5246, 4321]

MS_TO_SECONDS = 0.001
# Converts raw Dephy encoder output to degrees
K_TO_NM_PER_DEGREE = 0  #
B_TO_NM_PER_DEGREE_PER_S = 0

ENC_CLICKS_TO_DEG = 1/(2**14/360)
# Getting the motor current to motor torque conversion is tricky, and any updates to
# the firmware should confirm that Dephy has not changed their internal current units.
# This constant assumes we are using q-axis current.
MOTOR_CURRENT_TO_MOTOR_TORQUE = 0.000146  # mA to Nm

# Dephy units to deg/s --experimentally estimated because their numbers are wrong
DEPHY_VEL_TO_MOTOR_VEL = 0.025*ENC_CLICKS_TO_DEG

# ankle_torque ~ AVERAGE_TRANSMISSION_RATIO*motor_torque
AVERAGE_TRANSMISSION_RATIO = 12.5  # Used to roughly map motor to ankle impedance

# https://dephy.com/wiki/flexsea/doku.php?id=controlgains
DEPHY_K_CONSTANT = 0.00078125
DEPHY_B_CONSTANT = 0.0002844
# Multiply Dephy's k_val by this to get a motor stiffness in Nm/deg
DEPHY_K_TO_MOTOR_K = MOTOR_CURRENT_TO_MOTOR_TORQUE *DEPHY_K_CONSTANT / (ENC_CLICKS_TO_DEG )
# Multiply Dephy's k_val by this to get an estimate of ankle stiffness in Nm/deg
DEPHY_K_TO_ANKLE_K = AVERAGE_TRANSMISSION_RATIO**2 * DEPHY_K_TO_MOTOR_K

# Inferred from https://invensense.tdk.com/products/motion-tracking/6-axis/mpu-6050/
ACCEL_GAIN = 1 / 8192  # LSB -> gs
# Inferred from https://invensense.tdk.com/products/motion-tracking/6-axis/mpu-6050/
GYRO_GAIN = 1 / 32.75  # LSB -> deg/s

LOGGING_FREQ = 200
# Dephy recommends as a starting point: Kp=250, Ki=200, Kd=0, FF=100
# DEFAULT_KP = 300  # updated from 250 on 3/10/2021
# DEFAULT_KI = 360  # updated from 250 on 3/10/2021
# DEFAULT_KD = 5
DEFAULT_KP = 40
DEFAULT_KI = 400
DEFAULT_KD = 0
# Feedforward term. "0 is 0% and 128 (possibly unstable!) is 100%."
DEFAULT_FF = 120  # 126
DEFAULT_SWING_KP = 150
DEFAULT_SWING_KI = 50
DEFAULT_SWING_KD = 0
DEFAULT_SWING_FF = 0

# TODO(maxshep) raise these when it seems safe
MAX_ALLOWABLE_VOLTAGE_COMMAND = 3000  # mV
MAX_ALLOWABLE_CURRENT_COMMAND = 25000  # mA
MAX_ALLOWABLE_K_COMMAND = 8000  # Dephy Internal Units
MAX_ALLOWABLE_B_COMMAND = 5500  # NOT TESTED!


class Side(Enum):
    RIGHT = 1
    LEFT = 2
    NONE = 3

class ControllerUsed(Enum):
    SoftReelOutController = 1   # "Soft Reel Out Controller"
    StalkController = 2         # "Stalk Controller"
    SmoothReelInController = 3  # "Smooth Reel In Controller"
    VirtualNeuromusuclarController = 4   # "Virtual Neuromuscular Controller"
    SawickiWickiController = 5           # "SawickiWicki Controller"
    ConstantTorqueController = 6         # "Constant Torque Controller"
    GenericSplineController = 7          # "Generic Spline Controller"
    FourPointSplineController = 8        # "Four Point Spline Controller"
    BallisticReelInController = 9        # "Ballistic Reel In Controller"
    GenericImpedanceController = 10      # "Generic Impedance Controller"
    FivePointSplineController = 11       # "Five Point Spline Controller"


class ControlState(Enum):
    ReelOutState = 1    # "Reel Out State"
    SwingState = 2      # "Swing State (Swing Only)"
    ReelInState = 3     # "Reel In State"
    StanceState = 4     # "Stance State"
    StandingState = 5   # "Standing State"
    SlipState = 6       # "Slip State"


# RPi's GPIO pin numbers (not physical pin number) for FSR testing
LEFT_HEEL_FSR_PIN = 17
LEFT_TOE_FSR_PIN = 18
RIGHT_HEEL_FSR_PIN = 24
RIGHT_TOE_FSR_PIN = 25

# RPi's GPIO pin numbers (not physical pin number) for Sync signal
SYNC_PIN = 16
