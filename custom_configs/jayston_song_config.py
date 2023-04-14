import config_util

config = config_util.ConfigurableConstants()

config.TARGET_FREQ = 175
config.DO_DEPHY_LOG = False # True
config.NUM_STRIDES_REQUIRED = 2 # 3
config.FALL_FRACTION = 0.60 # 0.63
config.B_RATIO = 0
config.LEFT_STANDING_ANGLE = 2.68017578125  # Deg
config.RIGHT_STANDING_ANGLE = 0.83447265625  # Deg
config.TASK = config_util.Task.WALKING
config.STANCE_CONTROL_STYLE = config_util.StanceCtrlStyle.VIRTUALNEUROMUSCULARCONTROLLER
config.IS_HARDWARE_CONNECTED = True
config.DO_READ_SYNC = True
config.HARDWARE_FACTOR = 1.5
config.VNMC_GAIN = 1.2

# config.loop_time = 0
# config.actual_time = time.time()
# config.TARGET_FREQ = 200  # Hz
# config.ACTPACK_FREQ = 200  # Hz
# config.DO_DEPHY_LOG = True
# config.DEPHY_LOG_LEVEL = 4
# config.ONLY_LOG_IF_NEW = True
# config.MAX_ALLOWABLE_CURRENT = 20000  # mA
# # Gait State details
# config.HS_GYRO_THRESHOLD = 100
# config.HS_GYRO_FILTER_N = 2
# config.HS_GYRO_FILTER_WN = 3
# config.HS_GYRO_DELAY = 0.05
# config.SWING_SLACK = 10000
# config.TOE_OFF_FRACTION = 0.62
# config.REEL_IN_MV = 1200
# config.REEL_IN_SLACK_CUTOFF = 1200
# config.REEL_IN_TIMEOUT = 0.2
# config.NUM_STRIDES_REQUIRED = 3
# config.SWING_ONLY = False
# # 4 point Spline
# config.RISE_FRACTION = 0.2
# config.PEAK_FRACTION = 0.53
# config.FALL_FRACTION = 0.63
# config.PEAK_TORQUE = 5
# config.SPLINE_BIAS = 3  # Nm
# # Impedance
# config.K_VAL = 500
# config.B_VAL = 0
# config.B_RATIO = 0  # when B_VAL is a function of B_RATIO. 2.5 is approx. crit. damped
# config.SET_POINT = 0  # Deg
# config.READ_ONLY = False  # Does not require Lipos
# config.DO_READ_FSRS = False  # <--------
# config.DO_READ_SYNC = False  # <-------
# config.PRINT_HS = True  # Print heel strikes
# config.VARS_TO_PLOT = True
# config.DO_DETECT_SLIP = False
# config.SLIP_DETECT_ACTIVE = False
# config.DO_INCLUDE_GEN_VARS = False
# config.SLIP_DETECT_DELAY = 0
# config.DO_FILTER_GAIT_PHASE = True
# config.EXPERIMENTER_NOTES = 'Experimenter notes go here'