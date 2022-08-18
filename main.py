# _____________ IMPORT
#region
from calendar import c
from ntpath import join
from re import A
from zlib import DEF_BUF_SIZE
import pandas as pd
import seaborn as sns # added to OGM_HMM
import numpy as np
import matplotlib.pyplot as plt
import shutil
from glob import glob
from pathlib import Path
# from os import path
import os
# import glob
from IPython.display import display

# make requirements.txt that lists all packages that need to be installed in environment -

# import own modules
import add_columns as ac
import ooi_metrics
import tobii_to_cgom_new
# import make_gaze_OGD

# from import_gui_input import get_variables_gui # the entire import_gui_input is executed already here!


#endregion


# _____________ VARIABLES FROM GUI (replacement for GUI at this stage)
# region

# replacing input from gui
def get_variables_gui():
    global ogd_exist, pixel_distance, subs_trials, input_path, output_path, number_of_subs_trials, group_names, action_analysis, ooi_analysis, general_analysis

    # choose input path (where group folders lie)
    ui_input_path =  'Data/gaze_input_1file_ogd_with_har'
    input_path = Path(ui_input_path)

    # (choose) output path (group folders will be created in there)
    ui_output_path = 'Output'
    output_path = Path(ui_output_path)

    # general analysis
    general_analysis = True

    # action-based analysis
    action_analysis = False

    # ooi-based analysis
    ooi_analysis = True

    # import ogd file if it already exists
    if ooi_analysis == True:
        # ask if ogd file exists
        ogd_exist = True


    ## groups

    # same folder structure for one group and multiple groups: input/groupname/data
    group_names = []
    group_names = [f for f in sorted(os.listdir(input_path))] 


    # multiple trials per participant?
    subs_trials = True
    number_of_subs_trials = 4

    # others
    pixel_distance = 20

    
get_variables_gui()


#endregion


# _____________ OTHER VARIABLES / DEFINITIONS / FUNCTIONS
#region

## for copying folder structure to output 
# defining the function to ignore the files if present in any folder
def ignore_files(dir, files):
    return [f for f in files if os.path.isfile(os.path.join(dir, f))]

#endregion



# _____________ GET LIST & PATHS OF PARTICIPANTS AND TRIALS 
#region

trials = [[]]
trial_paths = [[]]
participants = [[]]
participant_paths = [[]]
i=0 

for group_name in group_names:

    data_path = input_path / group_name
    output_path_groups = output_path / group_name

    # copy folder structure to output (one folder per participant)
    shutil.copytree(data_path, output_path_groups, ignore=ignore_files, dirs_exist_ok=True)

    # take all files from fixation input (only one input type is needed to extract participants and trial names)
    filepaths = glob(join(data_path,'*_fixationdata.tsv'))

    # save all trials (trial[0] for group 1 and trial[1] for group 2)
    trial_paths[i] = [filepath[:-17] for filepath in filepaths]
    trials[i] = [os.path.basename(trial) for trial in trial_paths[i]]

    # save all participants (participants[0] for group 1 and participants[1] for group 2)
    participant_paths[i] = [filepath[:-25] for filepath in filepaths] # -25 to get filename
    participants[i] = [os.path.basename(participant) for participant in participant_paths[i]]

    i=i+1

#endregion


# _____________ GENERAL ANALYSIS (not OOI and not action based) 
#region

if general_analysis == True:
      
    i=0
    # iterate through groups
    for i in range (len(group_names)):
        # iterate through trials per group
        for trial_path in trial_paths[i]:

            # transform tobii into (not)cgom file (in all cases)
            filename = trial_path + '_fixationdata.tsv'
            tobii_to_cgom_new.reformat(filename, trial_path)

            # read newly created cgom file 
            cgom_data = pd.read_csv(trial_path + '_cgom.txt', sep='\t')

            # calculations of general metrics
            a=2
        i=i+1






# _____________ OOI-BASED ANALYSIS


#region

# only run if specified to do so 
if ooi_analysis == True:

    # ______ PREPARE DATA

    # if ogd files do not exist yet, create them
    if ogd_exist == False:
        # run the same as in suchitas GUI 
        # let user add labels & weights
        # run make_gaze_OGD 
        # and safe new files to trial path (similar to above)
        # give them the name: participant01_trial03_ogd.txt
        a=1
    
    # go through each trial
    for i in range (len(group_names)):
        for trial_path in trial_paths[i]:
            ogd_data = pd.read_csv(trial_path + '_ogd.txt', sep='\t')

            # extract oois from ogd_data
            if ogd_data.columns.values[-1] == 'action' or 'Action':
            # format: start_time, end_time, OOI_1, OOI_2, OOI_3, action
                all_ooi = ogd_data.columns.values.tolist()[2:-1]
            else:
                # format: start_time, end_time, OOI_1, OOI_2, OOI_3
                all_ooi = ogd_data.columns.values.tolist()[2:]


            # add columns to ogd_data (fixation object, fixation time)
            ogd_final = ogd_data
            ac.add_fixation_object(ogd_final,pixel_distance)
            ac.add_fixation_time(ogd_final)
        

            # calculate all ooi-based metrics
            df_ooi_metrics = ooi_metrics.calculate_ooi_metrics(ogd_final, all_ooi)

            display(df_ooi_metrics)

            # calculate all general ooi-based metrics
            ooi_metrics.calculate_general_ooi_metrics(ogd_final, all_ooi)



e=3








