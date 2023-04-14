import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os
import argparse


def print_options(is_vnmc_included_in_past_data, is_vnmc_included_in_new_data):
    if is_vnmc_included_in_past_data or is_vnmc_included_in_new_data:
        print("""1: All Acceleration & Gyro Data
2: Motor Angle, Velocity & Current data
3: Ankle Angle, Velocity & Torque from Current Data
4: Did Heel Strike (Boolean), Did Toe Off (Boolean) & gait_phase data
5: Command Current, Position and Torque data
6: Slack & Temperature data
7: Controller Implemented and Control State Data
8: Muscle Tendon Unit (MTU) Length, Velocity, Torque, Force, Muscle Stimulation and Ankle Angle""")
    else:
        print("""1: All Acceleration & Gyro Data
2: Motor Angle, Velocity & Current data
3: Ankle Angle, Velocity & Torque from Current Data
4: Did Heel Strike (Boolean), Did Toe Off (Boolean) & gait_phase data
5: Command Current, Position and Torque data
6: Slack & Temperature data
7: Controller Implemented and Control State Data""")

def get_len_from_seconds(length_1, length_2, new_data_file):
    
    length_list = list()
    for i in [length_1, length_2]:
        for j in range(len(new_data_file)):
            if float(new_data_file['loop_time'][j]) >= float(i):
                length_list.append(j)
                break
            else:
                pass
    length_1 = length_list[0]
    length_2 = length_list[1]

    return length_1, length_2

def get_data_from_input(input_from_user, new_data_file, past_data_file):
    list_of_input = input_from_user.split()
    try:
        if len(list_of_input) == 1:
            choice_of_plot = str(input_from_user)
            length_1 = 0
            length_2 = 5
        elif len(list_of_input) == 2:
            choice_of_plot = str(list_of_input[0])
            length_1 = 0
            length_2 = float(list_of_input[1])
        elif len(list_of_input) == 3:
            choice_of_plot = str(list_of_input[0])
            length_1 = float(list_of_input[1])
            length_2 = float(list_of_input[2])
        elif not list_of_input:
            choice_of_plot, length_1, length_2 = '', None, None
            return length_1, length_2, choice_of_plot
        else:
            choice_of_plot, length_1, length_2 = 'a', None, None
            return length_1, length_2, choice_of_plot
    except:
        print('Input not recognized. Please enter float and integers only.')
        return

    length_1, length_2 = get_len_from_seconds(length_1, length_2, new_data_file)
    
    return length_1, length_2, choice_of_plot

