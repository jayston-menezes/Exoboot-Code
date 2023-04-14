## Instructions for Running Exoboot Code for Offline Testing
####
`python main_loop.py -hd (hardware_connected) -ot (offline_hardware_test_duration) -pf (past_data_file_names) -c (config_file_name)`
####
Example: `python main_loop.py -hd False -ot 15 -pf Default_Past_Data -c jayston_song_config`
####
1) offline_hardware_test_duration is an optional argument to command run time for offline testing in seconds. Default value is run through full dataset
####
2) hardware_connected is an optional argument to switch from online to offline testing. Default is True.
####
3) past_data_file_names is an optional argument to enter names of past data files for offline testing. Default_Past_Data_LEFT.csv and Default_Past_Data_RIGHT.csv are default files.
####
4) config_file_name is an optional argument for custom config file name. Default config file is default_config.py
####
5) Please ensure all the libraries mentioned in the requirements.text are installed in the interpreter, as well as all the files are present in the same directory as main_loop.py.
####
6) For better understanding of the code, please refer Readme.md.
####
7) The code can be executed using multiple Stance Control Styles, that can be viewed and modified in config_util.py file, including Virtual Neuromuscular Controller.
####
8) The variable hardware_connected can be set in the custom config file through the IDE, as config.IS_HARDWARE_CONNECTED. Set True for Hardware Testing and False for Offline Testing 
####
9) The offline_hardware_test_duration argument is an optional argument for running the offline for the particular duration mentioned, in seconds.
####
10) The past_data_file_names is the name of the data files to iterate on for offline testing instead of exoboot readings.
####
11) Once the code is run and data is stored in the excel files, run plot_exo_data.py to get the plots of New Data vs. Loop Time or New Data & Old Data vs. Loop Time.
####
`python offline_plotting.py Past_Data New_Data`
####
Example: `python offlne_plotting.py Default_Past_Data New_Generated_Data` 
####
13) For Plotting line of code, Past_Data is the name of Past Data Files and New_Data is the name of New Data Files. The code will by default select the most recent left and right excel files as new data.
####
14) When prompted to Type Number and Range of Duration (in secs) for Plot + Enter. The following line of 3 arguments can be entered.

`choice_of_plot start_time_of_plot end_time_of_plot`
####
Example: `5 10 55`
####
15) For the above line,

    a) choice_of_plot is the desired plot from the given options, which is required.
    
    b) start_time_of_plot is the start time from which data should be plotted.
    
    c) end_time_of_plot is the time up to which data should be plotted. 

###Credits:
Dr. Max Shepherd - Original Writer of Exoboot Code for Online Testing.
####
Jayston Menezes & Dr. Seungmoon Song - Modified Exoboot Code for Offline Testing and Virtual Neuromuscular Controller. (October 2022)