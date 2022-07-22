# load packages
from ntpath import join
from re import A
import pandas as pd
import seaborn as sns
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
from metrics_calculations import count_hits_per_ooi
# from tobii_to_cgom import reformat
import tobii_to_cgom_new
# from import_gui_input import get_variables_gui # the entire import_gui_input is executed already here!



# _____________ VARIABLES FROM GUI (replacement for GUI at this stage)
# region



# makes folder structure (input and output) and imports variables: 
# number_of_oois
# all_oois
# pixel distance
# etc. 

# replacing input from gui
def get_variables_gui():
    # number of OOIs
    global number_of_oois, pixel_distance, two_groups, comparing_groups, subs_trials, input_path, output_path, number_of_subs_trials, group_names

    ui_input_path =  'Data/gaze_input_1file_ogd_with_har/'
    input_path = Path(ui_input_path)

    ui_output_path = 'Output'
    output_path = Path(ui_output_path)

    group_names = []
    group_names = [f for f in sorted(os.listdir(input_path))] 

    number_of_oois = 3
    pixel_distance = 20
    two_groups = False
    comparing_groups = True
    subs_trials = True
    number_of_subs_trials = 4
        
get_variables_gui()

#test
#if comparing_groups == True:
#        print('juhu')
#print(input_path)

#endregion


# _____________ COPY FOLDER STRUCTURE TO OUTPUT
#region


# defining the function to ignore the files
# if present in any folder
def ignore_files(dir, files):
    return [f for f in files if os.path.isfile(os.path.join(dir, f))]
 
# calling the shutil.copytree() method and passing the src,dst,ignore parameter, and do not raise exception if dir already exists
shutil.copytree(input_path, output_path, ignore=ignore_files, dirs_exist_ok=True)


# find all participants per group and save in one list


# now create subdirectory for each participant
# or maybe create in the first analysis

#endregion


# _____________ GET LIST OF PARTICIPANTS AND TRIALS 
#region

# get list of all participants and all trials + tobii to cGOM

trials = [[]]
trial_paths = [[]]
participants = [[]]
participant_paths = [[]]
i=0 

if two_groups == True:

    for group_name in group_names:

        data_path = input_path / group_name

        # take all files from fixation input (only one input needed to extract participants and trials)
        filepaths = glob(join(data_path,'*_fixationdata.tsv'))

        # save all trials (trial[0] for group 1 and trial[1] for group 2)
        trial_paths[i] = [filepath[:-17] for filepath in filepaths]
        trials[i] = [os.path.basename(trial) for trial in trial_paths[i]]

        # save all participants (participants[0] for group 1 and participants[1] for group 2)
        participant_paths[i] = [filepath[:-25] for filepath in filepaths]
        participants[i] = [os.path.basename(participant) for participant in participant_paths[i]]



        i=i+1


else:

    data_path = input_path 

    filepaths =  glob(join(data_path,'*_fixationdata.tsv'))


    # save all trials (trial[0] for group 1 and trial[1] for group 2)
    trial_paths[i] = [filepath[:-17] for filepath in filepaths]
    trials[i] = [os.path.basename(trial) for trial in trial_paths[i]]

    # save all participants (participants[0] for group 1 and participants[1] for group 2)
    participant_paths[i] = [filepath[:-25] for filepath in filepaths]
    participants[i] = [os.path.basename(participant) for participant in participant_paths[i]]

    # transform tobii fixation_data into cGOM file
    fixation_files = [trial_path[i] + '_fixationdata.tsv' for trial_path in trial_paths]
    for filename in fixation_files:
        for trial_path in trial_paths[i]:
            tobii_to_cgom_new.reformat(filename, trial_path)

#endregion


# _____________ PREPARE DATA


input_types = ['fixationdata', 'saccadedata']

# what we have so far
#region
# list of participants + paths
# list of individual trials + paths
# ogd files of all trials (from tobii fixation files ending with _fixationdata.txt)

# now for loop through them to get individual analysis
# and make folder per subject
# but for now: analysis with one participant
#endregion


# loop through all the trials/participants to import data
#region


#for i in range(0,len(participants)): 

    #for j in range(len(participants[i])):
        # read data

#endregion



# import cGOM file and make OGD with HAR out of it 
# ---> SKIPPED FOR NOW
# and just import OGD with HAR file

# (OGD_with_actions) including assigned action per fixation (how I got it in python self assessment)
# format/columns: start_time, end_time, OOI_1, OOI_2, OOI_3, action
ogd_file = pd.read_csv(data_path / 'participant01_trial01_ogdhar.txt')
e=2

# all_oois = columns 2-(n-1) -> list: [OOI_1, OOI_2, OOI_3]



# _____________ Module: Add columns

# one module that will add more columns with information to each fixation in OGD_with_steps file per participant

# fixation time
# fixation object: OOI or something else
# entropy?
# K-coefficient?

# new name: OGD_final


# ____________ Module: second input required for other calculations
# entropy?
# K coefficient?

# ____________ Module: one module that calculates all metrics with the OGD_final

# name: metrics_calculations

#### functions:

# count total hits per OOI
# count hits per OOI per step

# calculate total dwell time per OOI
# calculate total dwell time per OOI per step
# calculate average dwell time per OOI
# calculate average dwell time per OOI per step

# calculate average fixation time per OOI
# calculate average fixation time per OOI per step









