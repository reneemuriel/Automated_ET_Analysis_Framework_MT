# _____________ IMPORT
#region
from calendar import c
from cmath import nan
from ntpath import join
#from pprint import pp
from re import A
from tkinter.tix import DirSelectBox
from tokenize import group
from zlib import DEF_BUF_SIZE
from matplotlib import test
import pandas as pd
from pyparsing import col
import seaborn as sns # added to OGD_HMM
import numpy as np
import matplotlib.pyplot as plt
import shutil
from glob import glob
from pathlib import Path
import statistics
# from os import path
import os
# import glob
from IPython.display import display
import math
import re


# make requirements.txt that lists all packages that need to be installed in environment -

# import own modules
import add_columns as ac
import ooi_metrics
import general_metrics
import tobii_to_fixations
import tobii_to_saccades
import action_separation
import kcoefficient_analysis
import visualisations
import summary_calculations
# import make_gaze_OGD

#endregion


# _____________ VARIABLES FROM GUI (replacement for GUI at this stage)
# region

# replacing input from gui
def get_variables_gui():
    global ogd_exist, pixel_distance, subs_trials, input_path, output_path, number_of_subs_trials, group_names, action_analysis, ooi_analysis, general_analysis, kcoeff_analysis, all_actions

    # choose input path (where group folders lie)
    ui_input_path =  'Data/gaze_input_tobii_and_ogd'
    input_path = Path(ui_input_path)

    # (choose) output path (group folders will be created in there)
    ui_output_path = 'Output'
    output_path = Path(ui_output_path)

    # general analysis
    general_analysis = True

    # calculate k-coefficient
    kcoeff_analysis = False

    # action-based analysis (needs ooi-based analysis to be ran first, because dirs are created, will be changed!)
    action_analysis = False

    # ooi-based analysis
    ooi_analysis = False

    # import ogd file if it already exists
    if ooi_analysis == True:
        # ask if ogd file exists
        ogd_exist = True

    # if action analysis, ask for actions
    if action_analysis == True:
        all_actions = ['Cap Off', 'Apply Tip', 'Setting Units', 'Priming', 'Injection', 'Remove Tip', 'Cap On']


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
trials_only = []
trial_paths = []
participants = []
participant_paths = []
group_paths = []
output_path_groups = []

i=0

for i in range (len(group_names)):

    group_paths.append(input_path / Path(group_names[i]))
    output_path_groups.append(output_path / Path(group_names[i]))

    # copy group folder structure to output 
    os.makedirs(output_path / Path(group_names[i]), exist_ok=True)
    
    # take all files from tobii input (to get one name per trial)
    filepaths = glob(join(group_paths[i],'*_tobii.tsv'))
    filenames =  [os.path.basename(filenames) for filenames in filepaths]
    
    # save all participants (participants[0] for group 1 and participants[1] for group 2)
    participant_paths.insert(i,[Path(filepath[:-18]) for filepath in filepaths]) # -18 to get participantxx
    participant_paths[i] = set(participant_paths[i]) # remove duplicates
    participant_paths[i] = list(participant_paths[i])
    participants.insert(i,[os.path.basename(participant) for participant in participant_paths[i]])

    # iterate through participants to save trial paths per participants
    trials.append([])
    trials_only.append([])
    trial_paths.append([])
    j=0
    for j in range(len(participants[i])):

        # create ouput folder for participant[i][j]
        os.makedirs(output_path / Path(group_names[i]) / Path(participants[i][j]), exist_ok=True)
        
        # list all trials of participant[i][j]
        trial_path_list = []
        for file in filepaths:
            if '{}'.format(participants[i][j]) in file:
                trial_name = file[:-10] # to get trialname only
                trial_path_list.append(trial_name)
                #trial_paths[i][j] = [file]
        trials_list = [os.path.basename(trial) for trial in trial_path_list]
        trials_only_list = [trial[14:] for trial in trials_list]
        
        # create ouput folder for each trial
        [os.makedirs(output_path / Path(group_names[i]) / Path(participants[i][j]) / trial, exist_ok = True) for trial in trials_list]

        # add to trial list
        trials[i].insert(j,trials_list)
        # add to trials_only list
        trials_only[i].insert(j, trials_only_list)
        # add to trial_paths list
        trial_paths[i].insert(j,trial_path_list) # for some reason adds a new empty element



#endregion


# _____________ GENERAL ANALYSIS (not OOI and not action based) 
#region

