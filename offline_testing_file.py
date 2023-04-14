import pandas as pd

def get_offline_past_data_files(IS_HARDWARE_CONNECTED, past_data_file_names, offline_test_time_duration):

    if not IS_HARDWARE_CONNECTED:
        print('''
Offline Testing Detected.
''')
        try:
            offline_data_left= pd.read_csv(str(past_data_file_names) + '_LEFT.csv')
            offline_data_right = pd.read_csv(str(past_data_file_names) + '_RIGHT.csv')
        except:
            print('''No Files found by given name.''')
            print('''
Using Default Offline Data file: Default_Past_Data_LEFT.csv & Default_Past_Data_RIGHT.csv.
            ''')
            offline_data_left = pd.read_csv('Default_Past_Data_LEFT.csv')
            offline_data_right = pd.read_csv('Default_Past_Data_RIGHT.csv')

    else:
        if offline_test_time_duration:
            print('Offline Test Duration argument will not be considered, since hardware is connected.')
        offline_data_left = None
        offline_data_right = None

    return offline_data_left, offline_data_right
