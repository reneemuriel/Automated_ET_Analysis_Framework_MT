# _____________ IMPORT
#region
from calendar import c
from ntpath import join
from re import A
from tkinter.tix import DirSelectBox
from zlib import DEF_BUF_SIZE
import pandas as pd
from pyparsing import col
import seaborn as sns # added to OGD_HMM
import numpy as np
import matplotlib.pyplot as plt
import shutil
from glob import glob
from pathlib import Path
# from os import path
import os
# import glob
from IPython.display import display
import math

# make requirements.txt that lists all packages that need to be installed in environment -

# import own modules
import add_columns as ac
import ooi_metrics
import general_metrics
import tobii_to_fixations
import tobii_to_saccades
import action_separation
# import make_gaze_OGD

#endregion


# _____________ VARIABLES FROM GUI (replacement for GUI at this stage)
# region

# replacing input from gui
def get_variables_gui():
    global ogd_exist, pixel_distance, subs_trials, input_path, output_path, number_of_subs_trials, group_names, action_analysis, ooi_analysis, general_analysis

    # choose input path (where group folders lie)
    ui_input_path =  'Data/gaze_input_tobii_and_ogd_short'
    input_path = Path(ui_input_path)

    # (choose) output path (group folders will be created in there)
    ui_output_path = 'Output'
    output_path = Path(ui_output_path)

    # general analysis
    general_analysis = False

    # action-based analysis
    action_analysis = True

    # ooi-based analysis
    ooi_analysis = False

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


# _____________ GET LIST & PATHS OF PARTICIPANTS AND TRIALS 
#region

trials = []
trial_paths = []
participants = []
participant_paths = []
i=0

for i in range (len(group_names)):

    group_path = input_path / group_names[i]
    output_path_groups = output_path / group_names[i]

    # copy group folder structure to output 
    os.makedirs(output_path / Path(group_names[i]), exist_ok=True)
    
    # take all files from tobii input (to get one name per trial)
    filepaths = glob(join(group_path,'*_tobii.tsv'))
    filenames =  [os.path.basename(filenames) for filenames in filepaths]
    
    # save all participants (participants[0] for group 1 and participants[1] for group 2)
    participant_paths.insert(i,[filepath[:-18] for filepath in filepaths]) # -18 to get participantxx
    participant_paths[i] = set(participant_paths[i])
    participants.insert(i,[os.path.basename(participant) for participant in participant_paths[i]])

    # iterate through participants to save trial paths per participants
    trials.append([])
    trial_paths.append([])
    j=0
    for j in range(len(participants[i])):

        # create folder for participant[i][j]
        os.makedirs(output_path / Path(group_names[i]) / Path(participants[i][j]), exist_ok=True)
        
        # list all trials of participant[i][j]
        trial_path_list = []
        for file in filepaths:
            if '{}'.format(participants[i][j]) in file:
                trial_name = file[:-10] # to get trialname only
                trial_path_list.append(trial_name)
                #trial_paths[i][j] = [file]
        trials_list = [os.path.basename(trial) for trial in trial_path_list]

        # add to trial list
        trials[i].insert(j,trials_list)
        #trials[i].insert(j,trials_list)
        # add to trial_paths list
        trial_paths[i].insert(j,trial_path_list) # for some reason adds a new empty element



#endregion


# _____________ GENERAL ANALYSIS (not OOI and not action based) 
#region

if general_analysis == True:
      
    i=0
    # iterate through groups
    for i in range(len(group_names)):
        # iterate through participants
        for j in range(len(participants[i])):
            # iterate through each trial
            k=0
            for trial_path in trial_paths[i][j]:
                
                tobiipath = trial_path + '_tobii.tsv' # new: changed from _fixationdata.tsv!

                # transform tobii into (not)cgom file 
                tobii_to_fixations.reformat(tobiipath, trial_path) # new: saved as _fixations.txt (not _cgom.txt anymore)

                # read newly created cgom file 
                fixationdata = pd.read_csv(trial_path + '_fixations.txt', sep='\t')

                # transform tobii into saccade file
                tobii_to_saccades.reformat(tobiipath, trial_path)

                # read saccade data
                saccadedata = pd.read_csv(trial_path + '_saccades.txt', sep='\t')

                # calculations of general metrics
                df_general_metrics = general_metrics.calculate_general_metrics(fixationdata, saccadedata,trials[i][j][k])

                # save df_general_metrics to csv
                participant_output_path = output_path / Path(group_names[i]) / Path(participants[i][j]) 
                df_general_metrics.to_csv(participant_output_path / '{}_general_analysis.csv'.format(trials[i][j][k]))
            
                k=k+1
        