def plotter(new_data_file, past_data_file):

    loop_choice_of_plot = True

    print('')
    try:
        for find_vnmc in range(len(past_data_file)):
            if past_data_file['controller'][find_vnmc] == "ControllerUsed.VirtualNeuromusuclarController":
                is_vnmc_included_in_past_data = True
                print('Info: Virtual Neuromuscular Controller found in past data.')
                break
            else:
                is_vnmc_included_in_past_data = False
        print('')
    except:
        is_vnmc_included_in_past_data = False
        print('Info: Virtual Neuromuscular Controller not found in past data.')
        print('')

    try:
        for find_vnmc in range(len(new_data_file)):
            if new_data_file['controller'][find_vnmc] == "ControllerUsed.VirtualNeuromusuclarController":
                is_vnmc_included_in_new_data = True
                print('Info: Virtual Neuromuscular Controller found in new data.')
                break
            else:
                is_vnmc_included_in_new_data = False
        print('')
    except:
        is_vnmc_included_in_new_data = False
        print('Info: Virtual Neuromuscular Controller not found in new data.')
        print('')

    print_options(is_vnmc_included_in_past_data, is_vnmc_included_in_new_data)

    while loop_choice_of_plot:
        print('')
        input_from_user = input('Type Number and Range of Duration (in secs) for Plot + Enter. Press only Enter to Exit: ')
        length_1, length_2, choice_of_plot = get_data_from_input(input_from_user, new_data_file, past_data_file)
        past_data_loop_time = past_data_file['loop_time'][length_1:length_2]
        new_data_loop_time = new_data_file['loop_time'][length_1:length_2]
        if choice_of_plot == '1':
            past_data_file_accel_x = past_data_file['accel_x'][length_1:length_2]
            past_data_file_accel_y = past_data_file['accel_y'][length_1:length_2]
            past_data_file_accel_z = past_data_file['accel_z'][length_1:length_2]
            past_data_file_gyro_x = past_data_file['gyro_x'][length_1:length_2]
            past_data_file_gyro_y = past_data_file['gyro_y'][length_1:length_2]
            past_data_file_gyro_z = past_data_file['gyro_z'][length_1:length_2]
            new_data_file_accel_x = new_data_file['accel_x'][length_1:length_2]
            new_data_file_accel_y = new_data_file['accel_y'][length_1:length_2]
            new_data_file_accel_z = new_data_file['accel_z'][length_1:length_2]
            new_data_file_gyro_x = new_data_file['gyro_x'][length_1:length_2]
            new_data_file_gyro_y = new_data_file['gyro_y'][length_1:length_2]
            new_data_file_gyro_z = new_data_file['gyro_z'][length_1:length_2]
            fig = make_subplots(rows=3, cols=2, subplot_titles=(
            "Acceleration X", "Acceleration Y", "Acceleration Z", "Gyro X", "Gyro Y", "Gyro Z"))
            fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_accel_x, name='Past Acceleration X Data',
                         line = dict(color='gray', width=5)), row=1, col=1)
            fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_accel_y, name='Past Acceleration Y Data',
                         line = dict(color='gray',width=5)), row=2, col=1)
            fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_accel_z, name='Past Acceleration Z Data',
                         line = dict(color='gray',width=5)), row=3, col=1)
            fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_gyro_x, name='Past Gyro X Data',
                         line = dict(color='gray',width=5)), row=1, col=2)
            fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_gyro_y, name='Past Gyro Y Data',
                         line = dict(color='gray',width=5)), row=2, col=2)
            fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_gyro_z, name='Past Gyro Z Data',
                         line = dict(color='gray',width=5)), row=3, col=2)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_accel_x, name='New Acceleration X Data',
                                     line=dict(width=1)), row=1, col=1)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_accel_y, name='New Acceleration Y Data',
                                     line = dict(width=1)), row=2, col=1)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_accel_z, name='New Acceleration Z Data',
                                     line = dict(width=1)), row=3, col=1)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_gyro_x, name='New Gyro X Data',
                                     line = dict(width=1)), row=1, col=2)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_gyro_y, name='New Gyro Y Data',
                                     line = dict(width=1)), row=2, col=2)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_gyro_z, name='New Gyro Z Data',
                                     line = dict(width=1)), row=3, col=2)
            fig.update_layout(height=1500, width=1850,
                              title_text="Acceleration & Gyro Data - Time (X-axis) vs. Data (Y-axis)")
        elif choice_of_plot == '2':
            past_data_file_motor_angle = past_data_file['motor_angle'][length_1:length_2]
            past_data_file_motor_velocity = past_data_file['motor_velocity'][length_1:length_2]
            past_data_file_motor_current = past_data_file['motor_current'][length_1:length_2]
            new_data_file_motor_angle = new_data_file['motor_angle'][length_1:length_2]
            new_data_file_motor_velocity = new_data_file['motor_velocity'][length_1:length_2]
            new_data_file_motor_current = new_data_file['motor_current'][length_1:length_2]
            fig = make_subplots(rows=3, cols=1, subplot_titles=("Motor Angle", "Motor Velocity", "Motor Current"))
            fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_motor_angle, name='Past Motor Angle Data',
                         line = dict(color='gray', width=5)), row=1, col=1)
            fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_motor_velocity, name='Past Motor Velocity Data',
                         line = dict(color='gray', width=5)), row=2, col=1)
            fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_motor_current, name='Past Motor Current Data',
                         line = dict(color='gray', width=5)), row=3, col=1)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_motor_angle, name='New Motor Angle Data',
                                     line=dict(width=1)), row=1, col=1)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_motor_velocity, name='New Motor Velocity Data',
                           line=dict(width=1)), row=2, col=1)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_motor_current, name='New Motor Current Data',
                                     line=dict(width=1)), row=3, col=1)
            fig.update_layout(height=1500, width=1850,
                              title_text="Motor Data - Time (X-axis) vs. Data (Y-axis)")
        elif choice_of_plot == '3':
            past_data_file_ankle_angle = past_data_file['ankle_angle'][length_1:length_2]
            past_data_file_ankle_velocity = past_data_file['ankle_velocity'][length_1:length_2]
            past_data_file_ankle_torque_from_current = past_data_file['ankle_torque_from_current'][length_1:length_2]
            new_data_file_ankle_angle = new_data_file['ankle_angle'][length_1:length_2]
            new_data_file_ankle_velocity = new_data_file['ankle_velocity'][length_1:length_2]
            new_data_file_ankle_torque_from_current = new_data_file['ankle_torque_from_current'][length_1:length_2]
            fig = make_subplots(rows=3, cols=1, subplot_titles=("Ankle Angle", "Ankle Velocity", "Ankle Torque from Current"))
            fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_ankle_angle, name='Past Ankle Angle Data',
                         line = dict(color='gray', width=5)), row=1, col=1)
            fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_ankle_velocity, name='Past Ankle Velocity Data',
                         line = dict(color='gray', width=5)), row=2, col=1)
            fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_ankle_torque_from_current, name='Past Ankle Torque from '
                         'Current Data', line = dict(color='gray', width=5)), row=3, col=1)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_ankle_angle, name='New Ankle Angle Data',
                                     line=dict(width=1)), row=1, col=1)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_ankle_velocity, name='New Ankle Velocity Data',
                           line=dict(width=1)), row=2, col=1)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_ankle_torque_from_current, name='New Ankle Torque from'
                           'Current Data', line=dict(width=1)), row=3, col=1)
            fig.update_layout(height=1500, width=1850, title_text="Ankle Data - Time (X-axis) vs. Data (Y-axis)")
        elif choice_of_plot == '4':
            past_data_file_did_heel_strike = past_data_file['did_heel_strike'][length_1:length_2]
            past_data_file_did_toe_off = past_data_file['did_toe_off'][length_1:length_2]
            past_data_file_gait_phase = past_data_file['gait_phase'][length_1:length_2]
            new_data_file_did_heel_strike = new_data_file['did_heel_strike'][length_1:length_2]
            new_data_file_did_toe_off = new_data_file['did_toe_off'][length_1:length_2]
            new_data_file_gait_phase = new_data_file['gait_phase'][length_1:length_2]
            fig = make_subplots(rows=3, cols=1, subplot_titles=("Did Heel Strike", "Did Toe Off", "Gait Phase"))
            fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_did_heel_strike, name='Past Did Heel Strike Data',
                         line = dict(color='gray', width=5)), row=1, col=1)
            fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_did_toe_off, name='Past Did Toe Off Data',
                         line = dict(color='gray', width=5)), row=2, col=1)
            fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_gait_phase, name='Past Gait PhaseData',
                         line = dict(color='gray', width=5)), row=3, col=1)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_did_heel_strike, name='New Did Heel Strike Data',
                           line=dict(width=1)), row=1, col=1)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_did_toe_off, name='New Did Toe Off Data',
                                     line=dict(width=1)), row=2, col=1)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_gait_phase, name='New Gait Phase Data',
                                     line=dict(width=1)), row=3, col=1)
            fig.update_layout(height=1500, width=1850, title_text="Gait Data - Time (X-axis) vs. Data (Y-axis)")
        elif choice_of_plot == '5':
            past_data_file_commanded_current = past_data_file['commanded_current'][length_1:length_2]
            past_data_file_commanded_position = past_data_file['commanded_position'][length_1:length_2]
            past_data_file_commanded_torque = past_data_file['commanded_torque'][length_1:length_2]
            new_data_file_commanded_current = new_data_file['commanded_current'][length_1:length_2]
            new_data_file_commanded_position = new_data_file['commanded_position'][length_1:length_2]
            new_data_file_commanded_torque = new_data_file['commanded_torque'][length_1:length_2]
            fig = make_subplots(rows=3, cols=1, subplot_titles=("Commanded Current", "Commanded Position", "Commanded Torque"))
            fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_commanded_current, name='Past Commanded Current Data',
                         line = dict(color='gray', width=5)), row=1, col=1)
            fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_commanded_position, name='Past Commanded Position Data',
                         line = dict(color='gray', width=5)),row=2, col=1)
            fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_commanded_torque, name='Past Commanded Torque Data',
                         line = dict(color='gray', width=5)), row=3, col=1)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_commanded_current, name='New Commanded Current Data',
                           line=dict(width=1)), row=1, col=1)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_commanded_position, name='New Commanded Position Data',
                           line=dict(width=1)), row=2, col=1)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_commanded_torque, name='New Commanded Torque Data',
                           line=dict(width=1)), row=3, col=1)
            fig.update_layout(height=1500, width=1850, title_text="Commanded Data - Time (X-axis) vs. Data (Y-axis)")
        elif choice_of_plot == '6':
            past_data_file_slack = past_data_file['slack'][length_1:length_2]
            past_data_file_temperature = past_data_file['temperature'][length_1:length_2]
            new_data_file_slack = new_data_file['slack'][length_1:length_2]
            new_data_file_temperature = new_data_file['temperature'][length_1:length_2]
            fig = make_subplots(rows=2, cols=1, subplot_titles=("Slack", "Temperature"))
            fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_slack, name='Past Slack Data',
                         line = dict(color='gray', width=5)), row=1, col=1)
            fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_temperature, name='Past Temperature Data',
                         line = dict(color='gray', width=5)), row=2, col=1)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_slack, name='New Slack Data',
                                     line=dict(width=1)), row=1, col=1)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_temperature, name='New Temperature Data',
                                     line=dict(width=1)), row=2, col=1)
            fig.update_layout(height=1000, width=1850, title_text="Slack & Temperature - Time (X-axis) vs. Data (Y-axis)")
        elif choice_of_plot == '7':
            new_data_file_controller = new_data_file['controller'][length_1:length_2]
            new_data_file_control_state = new_data_file['control_state'][length_1:length_2]
            fig = make_subplots(rows=1, cols=2,
                                subplot_titles=("New Data Controller Implemented", "New Data Control State"))
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_controller), row=1, col=1)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_control_state), row=1, col=2)
            fig.update_layout(height=1000, width=1700,
                              title_text="Controller Implemented & Control State - Time (X-axis) vs. Data (Y-axis)")
        elif choice_of_plot == '8':
            new_data_file_vnmc_torque = new_data_file['vnmc_torque'][length_1:length_2]
            new_data_file_mtu_force = new_data_file['mtu_force'][length_1:length_2]
            new_data_file_length_ce = new_data_file['length_CE'][length_1:length_2]
            new_data_file_velocity_ce = new_data_file['velocity_CE'][length_1:length_2]
            if is_vnmc_included_in_past_data:
                fig = make_subplots(rows=3, cols=2, subplot_titles=("VNMC Torque", "Length CE", "Velocity CE", "MTU Force", "Ankle Angle", "Muscle Stimulation"))
                past_data_file_vnmc_torque = past_data_file['vnmc_torque'][length_1:length_2]
                past_data_file_mtu_force = past_data_file['mtu_force'][length_1:length_2]
                past_data_file_length_ce = past_data_file['length_CE'][length_1:length_2]
                past_data_file_velocity_ce = past_data_file['velocity_CE'][length_1:length_2]
                fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_vnmc_torque, name='Past VNMC Torque Data',
                         line = dict(color='gray', width=5)), row=1, col=1)
                fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_mtu_force, name='Past MTU Force Data',
                         line = dict(color='gray', width=5)), row=2, col=1)
                fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_length_ce, name='Past Length CE Data',
                         line = dict(color='gray', width=5)), row=3, col=1)
                fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_velocity_ce, name='Past Velocity CE Data',
                         line = dict(color='gray', width=5)), row=1, col=2)
                fig.update_layout(height=1500, width=1750,
                                  title_text="Virtual Neuromuscular Controller Parameters - Time (X-axis) vs. Data (Y-axis)")
            else:
                fig = make_subplots(rows=3, cols=2, subplot_titles=("VNMC Torque", "Length CE", "Velocity CE", "MTU Force", "Ankle Angle", "Muscle Stimulation"))
                fig.update_layout(height=1500, width=1750, title_text="Virtual Neuromuscular Controller Parameters - Time (X-axis) vs. Data (Y-axis)")
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_vnmc_torque, name='New VNMC Torque Data',
                         line = dict(width=1)), row=1, col=1)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_mtu_force, name='New MTU Force Data',
                         line = dict(width=1)), row=2, col=1)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_length_ce, name='New Length CE Data',
                         line = dict(width=1)), row=3, col=1)
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_velocity_ce, name='New Velocity CE Data',
                         line = dict(width=1)), row=1, col=2)
            new_data_file_ankle_angle = new_data_file['ankle_angle'][length_1:length_2]
            past_data_file_ankle_angle = past_data_file['ankle_angle'][length_1:length_2]
            fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_ankle_angle, name='New Ankle Angle Data',
                                     line=dict(width=1)), row=2, col=2)
            fig.add_trace(go.Scatter(x=past_data_loop_time, y=past_data_file_ankle_angle, name='Past Ankle Angle Data',
                                     line=dict(color='gray', width=5)), row=2, col=2)
            try:
                new_data_file_m_stim = new_data_file['muscle_stimulation'][length_1:length_2]
                fig.add_trace(go.Scatter(x=new_data_loop_time, y=new_data_file_m_stim, name='New Muscle Stimulation Data',
                                         line=dict(width=1)), row=3, col=2)
            except:
                pass
            try:
                past_data_file_m_stim = past_data_file['muscle_stimulation'][length_1:length_2]
                fig.add_trace(go.Scatter(x=new_data_loop_time, y=past_data_file_m_stim, name='Past Muscle Stimulation Data',
                                         line=dict(color='gray', width=5)), row=3, col=2)
            except:
                pass

        elif choice_of_plot == ' ' or choice_of_plot == '':
            loop_choice_of_plot = False
        else:
            print('')
            print('Input not recognized. Please enter the correct number for corresponding plot and duration in seconds.')
            print('')
            choice_of_plot = None

        if loop_choice_of_plot == True and choice_of_plot != None:
            fig.show()