if general_analysis == True:

    # to save data for plots & summary dfs
    allgroups_list_dfs = []

    # iterate through groups
    for i in range(len(group_names)):


        # to save data for plots & summary dfs
        group_list_dfs = []


        

        # iterate through participants
        for j in range(len(participants[i])):


            # to save data for plots & summary dfs
            pp_sac_dur_list = []
            pp_fix_dur_list = []
            participant_list_dfs = []

            # iterate through each trial
            k=0
            for trial_path in trial_paths[i][j]:
                
                tobiipath = trial_path + '_tobii.tsv' 

                # transform tobii into (not)cgom file 
                tobii_to_fixations.reformat(tobiipath, trial_path) # new: saved as _fixations.txt (not _cgom.txt anymore)
                
                # read newly created fixation file 
                fixationdata = pd.read_csv(trial_path + '_fixations.txt', sep='\t')

                # transform tobii into saccade file
                tobii_to_saccades.reformat(tobiipath, trial_path)
                
                # read saccade data
                saccadedata = pd.read_csv(trial_path + '_saccades.txt', sep='\t')

                # calculations of general metrics with fixationdata & saccadedata
                df_general_metrics = general_metrics.calculate_general_metrics(fixationdata, saccadedata,trials[i][j][k])

                # define trial output path
                trial_output_path = output_path / Path(group_names[i]) / Path(participants[i][j] / Path(trials[i][j][k]))

                # create folder for general analysis in trial folder
                os.makedirs(trial_output_path / Path('general_analysis'), exist_ok = True)

                # define final output path
                analysispath = trial_output_path / Path('general_analysis')

                # save to folder
                df_general_metrics.to_csv(analysispath / '{}_general_analysis.csv'.format(trials[i][j][k]))

                # add df to summary list per participant
                participant_list_dfs.append(df_general_metrics)  

                # save data for boxplots (average fixation and saccade duration)
                # append saccade duration to list
                pp_sac_dur_list.append(saccadedata['Event Duration [ms]'].to_list())
                # append fixation duration to list
                pp_fix_dur_list.append(fixationdata['Event Duration [ms]'].to_list())
           
                k=k+1

        
            ### summary of general analysis per participant

            # create path for general analysis in participant folder
            os.makedirs(output_path_groups[i] / Path(participants[i][j]) / Path('general_analysis'), exist_ok = True)
            save_path = output_path_groups[i] / Path(participants[i][j]) / Path('general_analysis')

            # create summary df of all trials per participant and save to created dir
            pp_df_summary = summary_calculations.summary_general_analysis(participant_list_dfs, participants[i][j], save_path, 'Whole Trial')

            # extract average row from pp_df_summary and append to group_list_df
            pp_df_average = pp_df_summary.iloc[[-2]]
            group_list_dfs.append(pp_df_average)
            
            ### visualisations per participant

            vis_path = save_path / Path('visualisation')
            os.makedirs(vis_path, exist_ok=True)
            
            # boxplots for avg fixation and saccade duration
            # add a list of trial means to list
            pp_sac_dur_list.append([statistics.mean(pp_sac_dur_list[i]) for i in range(len(pp_sac_dur_list))])
            pp_fix_dur_list.append([statistics.mean(pp_fix_dur_list[i]) for i in range(len(pp_fix_dur_list))])
            # add mean to labels
            x_labels = trials[i][j] + ['Mean {}'.format(participants[i][j])]
            # get boxplots
            visualisations.vis_gen_metrics_boxplots_trials(pp_sac_dur_list, pp_fix_dur_list, vis_path , participants[i][j], 'Whole Trial', x_labels)

            # barplots from summary df
            visualisations.vis_gen_metrics_barplots(pp_df_summary, vis_path , participants[i][j], 'Whole Trial')

            # piechart relative sacc/fix duration
            visualisations.vis_gen_metrics_piechart(pp_df_summary, vis_path, group_names[i], 'Whole Trial')


            # if first participant
            if j == 0:
                group_boxplot_df = pd.DataFrame(columns=pp_df_summary.columns[:-1])
                group_boxplot_df.loc[0] =  np.empty((len(group_boxplot_df.columns), 0)).tolist()  
            # add row of empty list for new participant
         
            for metric in group_boxplot_df.columns:
                # add a list to list 
                inner_list = []
                for x in range(len(trials[i][j])):
                    inner_list.append(pp_df_summary[metric][x])
                group_boxplot_df[metric][0].append(inner_list)


            


            #pp_df_means = pp_df_summary.iloc[:-2,:-1] # -2 to only get the trial means and -1 to leave out relative fix/sac duration
            #group_boxplot_df = pd.concat([group_boxplot_df, pp_df_means])  

    
        ### summary of general analysis per group

        # create path for general analysis in group folder
        os.makedirs(output_path_groups[i] / Path('general_analysis'), exist_ok=True)
        save_path = output_path_groups[i] / Path('general_analysis')
        
        # create summary df of all participants per group and save to created dir
        group_df_summary = summary_calculations.summary_general_analysis(group_list_dfs, group_names[i], save_path, 'Whole Trial')

        # add df to summary list for all groups
        # extract average row from pp_df_summary and append to group_list_df
        group_df_average = group_df_summary.iloc[[-2]]
        allgroups_list_dfs.append(group_df_average)

        ### visualisations per group
        vis_path = save_path / Path('visualisation')
        os.makedirs(vis_path, exist_ok=True)



        # boxplots
        # (for allgroups_boxplot_df) if first group: make df with one empty column to fill 
        if i == 0:
            allgroups_boxplot_df = pd.DataFrame(columns=group_df_summary.columns[:-1])
            allgroups_boxplot_df.loc[0] =  np.empty((len(allgroups_boxplot_df.columns), 0)).tolist()  
        
        # define x labels
        x_labels = participants[i] + ['Mean {}'.format(group_names[i])]

        for metric in group_boxplot_df.columns:
            group_nested_list = group_boxplot_df[metric][0]
            list_means = [statistics.mean(group_nested_list[x]) for x in range(len(group_nested_list))]
            group_nested_list.append(list_means)
            visualisations.vis_gen_metrics_boxplots_group(group_nested_list, vis_path, group_names[i], 'Whole Trial', metric, x_labels)

            # append to boxplot_allgroups_df 
            inner_list = []
            for x in range(len(participants[i])):
                inner_list.append(group_df_summary[metric][x])
            allgroups_boxplot_df[metric][0].append(inner_list)



        # barplots
        visualisations.vis_gen_metrics_barplots(group_df_summary, vis_path , group_names[i], 'Whole Trial')

        # piechart
        visualisations.vis_gen_metrics_piechart(group_df_summary, vis_path, group_names[i], 'Whole Trial')

    ### summary of general analysis of all groups

    # create path for general analysis in group folder
    os.makedirs(output_path / Path('general_analysis'), exist_ok=True)
    save_path = output_path / Path('general_analysis')

    # create summary df of all groups and save to created df
    allgroups_df_summary = summary_calculations.summary_general_analysis(allgroups_list_dfs, 'All Groups', save_path, 'Whole Trial')

    # visualisations per group
    vis_path = save_path / Path('visualisation')
    os.makedirs(vis_path, exist_ok=True)
    x_labels = group_names + ['Mean All Groups']

    # boxplots
    for metric in allgroups_boxplot_df.columns:
        allgroups_nested_list = allgroups_boxplot_df[metric][0]
        list_means = [statistics.mean(allgroups_nested_list[x]) for x in range(len(allgroups_nested_list))]
        allgroups_nested_list.append(list_means)
        visualisations.vis_gen_metrics_boxplots_group(allgroups_nested_list, vis_path, 'All Groups', 'Whole Trial', metric, x_labels)


    # barplots
    visualisations.vis_gen_metrics_barplots(allgroups_df_summary, vis_path , 'All Groups', 'Whole Trial')


    # piecharts
    visualisations.vis_gen_metrics_piechart(allgroups_df_summary, vis_path, 'All Groups', 'Whole Trial')



    #visualisations.vis_gen_metrics(allgroups_df_summary, allgroups_sac_dur_list, allgroups_fix_dur_list, vis_path , 'All Groups', 'Whole Trial', x_labels)