#endregion


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

    for i in range(len(group_names)):
        # iterate through participants
        for j in range(len(participants[i])):
            # iterate through each trial
            k=0
            for trial_path in trial_paths[i][j]:

                ogd_data = pd.read_csv(trial_path + '_ogd.txt', sep='\t')

                # extract all OOIs
                all_ooi = ooi_metrics.extract_oois(ogd_data)

                # preprocess ogd data and add columns (fixation object and fixation time)
                ogd_final = ooi_metrics.prepare_ogd_file(ogd_data, pixel_distance)


                # calculate all ooi-based metrics
                df_ooi_metrics = ooi_metrics.calculate_ooi_metrics(ogd_final, all_ooi)

                # save df_ooi_metrics to csv
                participant_output_path = output_path / Path(group_names[i]) / Path(participants[i][j]) 
                df_ooi_metrics.to_csv(participant_output_path / '{}_ooi-based_ooi_analysis.csv'.format(trials[i][j][k]))
            
                # calculate all general ooi-based metrics
                df_general_ooi_metrics = ooi_metrics.calculate_general_ooi_metrics(ogd_final, all_ooi, trials[i][j][k])

                # save df_general_ooi_metrics
                df_general_ooi_metrics.to_csv(participant_output_path / '{}_ooi-based_general_analysis.csv'.format(trials[i][j][k]))

                k=k+1

#endregion


# _____________ ACTION-BASED ANALYSIS
#region

# only if specified to so do
if action_analysis == True:
    # loop per trial
    for i in range(len(group_names)):
        # iterate through participants
        for j in range(len(participants[i])):
            
            # iterate through each trial
            k=0
            for trial_path in trial_paths[i][j]:

                # import ogd data
                ogd_data = pd.read_csv(trial_path + '_ogd.txt', sep='\t')

                # extract all OOIs
                all_ooi = ooi_metrics.extract_oois(ogd_data)

                # preprocess ogd data and add columns (fixation object and fixation time)
                ogd_final = ooi_metrics.prepare_ogd_file(ogd_data, pixel_distance)

                # import fixationdata 
                fixationdata = pd.read_csv(trial_path + '_fixations.txt', sep='\t')

                # import saccadedata
                saccadedata = pd.read_csv(trial_path + '_saccades.txt', sep='\t')

                # extract actions
                all_actions = ogd_final['action'].unique().tolist()
               
                # get dataframe with actions + time from ogd dataframe
                df_actions = action_separation.action_times(ogd_final, fixationdata, all_actions)

                # save a list with the subsequent actions
                action_sequence = df_actions['action'].tolist()

                
                # general metrics
                # add change idx of fixationdata df to df_action
                df_actions = action_separation.fix_sac_data_per_action(df_actions, fixationdata, 'fixations')
                # add change idx of saccadedata df to df_action
                df_actions = action_separation.fix_sac_data_per_action(df_actions, saccadedata, 'saccades')

                # calculate general metrics with fixationdata and saccadedata
                general_metrics_action_df_list = action_separation.get_general_metrics_per_action_df_list(df_actions, fixationdata, saccadedata, trials[i][j][k])
                

                # calculate ooi-based metrics
                ooi_metrics_action_df_list, gen_ooi_metrics_action_df_list = action_separation.get_all_ooi_metrics_per_action_df_list(df_actions, ogd_final, all_ooi, trials[i][j][k])

                # ooi-based general metrics (based on ooi-based ooi metrics, so must be after their calculation)
                # gen_ooi_metrics_action_df_list = action_separation.get_general_ooi_metrics_per_action_df_list(df_actions, ogd_final, all_ooi, trials[i][j][k])

                # combine all dfs to one summary df per action
                for action in all_actions:

                    # extract indeces of the current action in the action_sequence (from df_actions)
                    idx_action_dfs = [ind for ind, ele in enumerate(action_sequence) if ele == action]

                    # output path to save dfs
                    participant_output_path = output_path / Path(group_names[i]) / Path(participants[i][j]) 

                    
                    ### summary of general metrics

                    # get summary of general metrics per action
                    df_summary_gen = action_separation.summary_general_metrics_per_action(general_metrics_action_df_list, idx_action_dfs)

                    # save output per action: general metrics
                    df_summary_gen.to_csv(participant_output_path / '{}_general_analysis_{}.csv'.format(trials[i][j][k], action))
                    

                    ### summary of ooi metrics

                    # get summary of ooi-based ooi metrics per action
                    df_summary_ooi = action_separation.summary_ooi_metrics_per_action(ooi_metrics_action_df_list, idx_action_dfs)

                    # save output per action: ooi-based ooi metrics
                    
                    df_summary_ooi.to_csv(participant_output_path / '{}_ooi-based_ooi_analysis_{}.csv'.format(trials[i][j][k], action))

                    # get summary of ooi-based ooi metrics per action
                    df_summary_ooi_gen = action_separation.summary_ooi_general_metrics_per_action(gen_ooi_metrics_action_df_list, idx_action_dfs, df_summary_ooi, general_metrics_action_df_list)

                    # save output per action: ooi-based general metrics
                    df_summary_ooi_gen.to_csv(participant_output_path / '{}_ooi-based_general_analysis_{}.csv'.format(trials[i][j][k], action))


                print(i,j,k)            
                k=k+1
     
      
    a=2






    

#endregion
e=2