def parse_args():
    my_parser = argparse.ArgumentParser(prog='Exoboot Code',
                                        description='Run Exoboot Controllers',
                                        epilog='Enjoy the program! :)')
    my_parser.add_argument('-pf', '--past_data_files', action='store',
                           type=str, required=False, default=False)
    my_parser.add_argument('-nf', '--new_data_files', action='store',
                           type=str, required=False, default=False)
    args = my_parser.parse_args()
    return args

if __name__ == '__main__':

    args = parse_args()

    past_data_file_name = args.past_data_files
    new_data_file_name = args.new_data_files

    if past_data_file_name:
        # Using Input from User
        past_data_file_left = pd.read_csv(str(past_data_file_name)+'_LEFT.csv')
        past_data_file_right = pd.read_csv(str(past_data_file_name) + '_RIGHT.csv')
    else:
        # Using Default files
        past_data_file_left = pd.read_csv("Default_Past_Data_LEFT.csv")
        past_data_file_right = pd.read_csv("Default_Past_Data_RIGHT.csv")

    if new_data_file_name:
        # Using Input from User
        new_data_file_left = pd.read_csv('exo_data/' + str(past_data_file_name)+'_LEFT.csv')
        new_data_file_right = pd.read_csv('exo_data/' + str(past_data_file_name) + '_RIGHT.csv')
    else:
        # Using most recent files
        file_list = os.listdir("exo_data")
        file_list.sort(reverse=True)
        new_data_file_right = pd.read_csv('exo_data/' + str(file_list[0]))
        new_data_file_left = pd.read_csv('exo_data/' + str(file_list[1]))

    print('''Input Desired Exoboot Side Plot
0: Exit Code
1: Left Side
2: Right Side''')
    while True:
        print('')
        left_or_right_or_exit = input('Enter Left Side or Right Side or Exit:')
        if left_or_right_or_exit == '1':
            plotter(new_data_file_left, past_data_file_left)
        elif left_or_right_or_exit == '2':
            plotter(new_data_file_right, past_data_file_right)
        elif left_or_right_or_exit == '0':
            print('')
            print('Exiting Plotting Code. Thank you!')
            break
        else:
            print('Input not understood. Please enter desired input.')