e=3
#endregion


# _____________ K-COEFFICIENT ANALYSIS 
#region

if kcoeff_analysis == True:

    fixation_durations = []
    saccade_amplitudes = []

    # iterate through groups    
    for i in range(len(group_names)):
        
        # iterate through participants
        for j in range(len(participants[i])):

            # iterate through each trial
            k=0
            for trial_path in trial_paths[i][j]:
                
                kcoeff_path = trial_path + '_tobii_kcoeff.tsv'

                # filter for whole fixations and saccades 
                kcoefficient_analysis.reformat(kcoeff_path, trial_path)
                
                # read newly created kcoeff file 
                kcoeff_data = pd.read_csv(trial_path + '_kcoeff.txt', sep='\t')

                # add all fixation durations to list (over all trials of all participants of all groups)
                fixation_durations = fixation_durations + kcoeff_data[kcoeff_data['event_type']=='Fixation']['duration'].to_list()

                # add all saccade amplitudes to list (over all trials of all participants of all groups)
                saccade_amplitudes = saccade_amplitudes + kcoeff_data[kcoeff_data['event_type']=='Saccade']['saccade_amplitude'].to_list()
                #remove nans (in case of partial fixations)
                saccade_amplitudes = [item for item in saccade_amplitudes if not(math.isnan(item)) == True]
 

    # calculate mean and standard deviation of fixation duration and saccade amplitude of all trials (of both groups)
    mean_fix_dur = statistics.mean(fixation_durations)
    stdv_fix_dur = statistics.pstdev(fixation_durations)
    mean_sac_amp = statistics.mean(saccade_amplitudes)
    stdv_sac_amp = statistics.pstdev(saccade_amplitudes)

    # now, iterate again through trials to calculate k-coefficient per fixation and save in df
   
    summary_df_kcoeff = pd.DataFrame(index = trials[i])
    df_kcoeff_participant_list = []

    # iterate through groups
    for i in range(len(group_names)):


        df_kcoeff_group = pd.DataFrame() 
        # iterate through participants
        for j in range(len(participants[i])):

            participant_list = []
            # iterate through each trial
            k=0
            for trial_path in trial_paths[i][j]:
                kcoeff_data = pd.read_csv(trial_path + '_kcoeff.txt', sep='\t')

                # fill list in length of df with K-coefficient at every fixation                
                kcoeff_column = []
                for row in range(len(kcoeff_data)):
                    # calculate K-coefficient for all fixations and subsequent saccades
                    if kcoeff_data['event_type'][row] == 'Fixation':
                            # if fixation is in last row, append np.nan
                            if row == (len(kcoeff_data)-1):
                                kcoeff_column.append(np.nan)
                            # if there is no saccade after the fixation, append np.nan
                            elif kcoeff_data['event_type'][row+1] != 'Saccade':
                                kcoeff_column.append(np.nan)
                            else:
                                fixdur = kcoeff_data['duration'][row] 
                                sacamp = kcoeff_data['saccade_amplitude'][row+1]
                                z_score_fix = (fixdur - mean_fix_dur) / stdv_fix_dur
                                z_score_amp = (sacamp - mean_sac_amp) / stdv_sac_amp
                                kcoeff_row = z_score_fix - z_score_amp
                                kcoeff_column.append(kcoeff_row)
                    else:
                        kcoeff_column.append(np.nan)
                
                kcoeff_data['K-coefficient'] = kcoeff_column

                # take two columns to create new dataframe
                df_kcoeff = kcoeff_data[['K-coefficient', 'start_time']]
                
                # remove rows where K-coefficient is np.nan
                df_kcoeff.dropna(inplace=True)

                # define trial output path
                trial_output_path = output_path / Path(group_names[i]) / Path(participants[i][j] / Path(trials[i][j][k]))

                # create folder for kcoefficient analysis in trial folder and save there
                os.makedirs(trial_output_path / Path('k-coefficient_analysis'), exist_ok = True)
                analysispath = trial_output_path / Path('k-coefficient_analysis')
                df_kcoeff.to_csv(analysispath / '{}_k-coefficient_analysis.csv'.format(trials[i][j][k]))
                
                # calculate average k-coefficient of entire trial and append to list per participant
                participant_list.append(statistics.mean(df_kcoeff['K-coefficient']))
         
                # visualise k-coefficient 
                os.makedirs(analysispath / Path('visualisations'), exist_ok=True)
                vis_path = analysispath / 'visualisations'
                spec = 'Whole Trial'
                visualisations.vis_kcoeff(df_kcoeff, vis_path, trials[i][j][k], spec)
                
                k=k+1

            # for each participant, add one column with avg Kcoeff per trial as rows
            col_header = participants[i][j]
            df_kcoeff_group[col_header] = participant_list
            e=2


        indeces_group_kcoeff = ['trial0{}'.format(number+1) for number in range(len(df_kcoeff_group))]
        df_kcoeff_group.index = indeces_group_kcoeff
        df_kcoeff_group.to_csv(output_path_groups[i] / 'K-Coefficient Group Summary.csv' )
        e=2 

