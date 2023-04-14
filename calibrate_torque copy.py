import os
import sys
import exoboot
import time
import csv
import util
import constants
import config_util
# from playsound import playsound
# from pydub import AudioSegment
# from pydub.playback import play
 


def calibrate_encoder_to_ankle_conversion(exo: exoboot.Exo, only_write_if_new):
    '''This routine can be used to manually calibrate the relationship
    between ankle and motor angles. Move through the full RoM!!!'''
    exo.update_gains(Kp=400, Ki=50, Kd=0, ff=0)
    # sound = AudioSegment.from_mp3('mp3_sound.mp3')
    # exo.command_current(exo.motor_sign*1500)
    # exo.read_data()
    # motor_angle = exo.data.motor_angle
    # print('Motor Angle:', motor_angle)
    time.sleep(5)
    print('begin!')
    for _ in range(100000):
        time.sleep(1)
        print('3')
        time.sleep(1)
        print('2')
        time.sleep(1)
        print('1')
        time.sleep(1)
        # exo.write_data()
        # exo.command_motor_angle(motor_angle)
        # a = time.time()
        exo.command_torque(1.00)
        # print((time.time() - a))
        for i in range(10):
            time.sleep(0.1)
            exo.read_data()            
            exo.write_data(only_write_if_new=only_write_if_new)
        exo.command_torque(0)

        # play(sound[:500])
        # print('Ankle Torque:', exo.data.ankle_torque_from_current)
        # print('Motor Angle:', exo.data.motor_angle)
        # time.sleep(2)
        
    print('Done! File saved.')


if __name__ == '__main__':
    config, offline_test_time_duration, past_data_file_names = config_util.load_config_from_args()  # loads config from passed args
    file_ID = input(
        'Other than the date, what would you like added to the filename?')

    '''if sync signal is used, this will be gpiozero object shared between exos.'''
    sync_detector = config_util.get_sync_detector(config)

    '''Connect to Exos, instantiate Exo objects.'''
    exo_list = exoboot.connect_to_exos(config.IS_HARDWARE_CONNECTED,
        file_ID=file_ID, config=config, sync_detector=sync_detector)
    only_write_if_new = not config.READ_ONLY and config.ONLY_LOG_IF_NEW
    # print('Exo: ', exo_list)
    # if len(exo_list) > 1:
    #     raise ValueError("Just turn on one exo for calibration")
    # print('Is HD:', config.IS_HARDWARE_CONNECTED)
    config_saver = config_util.ConfigSaver(file_ID=file_ID, config=config)  # Saves config updates
    exo = exo_list[0]
    exo.standing_calibration()
    calibrate_encoder_to_ankle_conversion(exo=exo, only_write_if_new=only_write_if_new)
    exo.close()