#endregion


# _____________ OOI-BASED ANALYSIS
#region

if ooi_analysis == True:

    # prepare data

    # if ogd files do not exist yet, create them
    if ogd_exist == False:
        # run the same as in suchitas GUI 
        # let user add labels & weights
        # run make_gaze_OGD 
        # and safe new files to trial path (similar to above)
        # give them the name: participant01_trial03_ogd.txt
        a=1

    allgroups_list_dfs_ooi = []
    allgroups_list_dfs_ooigen = []
    # iterate through groups
    for i in range(len(group_names)):

        group_list_dfs_ooi = []
        group_list_dfs_ooigen = []
        # iterate through participants
        for j in range(len(participants[i])):

            participant_list_dfs_ooi = []
            participant_list_dfs_ooigen = []
            # iterate through each trial
            k=0
            for trial_path in trial_paths[i][j]:

                ogd_data = pd.read_csv(trial_path + '_ogd.txt', sep='\t')

                # extract all OOIs
                all_ooi = ooi_metrics.extract_oois(ogd_data)

                # preprocess ogd data and add columns (fixation object and fixation time)
                ogd_final = ooi_metrics.prepare_ogd_file(ogd_data, pixel_distance)

                ### prepare output folders

                # define trial output path
                trial_output_path = output_path / Path(group_names[i]) / Path(participants[i][j] / Path(trials[i][j][k]))

                # create folder for ooi analysis in trial folder
                os.makedirs(trial_output_path / Path('ooi_analysis'), exist_ok = True)

                # define final output path
                analysispath = trial_output_path / Path('ooi_analysis')

                # create folder for visualisations
                os.makedirs(analysispath / Path('visualisations'), exist_ok=True)
                vis_path = analysispath / Path('visualisations')


                ### calculate all ooi metrics
                df_ooi_metrics = ooi_metrics.calculate_ooi_metrics(ogd_final, all_ooi)
                # save ooi metrics
                df_ooi_metrics.to_csv(analysispath / '{}_ooi_analysis.csv'.format(trials[i][j][k]))
                # visualisations of ooi metrics
                spec = 'Whole Trial'   # add this to title in figure (will be respective actin for action plots)
                visualisations.vis_ooi_metrics(df_ooi_metrics, vis_path, trials[i][j][k], spec)
                # append to list of dfs per participant
                participant_list_dfs_ooi.append(df_ooi_metrics)


                ### calculate all ooi-based general metrics
                df_general_ooi_metrics, transition_matrix,dict_ooi = ooi_metrics.calculate_general_ooi_metrics(ogd_final, all_ooi, trials[i][j][k])
                # save ooi-based general metrics
                df_general_ooi_metrics.to_csv(analysispath / '{}_ooi-based_general_analysis.csv'.format(trials[i][j][k]))
                # visualisation of transition matrix
                spec = 'Whole Trial'
                visualisations.vis_transition_matrix(transition_matrix, dict_ooi, vis_path, trials[i][j][k], spec)
                # append to list of dfs per participant
                participant_list_dfs_ooigen.append(df_general_ooi_metrics)


                k=k+1


            ### summary of ooi analysis per participant

            # create path for ooi analysis in participant folder
            os.makedirs(output_path_groups[i] / Path(participants[i][j]) / Path('ooi_analysis'), exist_ok = True)
            save_path = output_path_groups[i] / Path(participants[i][j]) / Path('ooi_analysis')

            # create summary df of all trials per participant and save to created dir
            participant_df_summary_ooi, participant_df_means_ooi = summary_calculations.summary_ooi_analysis(participant_list_dfs_ooi, participants[i][j], save_path, 'Whole Trial')

            # append mean_df to group_list_df
            group_list_dfs_ooi.append(participant_df_means_ooi)        
            
            # visualisations per participant
            e=3


            ### summary of ooi-based general analysis per participant

            # create summary df of all trials per participant and save to created dir
            participant_df_summary_ooigen = summary_calculations.summary_ooigen_analysis(participant_list_dfs_ooigen, participants[i][j], save_path, 'Whole Trial')

            # extract average row from pp_df_summary and append to group_list_df
            pp_df_average = participant_df_summary_ooigen.iloc[[-2]]
            group_list_dfs_ooigen.append(pp_df_average)  




        ### summary of ooi analysis per group

        # create path for general analysis in group folder
        os.makedirs(output_path_groups[i] / Path('ooi_analysis'), exist_ok=True)
        save_path = output_path_groups[i] / Path('ooi_analysis')
        
        # create summary df of all participants per group and save to created dir
        group_df_summary_ooi, group_df_means_ooi = summary_calculations.summary_ooi_analysis(group_list_dfs_ooi, group_names[i], save_path, 'Whole Trial')

        # add df to summary list of all groups
        allgroups_list_dfs_ooi.append(group_df_means_ooi)     

        # visualisations per group
        e=4



        ### summary of ooi-based general analysis per group

        # create summary df of all participants per group and save 
        group_df_summary_ooigen = summary_calculations.summary_ooigen_analysis(group_list_dfs_ooigen, group_names[i], save_path, 'Whole Trial')

        # extract means and add df to summary list of all groups
        group_df_average = group_df_summary_ooigen.iloc[[-2]]
        allgroups_list_dfs_ooigen.append(group_df_average)

        # visualisations per group



    ### summary of ooi analysis of all groups

    # create directory
    os.makedirs(output_path / Path('ooi_analysis'), exist_ok=True)
    save_path = output_path / Path('ooi_analysis')

    # create summary df of all participants per group and save to created dir
    allgroups_df_summary_ooi, allgroups_df_means_ooi = summary_calculations.summary_ooi_analysis(allgroups_list_dfs_ooi, 'All Groups', save_path, 'Whole Trial')



    ### summary of ooi-based general analysis of all groups
    allgroups_df_summary_ooigen = summary_calculations.summary_ooigen_analysis(allgroups_list_dfs_ooigen, 'All Groups', save_path, 'Whole Trial')

    # visualise
    e=2


#endregion


# _____________ ACTION-BASED ANALYSIS
#region

# only if specified to so do
if action_analysis == True:

    # create a df that stores all general/ooi/ooi-based general analysis summary dfs per action of all groups
    df_allgroups_gen_action_dfs = pd.DataFrame(columns=all_actions)
    df_allgroups_ooi_action_dfs = pd.DataFrame(columns=all_actions)
    df_allgroups_ooigen_action_dfs = pd.DataFrame(columns=all_actions)

    # iterate though groups
    for i in range(len(group_names)):


        # create a df that stores all summary dfs per action of one group
        df_group_gen_action_dfs = pd.DataFrame(columns=all_actions)
        df_group_ooi_action_dfs = pd.DataFrame(columns=all_actions)
        df_group_ooigen_action_dfs = pd.DataFrame(columns=all_actions)

        # add row of empty lists for participant to group summary dfs (why list: dfs can only be stored in other dfs in a list)
        df_allgroups_gen_action_dfs.loc['{}'.format(group_names[i])] =  np.empty((len(all_actions), 0)).tolist()           
        df_allgroups_ooi_action_dfs.loc['{}'.format(group_names[i])] =  np.empty((len(all_actions), 0)).tolist()
        df_allgroups_ooigen_action_dfs.loc['{}'.format(group_names[i])] =  np.empty((len(all_actions), 0)).tolist()

        
        # iterate through participants
        for j in range(len(participants[i])):

            # create a df that stores all summary dfs per action of one participant
            df_pp_gen_action_dfs = pd.DataFrame(columns=all_actions)
            df_pp_ooi_action_dfs = pd.DataFrame(columns=all_actions)
            df_pp_ooigen_action_dfs = pd.DataFrame(columns=all_actions)

        
            # add row of empty lists for participant to group summary df (why list: dfs can only be stored in other dfs in a list)
            df_group_gen_action_dfs.loc['{}'.format(participants[i][j])] =  np.empty((len(all_actions), 0)).tolist()
            df_group_ooi_action_dfs.loc['{}'.format(participants[i][j])] =  np.empty((len(all_actions), 0)).tolist()
            df_group_ooigen_action_dfs.loc['{}'.format(participants[i][j])] =  np.empty((len(all_actions), 0)).tolist()

        
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

                # extract actions -> new: defined in the beginning, since not all actions may occur in all trials
                #all_actions = ogd_final['action'].unique().tolist()
               
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


                # add row of empty lists for trial to participant summary df 
                df_pp_gen_action_dfs.loc['{}'.format(trials[i][j][k])] =  np.empty((len(all_actions), 0)).tolist()
                df_pp_ooi_action_dfs.loc['{}'.format(trials[i][j][k])] =  np.empty((len(all_actions), 0)).tolist()
                df_pp_ooigen_action_dfs.loc['{}'.format(trials[i][j][k])] =  np.empty((len(all_actions), 0)).tolist()


                # combine all dfs to one summary df per action
                for action in all_actions:

                    # extract indeces of the current action in the action_sequence (from df_actions)
                    idx_action_dfs = [ind for ind, ele in enumerate(action_sequence) if ele == action]

                    # output path to save dfs
                    trial_output_path = output_path / Path(group_names[i]) / Path(participants[i][j]) / Path(trials[i][j][k])

                    
                    ### summary of general metrics

                    # get summary of general metrics per action
                    df_summary_gen = action_separation.summary_general_metrics_per_action(general_metrics_action_df_list, idx_action_dfs)

                    # save output per action: general metrics
                    analysispath = trial_output_path / Path('general_analysis')
                    os.makedirs(analysispath, exist_ok=True)
                    df_summary_gen.to_csv(analysispath / '{}_general_analysis_{}.csv'.format(trials[i][j][k], action))

                    # add df to summary df per participant
                    df_pp_gen_action_dfs[action][k].append(df_summary_gen)
                    # how to access the saved df: df_pp_gen_action_dfs[action][k][0]
                    # because df is stored in a list     


                    ### summary of ooi metrics


                    # get summary of ooi-based ooi metrics per action
                    df_summary_ooi = action_separation.summary_ooi_metrics_per_action(ooi_metrics_action_df_list, idx_action_dfs)

                    # save output per action: ooi-based ooi metrics
                    analysispath = trial_output_path / Path('ooi_analysis')
                    os.makedirs(analysispath, exist_ok=True)
                    df_summary_ooi.to_csv(analysispath / '{}_ooi_analysis_{}.csv'.format(trials[i][j][k], action))

                    # add df to summary df per participant
                    df_pp_ooi_action_dfs[action][k].append(df_summary_ooi)

                    # visualisations of ooi metrics per action
                    vis_path = analysispath / Path('visualisations')
                    spec = action   # add this to title in figure and file name
                    visualisations.vis_ooi_metrics(df_summary_ooi, vis_path, trials[i][j][k], spec)



                    # get summary of ooi-based general metrics per action
                    df_summary_ooigen = action_separation.summary_ooi_general_metrics_per_action(gen_ooi_metrics_action_df_list, idx_action_dfs, df_summary_ooi, general_metrics_action_df_list)

                    # add df to summary df per participant
                    df_pp_ooigen_action_dfs[action][k].append(df_summary_ooigen)


                    # save output per action: ooi-based general metrics
                    df_summary_ooigen.to_csv(analysispath / '{}_ooi-based_general_analysis_{}.csv'.format(trials[i][j][k], action))

                    # visualisations of transition_matrix per action
                    # for each step!


                print(i,j,k)            
                k=k+1
            


            ### summary per participant

            ## general metrics

            # create directory and define output path
            save_path = output_path / Path(group_names[i]) / Path(participants[i][j]) / Path('general_analysis')
            os.makedirs(save_path, exist_ok= True)
            
            for action in all_actions:
                df_pp_action_list = [df_pp_gen_action_dfs[action][x][0] for x in range(len(df_pp_gen_action_dfs))]
                df_summary_pp_action = summary_calculations.summary_general_analysis(df_pp_action_list, participants[i][j], save_path, action)

                # extract row with means per pp (second last row) and append to group summary df
                pp_df_average = df_summary_pp_action.iloc[[-2]]
                df_group_gen_action_dfs[action][j].append(pp_df_average)
                e=3


            ## ooi metrics

            # create directory and define output path of csv file
            save_path = output_path / Path(group_names[i]) / Path(participants[i][j]) / Path('ooi_analysis')
            os.makedirs(save_path, exist_ok = True)

            # create directory and define output path of visualisations
            vis_path = save_path / Path('visualisations')
            os.makedirs(vis_path, exist_ok = True)
            
            for action in all_actions:
                df_pp_action_list = [df_pp_ooi_action_dfs[action][x][0] for x in range(len(df_pp_ooi_action_dfs))]
                df_summary_pp_action, df_summary_pp_action_means = summary_calculations.summary_ooi_analysis(df_pp_action_list, participants[i][j], save_path, action)

                # append means df to group summary df    
                df_group_ooi_action_dfs[action][j].append(df_summary_pp_action_means) 

                # visualisation of mean values of one participant
                visualisations.vis_ooi_metrics(df_summary_pp_action_means, vis_path, participants[i][j], action) 

            
            ## ooi-based general metrics
            
            for action in all_actions:
                df_pp_action_list = [df_pp_ooigen_action_dfs[action][x][0] for x in range(len(df_pp_ooigen_action_dfs))]
                df_summary_pp_action = summary_calculations.summary_ooigen_analysis(df_pp_action_list, participants[i][j], save_path, action)

                # extract row with means per pp (second last row) and append to group summary df
                pp_df_average = df_summary_pp_action.iloc[[-2]]
                df_group_ooigen_action_dfs[action][j].append(pp_df_average)
        
                            



        ### summary per group

        ## general analysis

        # create directory and define output path
        save_path = output_path / Path(group_names[i]) / Path('general_analysis')
        os.makedirs(save_path, exist_ok= True)

        for action in all_actions:
            df_group_action_list = [df_group_gen_action_dfs[action][x][0] for x in range(len(df_group_gen_action_dfs))]
            df_summary_group_action = summary_calculations.summary_general_analysis(df_group_action_list, group_names[i], save_path, action)

            # extract row with means (second last) per pp and append to group summary df
            group_df_average = df_summary_group_action.iloc[[-2]]
            df_allgroups_gen_action_dfs[action][i].append(group_df_average)

        
        ## ooi analysis

        # create directory and define output path
        save_path = output_path / Path(group_names[i]) / Path('ooi_analysis')
        os.makedirs(save_path, exist_ok= True)

        # create directory and define output path of visualisations
        vis_path = save_path / Path('visualisations')
        os.makedirs(vis_path, exist_ok = True)
            
        
        for action in all_actions:
            df_group_action_list = [df_group_ooi_action_dfs[action][x][0] for x in range(len(df_group_ooi_action_dfs))]
            df_summary_group_action, df_summary_group_action_means = summary_calculations.summary_ooi_analysis(df_group_action_list, group_names[i], save_path, action)

            # append means df to group summary df    
            df_allgroups_ooi_action_dfs[action][i].append(df_summary_group_action_means)  

            # visualisation of mean values of one group
            visualisations.vis_ooi_metrics(df_summary_group_action_means, vis_path, group_names[i], action) 

        
        ## ooi-based general metrics
        
        for action in all_actions:
            df_group_action_list = [df_group_ooigen_action_dfs[action][x][0] for x in range(len(df_group_ooigen_action_dfs))]
            df_summary_group_action = summary_calculations.summary_ooigen_analysis(df_group_action_list,group_names[i], save_path, action)

            # extract row with means per pp (second last row) and append to group summary df
            group_df_average = df_summary_group_action.iloc[[-2]]
            df_allgroups_ooigen_action_dfs[action][i].append(group_df_average)

    
    ### summary of all groups

    ## general analysis

    # create directory and define output path
    save_path = output_path / Path('general_analysis')
    os.makedirs(save_path, exist_ok= True)

    for action in all_actions:
        df_allgroups_action_list = [df_allgroups_gen_action_dfs[action][x][0] for x in range(len(df_allgroups_gen_action_dfs))]
        df_summary_allgroups_action = summary_calculations.summary_general_analysis(df_allgroups_action_list, 'All Groups', save_path, action)



    ## ooi analysis
    
    # create directory and define output path
    save_path = output_path / Path('ooi_analysis')
    os.makedirs(save_path, exist_ok= True)

    # create directory and define output path of visualisations
    vis_path = save_path / Path('visualisations')
    os.makedirs(vis_path, exist_ok = True)
    
    for action in all_actions:
        df_allgroups_action_list = [df_allgroups_ooi_action_dfs[action][x][0] for x in range(len(df_allgroups_ooi_action_dfs))]
        df_summary_allgroups_action, df_summary_allgroups_action_means = summary_calculations.summary_ooi_analysis(df_allgroups_action_list,'All Groups', save_path, action)
    

    # visualisation of mean values of all groups
    visualisations.vis_ooi_metrics(df_summary_allgroups_action_means, vis_path, 'All Groups', action) 

    ## ooi-based general analysis
    for action in all_actions:
        df_allgroups_action_list = [df_allgroups_ooigen_action_dfs[action][x][0] for x in range(len(df_allgroups_ooigen_action_dfs))]
        df_summary_allgroups_action = summary_calculations.summary_ooigen_analysis(df_allgroups_action_list,'All Groups', save_path, action)

e=3






    

#endregion






