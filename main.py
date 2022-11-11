# _____________ IMPORT
#region
from ntpath import join
import pandas as pd
import numpy as np
from glob import glob
from pathlib import Path
import statistics
import os
import math


# import own scripts
import ooi_metrics
import general_metrics
import tobii_to_fixations as t2f # change to "tobii_to_fixations_old" if you have the .tsv file from tobii data export (not metrics export!)
import tobii_to_saccades as t2s # change to "tobii_to_saccades_old" if you have the .tsv file from tobii data export (not metrics export!)
import action_separation
import kcoefficient_calculation
import visualisations
import sequence_comparisons
import result_summaries

#endregion


# _____________ VARIABLES FROM GUI (replacement for GUI at this stage)
# region

# replacing input from gui
def get_variables_gui():
    global ogd_exist, pixel_distance, input_path, output_path, action_analysis, ooi_analysis, general_analysis, kcoeff_analysis, all_actions, sequence_comp, opt_sequence, algrthm, run_stats, results_summary_report

    # choose input path (where group folders lie)
    ui_input_path =  'Data/study_analysis_part2' #test data: Data/gaze_input_tobii_ogd_kcoeff -> change to tobii_to_fixations_old.py and tobii_to_saccades_old.py in import & change kcoeff (tobii_kcoeff.tsv import)
    input_path = Path(ui_input_path)

    # (choose) output path (group folders will be created in there)
    ui_output_path = 'Output'
    output_path = Path(ui_output_path)

    # general analysis
    general_analysis = True

    # calculate k-coefficient
    kcoeff_analysis = True

    # action-based analysis (needs ooi-based analysis to be run first, because dirs are created, should be changed)
    action_analysis = True

    # ooi-based analysis
    ooi_analysis = True

    # sequence comparison
    sequence_comp = True

    # stats (entropy) (needs ooi-based analysis to be run first)
    run_stats = True

    # results
    results_summary_report = True
       

    # import ogd file if it already exists
    if ooi_analysis == True:
        # ask if ogd file exists
        ogd_exist = True

    # if action analysis, ask for actions
    if action_analysis == True:
        all_actions = ['Cap Off', 'Apply Tip', 'Setting Units', 'Priming', 'Injection', 'Remove Tip', 'Cap On']

    # if distance should be calculated between sequences, ask for optimal sequence
    if sequence_comp == True:
        opt_sequence =  ['Cap Off', 'Apply Tip', 'Setting Units', 'Priming', 'Setting Units', 'Injection', 'Remove Tip', 'Cap On']
        algrthm = 'levenshtein_distance' # to extend with other types of edit distance algorithm calculations




    # others
    pixel_distance = 20
    
get_variables_gui()


#endregion


# _____________ GET LIST & PATHS OF PARTICIPANTS AND TRIALS 
#region

# same folder structure for one group and multiple groups: input/groupname/data
groups = [f for f in sorted(os.listdir(input_path))] 

trials = []
trials_only = []
trial_paths = []
participants = []
participant_paths = []
group_paths = []
output_path_groups = []

i=0

for i in range (len(groups)):

    group_paths.append(input_path / Path(groups[i]))
    output_path_groups.append(output_path / Path(groups[i]))

    # copy group folder structure to output 
    os.makedirs(output_path / Path(groups[i]), exist_ok=True)
    
    # take all files from tobii input (to get one name per trial)
    filepaths = glob(join(group_paths[i],'*_tobii.tsv'))
    filenames =  [os.path.basename(filenames) for filenames in filepaths]
    
    # save all participants (participants[0] for group 1 and participants[1] for group 2)
    participant_paths.insert(i,[Path(filepath[:-18]) for filepath in filepaths]) # -18 to get participantxx
    participant_paths[i] = set(participant_paths[i]) # remove duplicates
    participant_paths[i] = list(participant_paths[i]) # convert to list
    participant_paths[i] = sorted(participant_paths[i]) # sort alphabetically
    participants.insert(i,[os.path.basename(participant) for participant in participant_paths[i]])
    participants[i] = sorted(participants[i]) # sort alphabetically

    # iterate through participants to save trial paths per participants
    trials.append([])
    trials_only.append([]) # not used yet, but could be useful later if trial number want to be compared to each other (e.g. all first trials vs. all third trials)
    trial_paths.append([])
    j=0
    for j in range(len(participants[i])):

        # create ouput folder for participant[i][j]
        os.makedirs(output_path / Path(groups[i]) / Path(participants[i][j]), exist_ok=True)
        
        # list all trials of participant[i][j]
        trial_path_list = []
        for file in filepaths:
            if '{}'.format(participants[i][j]) in file:
                trial_name = file[:-10] # to get trialname only
                trial_path_list.append(trial_name)
        trials_list = [os.path.basename(trial) for trial in trial_path_list]
        trials_only_list = [trial[14:] for trial in trials_list]
        
        # create ouput folder for each trial
        [os.makedirs(output_path / Path(groups[i]) / Path(participants[i][j]) / trial, exist_ok = True) for trial in trials_list]

        # add to trial list & sort alphabetically
        trials[i].insert(j,trials_list)
        trials[i][j] = sorted(trials[i][j])
        # add to trials_only list & sort alphabetically
        trials_only[i].insert(j, trials_only_list)
        trials_only[i][j] = sorted(trials_only[i][j])
        # add to trial_paths list
        trial_paths[i].insert(j,trial_path_list) 
        trial_paths[i][j] = sorted(trial_paths[i][j])

groups = sorted(groups) # sort groups alphabetically

#endregion


# _____________ GENERAL ANALYSIS (not OOI and not action based) 
#region

if general_analysis == True:

    # to save data for plots & summary dfs
    allgroups_list_dfs = []

    # iterate through groups
    for i in range(len(groups)):


        # to save data for plots & summary dfs
        group_list_dfs = []

       
        # iterate through participants
        for j in range(len(participants[i])):


            # to save data for plots & summary dfs
            pp_sac_dur_list = []
            pp_fix_dur_list = []
            participant_list_dfs = []

            # iterate through each trial
            for k in range(len(trials[i][j])):
                
                tobiipath = trial_paths[i][j][k] + '_tobii.tsv' 

                # transform tobii into (not)cgom file 
                t2f.reformat(tobiipath, trial_paths[i][j][k])
                
                # read newly created fixation file 
                fixationdata = pd.read_csv(trial_paths[i][j][k] + '_fixations.txt', sep='\t')

                # transform tobii into saccade file
                t2s.reformat(tobiipath, trial_paths[i][j][k])
                
                # read saccade data
                saccadedata = pd.read_csv(trial_paths[i][j][k] + '_saccades.txt', sep='\t')

                # calculations of general metrics with fixationdata & saccadedata
                df_general_metrics = general_metrics.calculate_general_metrics(fixationdata, saccadedata,trials[i][j][k])

                # define trial output path
                trial_output_path = output_path / Path(groups[i]) / Path(participants[i][j] / Path(trials[i][j][k]))

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


        
            ### summary of general analysis per participant

            # create path for general analysis in participant folder
            os.makedirs(output_path_groups[i] / Path(participants[i][j]) / Path('general_analysis'), exist_ok = True)
            save_path = output_path_groups[i] / Path(participants[i][j]) / Path('general_analysis')

            # create summary df of all trials per participant and save to created dir
            pp_df_summary = general_metrics.summary_general_analysis(participant_list_dfs, participants[i][j], save_path, 'Whole Trial')

            # extract average row from pp_df_summary and append to group_list_df
            pp_df_average = pp_df_summary.iloc[[-2]]
            group_list_dfs.append(pp_df_average)
            
            ### visualisations per participant

            vis_path = save_path / Path('visualisations')
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
            visualisations.vis_gen_metrics_piechart(pp_df_summary, vis_path, participants[i][j], 'Whole Trial')


            # for boxplots per group

            # if first participant
            if j == 0:
                group_boxplot_df = pd.DataFrame(columns=pp_df_summary.columns[:-1])
                group_boxplot_df.loc[0] =  np.empty((len(group_boxplot_df.columns), 0)).tolist()  

            for metric in group_boxplot_df.columns:
                # add a list to list 
                inner_list = []
                for x in range(len(trials[i][j])):
                    inner_list.append(pp_df_summary[metric][x])
                group_boxplot_df[metric][0].append(inner_list)

    
        ### summary of general analysis per group

        # create path for general analysis in group folder
        os.makedirs(output_path_groups[i] / Path('general_analysis'), exist_ok=True)
        save_path = output_path_groups[i] / Path('general_analysis')
        
        # create summary df of all participants per group and save to created dir
        group_df_summary = general_metrics.summary_general_analysis(group_list_dfs, groups[i], save_path, 'Whole Trial')

        # add df to summary list for all groups
        # extract average row from pp_df_summary and append to group_list_df
        group_df_average = group_df_summary.iloc[[-2]]
        allgroups_list_dfs.append(group_df_average)

        ### visualisations per group
        vis_path = save_path / Path('visualisations')
        os.makedirs(vis_path, exist_ok=True)


        # boxplots
        # (for allgroups_boxplot_df) if first group: make df with one empty column to fill 
        if i == 0:
            allgroups_boxplot_df = pd.DataFrame(columns=group_df_summary.columns[:-1])
            allgroups_boxplot_df.loc[0] =  np.empty((len(allgroups_boxplot_df.columns), 0)).tolist()  
        
        # define x labels
        x_labels = participants[i] + ['Mean {}'.format(groups[i])]

        for metric in group_boxplot_df.columns:
            group_nested_list = group_boxplot_df[metric][0]
            list_means = [statistics.mean(group_nested_list[x]) for x in range(len(group_nested_list))]
            group_nested_list.append(list_means)
            visualisations.vis_gen_metrics_boxplots_group(group_nested_list, vis_path, groups[i], 'Whole Trial', metric, x_labels)

            # append to boxplot_allgroups_df 
            inner_list = []
            for x in range(len(participants[i])):
                inner_list.append(group_df_summary[metric][x])
            allgroups_boxplot_df[metric][0].append(inner_list)



        # barplots
        visualisations.vis_gen_metrics_barplots(group_df_summary, vis_path , groups[i], 'Whole Trial')

        # piechart
        visualisations.vis_gen_metrics_piechart(group_df_summary, vis_path, groups[i], 'Whole Trial')


    ### summary of general analysis of all groups

    # create path for general analysis in group folder
    os.makedirs(output_path / Path('general_analysis'), exist_ok=True)
    save_path = output_path / Path('general_analysis')

    # create summary df of all groups and save to created df
    allgroups_df_summary = general_metrics.summary_general_analysis(allgroups_list_dfs, 'All Groups', save_path, 'Whole Trial')

    # visualisations per group
    vis_path = save_path / Path('visualisations')
    os.makedirs(vis_path, exist_ok=True)
    x_labels = groups + ['Mean All Groups']

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


e=3
#endregion


# _____________ K-COEFFICIENT ANALYSIS 
#region

if kcoeff_analysis == True:

    fixation_durations = []
    saccade_amplitudes = []

    # iterate through groups    
    for i in range(len(groups)):
        
        # iterate through participants
        for j in range(len(participants[i])):

            # iterate through each trial
            for k in range(len(trials[i][j])):
                
                kcoeff_path = trial_paths[i][j][k] + '_tobii.tsv' # change to '_tobii_kcoeff.tsv' if old tobii export is used

                # filter for whole fixations and saccades 
                kcoefficient_calculation.reformat(kcoeff_path, trial_paths[i][j][k])
                
                # read newly created kcoeff file 
                kcoeff_data = pd.read_csv(trial_paths[i][j][k] + '_kcoeff.txt', sep='\t')

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
    #summary_df_kcoeff = pd.DataFrame(index = trials[i])
    df_kcoeff_participant_list = []
    all_kcoeffs_list = []
    df_allgroups_kcoeff = pd.DataFrame(index=['All Groups'], columns = groups + ['Mean All Groups']) 

    # iterate through groups
    for i in range(len(groups)):

        df_group_kcoeff = pd.DataFrame(index=[groups[i]], columns = participants[i] + ['Mean {}'.format(groups[i])]) 

        # iterate through participants
        for j in range(len(participants[i])):

            
            df_pp_kcoeff = pd.DataFrame(columns = trials[i][j] + ['Mean {}'.format(participants[i][j])])
            df_list_kcoeff_lineplot = []
            pp_kcoeff_list = [] 

            # iterate through each trial
            for k in range(len(trials[i][j])):

                kcoeff_data = pd.read_csv(trial_paths[i][j][k] + '_kcoeff.txt', sep='\t')

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
                
                # remove rows where K-coefficient is np.nan and re-index
                df_kcoeff.dropna(inplace=True)
                df_kcoeff.reset_index(drop=True, inplace=True)

                # define trial output path
                trial_output_path = output_path / Path(groups[i]) / Path(participants[i][j] / Path(trials[i][j][k]))

                # create folder for kcoefficient analysis in trial folder and save there
                os.makedirs(trial_output_path / Path('k-coefficient_analysis'), exist_ok = True)
                analysispath = trial_output_path / Path('k-coefficient_analysis')
                df_kcoeff.to_csv(analysispath / '{}_k-coefficient_analysis.csv'.format(trials[i][j][k]))

                # append df to list of dfs of participant to get lineplots
                df_list_kcoeff_lineplot.append(df_kcoeff)
         
                # visualise k-coefficient 
                vis_path = output_path / Path(groups[i]) / Path(participants[i][j]) / Path(trials[i][j][k]) / Path('k-coefficient_analysis') / Path('visualisations')
                os.makedirs(vis_path, exist_ok=True)
                spec = 'Whole Trial'
                visualisations.vis_kcoeff_lineplot_trial(df_kcoeff, vis_path, trials[i][j][k], spec)
                                
                # calculate average k-coefficient of entire trial and append to list per participant
                pp_kcoeff_list.append(statistics.mean(df_kcoeff['K-coefficient']))
                # also add to list that saves all k-coefficents in one list to calculate mean and stdev over all trials
                all_kcoeffs_list.append(statistics.mean(df_kcoeff['K-coefficient']))



            ## pp summary 

            pp_kcoeff_mean = statistics.mean(pp_kcoeff_list)
            df_pp_kcoeff.loc[participants[i][j]] = pp_kcoeff_list + [pp_kcoeff_mean]
            # save and add focal/ambient and 2*stdev/not later after mean kcoeff is calculated
            analysispath =  output_path / Path(groups[i]) / Path(participants[i][j]) / Path('k-coefficient_analysis') 
            os.makedirs(analysispath, exist_ok = True)
            df_pp_kcoeff.to_csv(analysispath / '{} K-Coefficient Summary.csv'.format(participants[i][j]))


            # append mean to group summary
            df_group_kcoeff[participants[i][j]] = [df_pp_kcoeff.iloc[0,-1]]

            # visualisation 
            vis_path = analysispath / Path('visualisations')
            os.makedirs(vis_path, exist_ok = True)
            # lineplot per participant
            legends_lineplot = trials[i][j]
            spec = 'Whole Trial'
            visualisations.vis_kcoeff_lineplot_pp(df_list_kcoeff_lineplot, vis_path, participants[i][j], legends_lineplot, spec)



        ## group summary

        # calculate mean (yep, this complicated somehow)
        group_kcoeff_mean = df_group_kcoeff.astype(float).stack().dropna().mean()
        # add mean to last columns of the df
        df_group_kcoeff.iloc[0,-1] = group_kcoeff_mean
        # save and add focal/ambient and 2*stdev/not later after mean kcoeff is calculated
        analysispath =  output_path / Path(groups[i]) / Path('k-coefficient_analysis') 
        os.makedirs(analysispath, exist_ok = True)
        df_group_kcoeff.to_csv(analysispath / '{} K-Coefficient Summary.csv'.format(groups[i]))

        # append mean to all groups summary
        df_allgroups_kcoeff[groups[i]] = [df_group_kcoeff.iloc[0,-1]]
    
    ## all groups summary
    
    # calculate mean
    allgroups_kcoeff_mean = df_allgroups_kcoeff.astype(float).stack().dropna().mean()
    # add mean to last columns of the df
    df_allgroups_kcoeff.iloc[0,-1] = allgroups_kcoeff_mean
    # save and add focal/ambient and 2*stdev/not later after mean kcoeff is calculated
    analysispath =  output_path / Path('k-coefficient_analysis') 
    os.makedirs(analysispath, exist_ok = True)
    df_allgroups_kcoeff.to_csv(analysispath / 'All Groups K-Coefficient Summary.csv')



    # calculate overall mean kcoefficient and its std dev from list that collected all k-coefficients of each trial
    mean_kcoeff_all = statistics.mean(all_kcoeffs_list)
    stdev_kcoeff_all = statistics.stdev(all_kcoeffs_list)


    # append focal/ambient and outlier/not to dfs per allgroups, groups, participants
    
    # iterate through groups
    for i in range(len(groups)):
        # iterate through participants
        for j in range(len(participants[i])):

            # import pp summary 
            analysispath = output_path / Path(groups[i]) / Path(participants[i][j]) / Path('k-coefficient_analysis')
            df_pp_kcoeff_2 = pd.read_csv(analysispath / '{} K-Coefficient Summary.csv'.format(participants[i][j]), index_col=[0])

            # append rows 
            df_pp_kcoeff_2.loc['Outside 2x Stdev'] = 'No'
            df_pp_kcoeff_2.loc['Focal/Ambient'] =  'Ambient' 

            # iterate through each trial mean
            x=0
            for kcoeff in df_pp_kcoeff_2.iloc[0]:
                # check if any of the means are outside 2x standard deviation of overall mean and change to yes if the case
                if kcoeff > (mean_kcoeff_all + 2*stdev_kcoeff_all) or kcoeff < mean_kcoeff_all - 2*stdev_kcoeff_all:
                    df_pp_kcoeff_2.loc['Outside 2x Stdev'][x] = 'Yes'
                # change if mean is focal
                if kcoeff > 0:
                    df_pp_kcoeff_2.loc['Focal/Ambient'][x] = 'Focal'
                x=x+1
            # save again (and overwrite old file)
            df_pp_kcoeff_2.to_csv(analysispath / '{} K-Coefficient Summary.csv'.format(participants[i][j]))

            # visualisation
            vis_path = analysispath / Path('visualisations')
            visualisations.vis_kcoeff_barplot(df_pp_kcoeff_2,vis_path, participants[i][j], 'Whole Trial' )

        

        # import group summary 
        analysispath = output_path / Path(groups[i]) / Path('k-coefficient_analysis')
        df_group_kcoeff_2 = pd.read_csv(analysispath / '{} K-Coefficient Summary.csv'.format(groups[i]), index_col=[0])

        # append rows
        df_group_kcoeff_2.loc['Outside 2x Stdev'] = 'No'
        df_group_kcoeff_2.loc['Focal/Ambient'] = 'Ambient'

        # iterate through each participant mean
        x=0
        for kcoeff in df_group_kcoeff_2.iloc[0]:
            # check if any of the means are outside 2x standard deviation of overall mean and change to yes if the case
            if kcoeff > (mean_kcoeff_all + 2*stdev_kcoeff_all) or kcoeff < mean_kcoeff_all - 2*stdev_kcoeff_all:
                df_group_kcoeff_2.loc['Outside 2x Stdev'][x] = 'Yes'
            # change if mean is focal
            if kcoeff > 0:
                df_group_kcoeff_2.loc['Focal/Ambient'][x] = 'Focal'
            x=x+1
        # save again (and overwrite old file)
        df_group_kcoeff_2.to_csv(analysispath / '{} K-Coefficient Summary.csv'.format(groups[i]))

        # visualisation
        vis_path = analysispath / Path('visualisations')
        os.makedirs(vis_path, exist_ok=True)
        visualisations.vis_kcoeff_barplot(df_group_kcoeff_2,vis_path, groups[i], 'Whole Trial' )
    

    # import all groups summary
    analysispath = output_path / Path('k-coefficient_analysis')
    df_allgroups_kcoeff_2 = pd.read_csv(analysispath / 'All Groups K-Coefficient Summary.csv', index_col=[0])

    # append rows
    df_allgroups_kcoeff_2.loc['Outside 2x Stdev'] = 'No'
    df_allgroups_kcoeff_2.loc['Focal/Ambient'] = 'Ambient'

    # iterate through each participant mean
    x=0
    for kcoeff in df_allgroups_kcoeff_2.iloc[0]:
        # check if any of the means are outside 2x standard deviation of overall mean and change to yes if the case
        if kcoeff > (mean_kcoeff_all + 2*stdev_kcoeff_all) or kcoeff < mean_kcoeff_all - 2*stdev_kcoeff_all:
            df_allgroups_kcoeff_2.loc['Outside 2x Stdev'][x] = 'Yes'
        # change if mean is focal
        if kcoeff > 0:
            df_allgroups_kcoeff_2.loc['Focal/Ambient'][x] = 'Focal'
        x=x+1
    # save again (and overwrite old file)
    df_allgroups_kcoeff_2.to_csv(analysispath / 'All Groups K-Coefficient Summary.csv')

    # visualisation
    vis_path = analysispath / Path('visualisations')
    os.makedirs(vis_path, exist_ok=True)
    visualisations.vis_kcoeff_barplot(df_allgroups_kcoeff_2,vis_path, 'All Groups', 'Whole Trial' )


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

    allgroups_boxplot_list_df = []
    allgroups_boxplot_means_df = []
    
    allgroups_list_dfs_ooi = []
    allgroups_list_dfs_ooigen = []
    # iterate through groups
    for i in range(len(groups)):

        group_boxplot_list_df = []
        group_boxplot_means_df = []

        group_list_dfs_ooi = []
        group_list_dfs_ooigen = []
        # iterate through participants
        for j in range(len(participants[i])):

            participant_list_dfs_ooi = []
            participant_list_dfs_ooigen = []

            # iterate through each trial
            for k in range(len(trials[i][j])):

                ogd_data = pd.read_csv(trial_paths[i][j][k] + '_ogd.txt', sep='\t')

                # extract all OOIs
                all_ooi = ooi_metrics.extract_oois(ogd_data)

                # preprocess ogd data and add columns (fixation object and fixation time)
                ogd_final = ooi_metrics.prepare_ogd_file(ogd_data, pixel_distance)

                ### prepare output folders

                # define trial output path
                trial_output_path = output_path / Path(groups[i]) / Path(participants[i][j] / Path(trials[i][j][k]))

                # create folder for ooi analysis in trial folder
                os.makedirs(trial_output_path / Path('ooi_analysis'), exist_ok = True)

                # define final output path
                analysispath = trial_output_path / Path('ooi_analysis')

                # create folder for visualisations
                os.makedirs(analysispath / Path('visualisations'), exist_ok=True)
                vis_path = analysispath / Path('visualisations')


                ### calculate all ooi metrics per trial
                df_ooi_metrics = ooi_metrics.calculate_ooi_metrics(ogd_final, all_ooi)
                # save ooi metrics
                df_ooi_metrics.to_csv(analysispath / '{}_ooi_analysis.csv'.format(trials[i][j][k]))
                # append to list of dfs per participant
                participant_list_dfs_ooi.append(df_ooi_metrics)
                
                ### visualisations of ooi metrics per trial
                spec = 'Whole Trial'   # add this to title in figure (will be respective actin for action plots)
                visualisations.vis_ooi_metrics(df_ooi_metrics, vis_path, trials[i][j][k], spec)

                



                ### calculate all ooi-based general metrics per trial
                df_general_ooi_metrics, transition_matrix,dict_ooi = ooi_metrics.calculate_general_ooi_metrics(ogd_final, all_ooi, trials[i][j][k])
                # save ooi-based general metrics
                df_general_ooi_metrics.to_csv(analysispath / '{}_ooi-based_general_analysis.csv'.format(trials[i][j][k]))
                # append to list of dfs per participant
                participant_list_dfs_ooigen.append(df_general_ooi_metrics)

                ### visualisations of ooi-based general metrics per trial
                
                # visualisation of transition matrix
                spec = 'Whole Trial'
                visualisations.vis_transition_matrix(transition_matrix, dict_ooi, vis_path, trials[i][j][k], spec)

                # visualisation of ooi-based general metrics
                # boxplots of avg fixation duration and avg dwelltime (not priority)



            ### summary of ooi analysis per participant

            # create path for ooi analysis in participant folder
            os.makedirs(output_path_groups[i] / Path(participants[i][j]) / Path('ooi_analysis'), exist_ok = True)
            save_path = output_path_groups[i] / Path(participants[i][j]) / Path('ooi_analysis')
            # create summary df of all trials per participant and save to created dir
            participant_df_summary_ooi, participant_df_means_ooi = ooi_metrics.summary_ooi_analysis(participant_list_dfs_ooi, participants[i][j], save_path, 'Whole Trial')
            # append mean_df to group_list_df
            group_list_dfs_ooi.append(participant_df_means_ooi)        
            
            ### visualisations of ooi analysis per participant
            vis_path = save_path / Path('visualisations')
            os.makedirs(vis_path, exist_ok=True)

            # barplots and piechart (mean, without distribution)
            visualisations.vis_ooi_metrics(participant_df_means_ooi, vis_path, participants[i][j], 'Whole Trial')

            # collect for boxplots of next higher level
            
            # add first df (trial) to the df list
            df_list = participant_list_dfs_ooi[0].applymap(lambda x: [x])
            # add other trial dfs to group_boxplot_list_df[j]
            for l in range(1, len(participant_list_dfs_ooi)):
                df_list = df_list.add(participant_list_dfs_ooi[l].applymap(lambda x: [x]))
            group_boxplot_list_df.append(df_list)
            # collect means in one df
            group_boxplot_means_df.append(participant_df_means_ooi)



            ### summary of ooi-based general analysis per participant

            # create summary df of all trials per participant and save to created dir
            participant_df_summary_ooigen = ooi_metrics.summary_ooigen_analysis(participant_list_dfs_ooigen, participants[i][j], save_path, 'Whole Trial')
            # extract average row from pp_df_summary and append to group_list_df
            pp_df_average = participant_df_summary_ooigen.iloc[[-2]]
            group_list_dfs_ooigen.append(pp_df_average)  

            ### visualisations of ooi-based general analysis per participant

            # barplots
            visualisations.vis_ooigen_barplots(participant_df_summary_ooigen, vis_path, participants[i][j], 'Whole Trial')

            # collect for boxplots of next higher level

            # if first participant
            if j == 0:
                group_boxplot_df = pd.DataFrame(columns=participant_df_summary_ooigen.columns)
                group_boxplot_df.loc[0] =  np.empty((len(group_boxplot_df.columns), 0)).tolist()  
            
            for metric in group_boxplot_df.columns:
                # add a list to list 
                inner_list = []
                for x in range(len(trials[i][j])):
                    inner_list.append(participant_df_summary_ooigen[metric][x])
                group_boxplot_df[metric][0].append(inner_list)




        ### summary of ooi analysis per group

        # create path for general analysis in group folder
        os.makedirs(output_path_groups[i] / Path('ooi_analysis'), exist_ok=True)
        save_path = output_path_groups[i] / Path('ooi_analysis')    
        # create summary df of all participants per group and save to created dir
        group_df_summary_ooi, group_df_means_ooi = ooi_metrics.summary_ooi_analysis(group_list_dfs_ooi, groups[i], save_path, 'Whole Trial')
        # add df to summary list of all groups
        allgroups_list_dfs_ooi.append(group_df_means_ooi)     


        ### visualisations of ooi analysis per group
        vis_path = save_path / Path('visualisations')
        os.makedirs(vis_path, exist_ok = True)

        # barplots and piechart (mean, without distribution)
        visualisations.vis_ooi_metrics(group_df_means_ooi, vis_path, groups[i], 'Whole Trial')

        # boxplot
        x_labels = participants[i] + ['Mean {}'.format(groups[i])]
        # put elements in list, so that other lists can be appended -> nested lists for boxplot input
        df_nested_lists = group_boxplot_list_df[0].applymap(lambda x: [x])
        means_df = group_boxplot_means_df[0].applymap(lambda x: [x])
        # go through each participant df per group        
        for l in range(1,len(group_boxplot_list_df)):
            # add participant dfs to final df that will hold nested lists for boxplot
            df_to_add = group_boxplot_list_df[l].applymap(lambda x: [x])
            df_nested_lists = df_nested_lists.add(df_to_add)
            # add participant mean dfs to one df that will be added to final df
            df_to_add_means = group_boxplot_means_df[l].applymap(lambda x: [x])
            means_df =  means_df.add(df_to_add_means)
        # add means_df to final df 
        means_df = means_df.applymap(lambda x: [x])
        df_nested_lists = df_nested_lists.add(means_df)
        # loop through each metric to generate a boxplot with all oois and all participants
        for metric in df_nested_lists.index:
            nested_list_series = df_nested_lists.loc[metric]
            visualisations.vis_ooi_boxplots(nested_list_series, vis_path, groups[i], 'Whole Trial', metric, x_labels)
            e=2

        # fill dfs for next level
        # add first df (trial) to the df list
        df_list = group_list_dfs_ooi[0].applymap(lambda x: [x])
        # add other trial dfs to allgroups_boxplot_list_df[j]
        for l in range(1, len(group_list_dfs_ooi)):
            df_list = df_list.add(group_list_dfs_ooi[l].applymap(lambda x: [x]))
        allgroups_boxplot_list_df.append(df_list)
        # collect means in one df
        allgroups_boxplot_means_df.append(group_df_means_ooi)





        ### summary of ooi-based general analysis per group

        # create summary df of all participants per group and save 
        group_df_summary_ooigen = ooi_metrics.summary_ooigen_analysis(group_list_dfs_ooigen, groups[i], save_path, 'Whole Trial')

        # extract means and add df to summary list of all groups
        group_df_average = group_df_summary_ooigen.iloc[[-2]]
        allgroups_list_dfs_ooigen.append(group_df_average)

        ### visualisations per group
        
        # barplots
        visualisations.vis_ooigen_barplots(group_df_summary_ooigen, vis_path, groups[i], 'Whole Trial')

        # boxplots
        # (for allgroups_boxplot_df) if first group: make df with one empty column to fill 
        if i == 0:
            allgroups_boxplot_df = pd.DataFrame(columns=group_df_summary_ooigen.columns)
            allgroups_boxplot_df.loc[0] =  np.empty((len(allgroups_boxplot_df.columns), 0)).tolist()  
        
        # define x labels
        x_labels = participants[i] + ['Mean {}'.format(groups[i])]

        # iterate through metrics and make one figure per metric for all participants and the mean of one group
        for metric in group_boxplot_df.columns:
            group_nested_list = group_boxplot_df[metric][0]
            list_means = [statistics.mean(group_nested_list[x]) for x in range(len(group_nested_list))]
            group_nested_list.append(list_means)
            # maybe change to own function?
            visualisations.vis_gen_metrics_boxplots_group(group_nested_list, vis_path, groups[i], 'Whole Trial', metric, x_labels)

            # append to boxplot_allgroups_df 
            inner_list = []
            for x in range(len(participants[i])):
                inner_list.append(group_df_summary_ooigen[metric][x])
            allgroups_boxplot_df[metric][0].append(inner_list)



    ### summary of ooi analysis of all groups

    # create directory
    os.makedirs(output_path / Path('ooi_analysis'), exist_ok=True)
    save_path = output_path / Path('ooi_analysis')
    # create summary df of all participants per group and save to created dir
    allgroups_df_summary_ooi, allgroups_df_means_ooi = ooi_metrics.summary_ooi_analysis(allgroups_list_dfs_ooi, 'All Groups', save_path, 'Whole Trial')

    
    ### visualisations of ooi analysis of all groups
    vis_path = save_path / Path('visualisations')
    os.makedirs(vis_path, exist_ok = True)

    # barplots and piechart (mean, without distribution)
    visualisations.vis_ooi_metrics(allgroups_df_means_ooi, vis_path, 'All Groups', 'Whole Trial')

    # boxplots 
    x_labels = groups + ['Mean All Groups']
    # put elements in list, so that other lists can be appended -> nested lists for boxplot input
    df_nested_lists = allgroups_boxplot_list_df[0].applymap(lambda x: [x])
    means_df = allgroups_boxplot_means_df[0].applymap(lambda x: [x])
    # go through each group df        
    for l in range(1,len(allgroups_boxplot_list_df)):
        # add group dfs to final df that will hold nested lists for boxplot
        df_to_add = allgroups_boxplot_list_df[l].applymap(lambda x: [x])
        df_nested_lists = df_nested_lists.add(df_to_add)
        # add group mean dfs to one df that will be added to final df
        df_to_add_means = allgroups_boxplot_means_df[l].applymap(lambda x: [x])
        means_df =  means_df.add(df_to_add_means)
    # add means_df to final df 
    means_df = means_df.applymap(lambda x: [x])
    df_nested_lists = df_nested_lists.add(means_df)
    # loop through each metric to generate a boxplot with all oois and all groups
    for metric in df_nested_lists.index:
        nested_list_series = df_nested_lists.loc[metric]
        visualisations.vis_ooi_boxplots(nested_list_series, vis_path, 'All Groups', 'Whole Trial', metric, x_labels)
        e=2


    ### summary of ooi-based general analysis of all groups
    allgroups_df_summary_ooigen = ooi_metrics.summary_ooigen_analysis(allgroups_list_dfs_ooigen, 'All Groups', save_path, 'Whole Trial')

    # visualisations
    
    # barplots
    visualisations.vis_ooigen_barplots(allgroups_df_summary_ooigen, vis_path, 'All Groups', 'Whole Trial')

    # boxplots

    # define x labels
    x_labels = groups + ['Mean All Groups']

    # iterate through metrics and make one figure per metric for all participants and the mean of one group
    for metric in group_boxplot_df.columns:
        allgroups_nested_list = allgroups_boxplot_df[metric][0]
        list_means = [statistics.mean(allgroups_nested_list[x]) for x in range(len(allgroups_nested_list))]
        allgroups_nested_list.append(list_means)
        # maybe change to own function?
        visualisations.vis_gen_metrics_boxplots_group(allgroups_nested_list, vis_path, 'All Groups', 'Whole Trial', metric, x_labels)



#endregion


# _____________ ACTION-BASED ANALYSIS
#region

# only if specified to so do
if action_analysis == True:

    # create a df that stores all general/ooi/ooi-based general analysis summary dfs per action of all groups
    df_allgroups_gen_action_dfs = pd.DataFrame(columns=all_actions)
    df_allgroups_ooi_action_dfs = pd.DataFrame(columns=all_actions)
    df_allgroups_ooigen_action_dfs = pd.DataFrame(columns=all_actions)

    df_allgroups_kcoeff_per_action = pd.DataFrame(columns = all_actions)

    df_allgroups_duration_per_action = pd.DataFrame(columns = all_actions)

    # iterate though groups
    for i in range(len(groups)):


        # create a df that stores all summary dfs per action of one group
        df_group_gen_action_dfs = pd.DataFrame(columns=all_actions)
        df_group_ooi_action_dfs = pd.DataFrame(columns=all_actions)
        df_group_ooigen_action_dfs = pd.DataFrame(columns=all_actions)

        # add row of empty lists for participant to group summary dfs (why list: dfs can only be stored in other dfs in a list)
        df_allgroups_gen_action_dfs.loc[groups[i]] =  np.empty((len(all_actions), 0)).tolist()           
        df_allgroups_ooi_action_dfs.loc[groups[i]] =  np.empty((len(all_actions), 0)).tolist()
        df_allgroups_ooigen_action_dfs.loc[groups[i]] =  np.empty((len(all_actions), 0)).tolist()

        df_group_kcoeff_per_action = pd.DataFrame(columns = all_actions)

        df_group_duration_per_action = pd.DataFrame(columns = all_actions)

        df_group_seq_comp = pd.DataFrame()


        # iterate through participants
        for j in range(len(participants[i])):

            # create a df that stores all summary dfs per action of one participant
            df_pp_gen_action_dfs = pd.DataFrame(columns=all_actions)
            df_pp_ooi_action_dfs = pd.DataFrame(columns=all_actions)
            df_pp_ooigen_action_dfs = pd.DataFrame(columns=all_actions)
        
            # add row of empty lists for participant to group summary df (why list: dfs can only be stored in other dfs in a list)
            df_group_gen_action_dfs.loc[participants[i][j]] =  np.empty((len(all_actions), 0)).tolist()
            df_group_ooi_action_dfs.loc[participants[i][j]] =  np.empty((len(all_actions), 0)).tolist()
            df_group_ooigen_action_dfs.loc[participants[i][j]] =  np.empty((len(all_actions), 0)).tolist()

            df_pp_kcoeff_per_action = pd.DataFrame(columns = all_actions)

            df_pp_duration_per_action = pd.DataFrame(columns = all_actions)

            list_pp_seq_comp = []

            # iterate through each trial
            for k in range(len(trial_paths[i][j])):

                # define trial output path
                trial_output_path = output_path / Path(groups[i]) / Path(participants[i][j] / Path(trials[i][j][k]))

                # import ogd data
                ogd_data = pd.read_csv(trial_paths[i][j][k] + '_ogd.txt', sep='\t')

                # extract all OOIs
                all_ooi = ooi_metrics.extract_oois(ogd_data)

                # preprocess ogd data and add columns (fixation object and fixation time)
                ogd_final = ooi_metrics.prepare_ogd_file(ogd_data, pixel_distance)

                # import fixationdata 
                fixationdata = pd.read_csv(trial_paths[i][j][k] + '_fixations.txt', sep='\t')

                # import saccadedata
                saccadedata = pd.read_csv(trial_paths[i][j][k] + '_saccades.txt', sep='\t')

                # extract actions -> new: defined in the beginning, since not all actions may occur in all trials
                #all_actions = ogd_final['action'].unique().tolist()
               
                # get dataframe with actions + time from ogd dataframe
                df_actions = action_separation.action_times(ogd_final, fixationdata, all_actions)
                # save duration per step to trial folder
                df_duration_per_step = df_actions[['action', 'start_time_action', 'end_time_action']]
                df_duration_per_step.to_csv(trial_output_path / 'general_analysis' / Path('{} Duration per Step.csv'.format(trials[i][j][k])))
                
                ##  make df with average duration per action (general analysis)

                # make one column with duration
                df_duration_per_step['duration'] = df_duration_per_step['end_time_action'] - df_duration_per_step['start_time_action']
                # make one df with durations per action
                df_trial_duration_per_action = pd.DataFrame(columns = all_actions)
                df_trial_duration_per_action.loc[trials[i][j][k]] = np.empty((len(all_actions), 0)).tolist()

                for action in all_actions:
                    for x in range(len(df_duration_per_step)):
                        if df_duration_per_step['action'][x] == action:
                            df_trial_duration_per_action[action][0].append(df_duration_per_step['duration'][x])
                
                # add column with mean per action
                list_means = []
                for x in range(len(all_actions)):
                    if df_trial_duration_per_action.iloc[0][x] == 0:
                        list_means.append(0)
                    else:
                        list_means.append(statistics.mean(df_trial_duration_per_action.iloc[0][x]))      
                df_trial_duration_per_action.loc['Mean {}'.format(trials[i][j][k])] = list_means

                # make barplot
                vis_path = trial_output_path / Path('general_analysis') / Path('visualisations')
                os.makedirs(vis_path, exist_ok=True)
                visualisations.vis_gen_metrics_duration_per_action(df_trial_duration_per_action, vis_path, trials[i][j][k])


                # add new column to df_duration_per_action                
                df_pp_duration_per_action.loc[trials[i][j][k]] = df_trial_duration_per_action.loc['Mean {}'.format(trials[i][j][k])]


                # save a list with the actions
                action_sequence = df_actions['action'].tolist()


                ## distance algorithm
                if sequence_comp == True:
                    distance = sequence_comparisons.calculate_difference(opt_sequence, action_sequence, algrthm)
                    # save to list to add to df_group_distance
                    list_pp_seq_comp.append(distance)


                ## k-coefficient
                if kcoeff_analysis == True:
                    
                    ### (maybe put in separate function)
      
                    # import df_kcoeff of trial
                    analysispath = trial_output_path / Path('k-coefficient_analysis')
                    df_kcoeff_action = pd.read_csv(analysispath / '{}_k-coefficient_analysis.csv'.format(trials[i][j][k]), index_col=[0])
                    # add a column with action
                    df_kcoeff_action['Action'] = [0 for x in range(len(df_kcoeff_action))]
                    df_kcoeff_action['Outside 2x Stdev'] = [0 for x in range(len(df_kcoeff_action))]
                    df_kcoeff_action['Focal/Ambient'] = [0 for x in range(len(df_kcoeff_action))]

                    # add empty row to kcoeff per action df
                    df_trial_kcoeff_per_action = pd.DataFrame(columns=all_actions)
                    df_trial_kcoeff_per_action.loc['K-Coefficient per action'] =  np.empty((len(all_actions), 0)).tolist()


                    row_kcoeff=0
                    action_list_focal = []
                    action_list_ambient = []
                    for kcoeff in df_kcoeff_action['K-coefficient']:
                        time = df_kcoeff_action['start_time'][row_kcoeff]
                        for row_action in range(len(df_actions)):
                            if time > df_actions['start_time_action'][row_action] and time < df_actions['end_time_action'][row_action]:
                                df_kcoeff_action['Action'][row_kcoeff] = df_actions['action'][row_action]
                                # add if kcoeff is focal or ambient
                                if kcoeff > 0:
                                    df_kcoeff_action['Focal/Ambient'][row_kcoeff] = 'Focal'
                                else:
                                    df_kcoeff_action['Focal/Ambient'][row_kcoeff] = 'Ambient'
                                # add if kcoeff is outside 2x standard deviation
                                if kcoeff > (mean_kcoeff_all + 2*stdev_kcoeff_all) or kcoeff < mean_kcoeff_all - 2*stdev_kcoeff_all:
                                    df_kcoeff_action['Outside 2x Stdev'][row_kcoeff] = True
                                else:
                                    df_kcoeff_action['Outside 2x Stdev'][row_kcoeff] = False
                                # also add to df_trial_kcoeff_per_action
                                df_trial_kcoeff_per_action[df_actions['action'][row_action]]['K-Coefficient per action'].append(kcoeff)

                                                    
                        row_kcoeff = row_kcoeff + 1     

                    df_kcoeff_action.to_csv(analysispath / '{}_k-coefficient_analysis_with_actions.csv'.format(trials[i][j][k]))

                    # add rows with calculated average k-coeff per action per trial, if outside stdev or not and if focal or ambient
                    # add empty rows first
                    df_trial_kcoeff_per_action.loc['Mean {}'.format(trials[i][j][k])] = pd.Series([])
                    df_trial_kcoeff_per_action.loc['Outside 2x Stdev'] = 'No' 
                    df_trial_kcoeff_per_action.loc['Focal/Ambient'] =  'Ambient' 
                    # iterate through each acction
                    for x in range(len(df_trial_kcoeff_per_action.columns)):
                        kcoeff_list = df_trial_kcoeff_per_action.loc['K-Coefficient per action'][x] 
                        # if no kcoeffs for this action, assign np.nan
                        if kcoeff_list == []:
                            df_trial_kcoeff_per_action.loc['Mean {}'.format(trials[i][j][k])][x] =  np.nan 
                            df_trial_kcoeff_per_action.loc['Outside 2x Stdev'][x] =  np.nan 
                        # otherwise calculate mean
                        else:
                            kcoeff_mean = statistics.mean(df_trial_kcoeff_per_action.loc['K-Coefficient per action'][x])
                            df_trial_kcoeff_per_action.loc['Mean {}'.format(trials[i][j][k])][x] = kcoeff_mean
                            # check if any of the means are outside 2x standard deviation of overall mean and change to yes if the case
                            if kcoeff_mean > (mean_kcoeff_all + 2*stdev_kcoeff_all) or kcoeff_mean < mean_kcoeff_all - 2*stdev_kcoeff_all:
                                df_trial_kcoeff_per_action.loc['Outside 2x Stdev'][x] = 'Yes'
                            # change if mean is focal
                            if kcoeff_mean > 0:
                                df_trial_kcoeff_per_action.loc['Focal/Ambient'][x] = 'Focal'

                    # save trial df to csv
                    df_trial_kcoeff_per_action.to_csv(analysispath / Path('{} K-Coefficient per Action.csv'.format(trials[i][j][k])))

                    # visualisation of df
                    vis_path = analysispath / Path('visualisations')
                    os.makedirs(vis_path, exist_ok=True)
                    visualisations.vis_kcoeff_barplot_action(df_trial_kcoeff_per_action,vis_path, trials[i][j][k], 'Whole Trial' )
                
                    # add new column to pp df with trial mean
                    df_pp_kcoeff_per_action.loc['Mean {}'.format(trials[i][j][k])] = df_trial_kcoeff_per_action.iloc[1]
                           

                
                ## general metrics
                # add change idx of fixationdata df to df_action
                df_actions = action_separation.fix_sac_data_per_action(df_actions, fixationdata, 'fixations')
                # add change idx of saccadedata df to df_action
                df_actions = action_separation.fix_sac_data_per_action(df_actions, saccadedata, 'saccades')

                # calculate general metrics with fixationdata and saccadedata
                general_metrics_action_df_list = action_separation.get_general_metrics_per_action_df_list(df_actions, fixationdata, saccadedata, trials[i][j][k])
                

                ## ooi-based metrics
                ooi_metrics_action_df_list, gen_ooi_metrics_action_df_list = action_separation.get_all_ooi_metrics_per_action_df_list(df_actions, ogd_final, all_ooi, trials[i][j][k])


                # add row of empty lists for trial to participant summary df 
                df_pp_gen_action_dfs.loc[trials[i][j][k]] =  np.empty((len(all_actions), 0)).tolist()
                df_pp_ooi_action_dfs.loc[trials[i][j][k]] =  np.empty((len(all_actions), 0)).tolist()
                df_pp_ooigen_action_dfs.loc[trials[i][j][k]] =  np.empty((len(all_actions), 0)).tolist()


                ## combine all dfs to one summary df per action
                for action in all_actions:

                    # extract indeces of the current action in the action_sequence (from df_actions)
                    idx_action_dfs = [ind for ind, ele in enumerate(action_sequence) if ele == action]

                    # output path to save dfs
                    #trial_output_path = output_path / Path(groups[i]) / Path(participants[i][j]) / Path(trials[i][j][k])

                    
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

                    # visualisations of ooi metrics per action per trial
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
            


            ### summary per participant

            ## general metrics

            # create directory and define output path
            save_path = output_path / Path(groups[i]) / Path(participants[i][j]) / Path('general_analysis')
            os.makedirs(save_path, exist_ok= True)

            # create directory and define output path of visualisations
            vis_path = save_path / Path('visualisations')
            os.makedirs(vis_path, exist_ok = True)
            
            for action in all_actions:
                df_pp_action_list = [df_pp_gen_action_dfs[action][x][0] for x in range(len(df_pp_gen_action_dfs))]
                df_summary_pp_action = general_metrics.summary_general_analysis(df_pp_action_list, participants[i][j], save_path, action)

                # extract row with means per pp (second last row) and append to group summary df
                pp_df_average = df_summary_pp_action.iloc[[-2]]
                df_group_gen_action_dfs[action][j].append(pp_df_average)
                
                # visualisation of mean values of one participant
                visualisations.vis_gen_metrics_barplots(df_summary_pp_action, vis_path, participants[i][j], action) 


            # duration per action
            df_pp_duration_per_action.loc['Mean {}'.format(participants[i][j])] = df_pp_duration_per_action.mean()
            vis_path = save_path / Path('visualisations')
            os.makedirs(vis_path, exist_ok = True)
            visualisations.vis_gen_metrics_duration_per_action(df_pp_duration_per_action, vis_path, participants[i][j])
            # add mean to group 
            df_group_duration_per_action.loc[participants[i][j]] = df_pp_duration_per_action.loc['Mean {}'.format(participants[i][j])] 


            ## ooi metrics

            # create directory and define output path of csv file
            save_path = output_path / Path(groups[i]) / Path(participants[i][j]) / Path('ooi_analysis')
            os.makedirs(save_path, exist_ok = True)

            # create directory and define output path of visualisations
            vis_path = save_path / Path('visualisations')
            os.makedirs(vis_path, exist_ok = True)
            
            for action in all_actions:
                df_pp_action_list = [df_pp_ooi_action_dfs[action][x][0] for x in range(len(df_pp_ooi_action_dfs))]
                df_summary_pp_action, df_summary_pp_action_means = ooi_metrics.summary_ooi_analysis(df_pp_action_list, participants[i][j], save_path, action)

                # append means df to group summary df    
                df_group_ooi_action_dfs[action][j].append(df_summary_pp_action_means) 

                # visualisation of mean values of one participant
                visualisations.vis_ooi_metrics(df_summary_pp_action_means, vis_path, participants[i][j], action) 

            
            ## ooi-based general metrics
            
            for action in all_actions:
                df_pp_action_list = [df_pp_ooigen_action_dfs[action][x][0] for x in range(len(df_pp_ooigen_action_dfs))]
                df_summary_pp_action = ooi_metrics.summary_ooigen_analysis(df_pp_action_list, participants[i][j], save_path, action)

                # extract row with means per pp (second last row) and append to group summary df
                pp_df_average = df_summary_pp_action.iloc[[-2]]
                df_group_ooigen_action_dfs[action][j].append(pp_df_average)
                
                # visualisation of mean values of one participant
                visualisations.vis_ooigen_barplots(df_summary_pp_action, vis_path, participants[i][j], action) 
        

            ## k-coefficient
            if kcoeff_analysis == True:
                save_path = output_path / Path(groups[i]) / Path(participants[i][j]) / Path('k-coefficient_analysis')
                os.makedirs(save_path, exist_ok = True)
                # add row to participant df with mean 
                df_pp_kcoeff_per_action.loc['Mean {}'.format(participants[i][j])] = df_pp_kcoeff_per_action.mean()
                # add rows for std dev and focal/ambient
                df_pp_kcoeff_per_action.loc['Outside 2x Stdev'] = ['No']*len(df_pp_kcoeff_per_action.columns)
                df_pp_kcoeff_per_action.loc['Focal/Ambient'] = ['ambient']*len(df_pp_kcoeff_per_action.columns)

                # go through each action
                for x in range(len(df_pp_kcoeff_per_action.columns)):
                    kcoeff_mean = df_pp_kcoeff_per_action.loc['Mean {}'.format(participants[i][j])][x]
                    # check if mean is outside 2x standard deviation of overall mean and change to True if the case
                    if kcoeff_mean > (mean_kcoeff_all + 2*stdev_kcoeff_all) or kcoeff_mean < mean_kcoeff_all - 2*stdev_kcoeff_all:
                        df_pp_kcoeff_per_action.loc['Outside 2x Stdev'][x] = 'Yes'
                    # change to focal if > 0
                    else:
                        df_pp_kcoeff_per_action.loc['Focal/Ambient'][x] = 'Ambient'

                # save pp df to csv
                df_pp_kcoeff_per_action.to_csv(save_path / Path('{} K-Coefficient per Action.csv'.format(participants[i][j])))

                # visualisation of df
                vis_path = save_path / Path('visualisations')
                os.makedirs(vis_path, exist_ok=True)
                visualisations.vis_kcoeff_barplot_action(df_pp_kcoeff_per_action,vis_path, participants[i][j], 'Whole Trial' )
            
                # take df_pp_action_kcoeff to group level -> visualisations        
                df_group_kcoeff_per_action.loc['Mean {}'.format(participants[i][j])] = df_pp_kcoeff_per_action.loc['Mean {}'.format(participants[i][j])]                     


            ## sequence comparison
            if sequence_comp == True:
                df_group_seq_comp[participants[i][j]] = list_pp_seq_comp





        ### summary per group

        ## general analysis

        # create directory and define output path
        save_path = output_path / Path(groups[i]) / Path('general_analysis')
        os.makedirs(save_path, exist_ok= True)

        # create directory and define output path of visualisations
        vis_path = save_path / Path('visualisations')
        os.makedirs(vis_path, exist_ok = True)
      

        for action in all_actions:
            df_group_action_list = [df_group_gen_action_dfs[action][x][0] for x in range(len(df_group_gen_action_dfs))]
            df_summary_group_action = general_metrics.summary_general_analysis(df_group_action_list, groups[i], save_path, action)

            # extract row with means (second last) per pp and append to group summary df
            group_df_average = df_summary_group_action.iloc[[-2]]
            df_allgroups_gen_action_dfs[action][i].append(group_df_average)

            # visualisation of mean values per group
            visualisations.vis_gen_metrics_barplots(df_summary_group_action, vis_path, groups[i], action) 

            

        # duration per step
        df_group_duration_per_action.loc['Mean {}'.format(groups[i])] = df_group_duration_per_action.mean()
        vis_path = save_path / Path('visualisations')
        os.makedirs(vis_path, exist_ok = True)
        visualisations.vis_gen_metrics_duration_per_action(df_group_duration_per_action, vis_path, groups[i])
        # add mean to group 
        df_allgroups_duration_per_action.loc[groups[i]] = df_group_duration_per_action.loc['Mean {}'.format(groups[i])] 


        
        ## ooi analysis

        # create directory and define output path
        save_path = output_path / Path(groups[i]) / Path('ooi_analysis')
        os.makedirs(save_path, exist_ok= True)

        # create directory and define output path of visualisations
        vis_path = save_path / Path('visualisations')
        os.makedirs(vis_path, exist_ok = True)
            
        
        for action in all_actions:
            df_group_action_list = [df_group_ooi_action_dfs[action][x][0] for x in range(len(df_group_ooi_action_dfs))]
            df_summary_group_action, df_summary_group_action_means = ooi_metrics.summary_ooi_analysis(df_group_action_list, groups[i], save_path, action)

            # append means df to group summary df    
            df_allgroups_ooi_action_dfs[action][i].append(df_summary_group_action_means)  

            # visualisation of mean values of one group
            visualisations.vis_ooi_metrics(df_summary_group_action_means, vis_path, groups[i], action) 

        
        ## ooi-based general metrics
        
        for action in all_actions:
            df_group_action_list = [df_group_ooigen_action_dfs[action][x][0] for x in range(len(df_group_ooigen_action_dfs))]
            df_summary_group_action = ooi_metrics.summary_ooigen_analysis(df_group_action_list,groups[i], save_path, action)

            # extract row with means per pp (second last row) and append to group summary df
            group_df_average = df_summary_group_action.iloc[[-2]]
            df_allgroups_ooigen_action_dfs[action][i].append(group_df_average)
                            
            # visualisation of mean values of one participant
            visualisations.vis_ooigen_barplots(df_summary_group_action, vis_path, groups[i], action) 

        
        ## k-coefficient
        if kcoeff_analysis == True:
            save_path = output_path / Path(groups[i]) / Path('k-coefficient_analysis')
            os.makedirs(save_path, exist_ok = True)
            # add row to participant df with mean 
            df_group_kcoeff_per_action.loc['Mean {}'.format(groups[i])] = df_group_kcoeff_per_action.mean()
            # add empty rows 
            df_group_kcoeff_per_action.loc['Outside 2x Stdev'] = ['No']*len(df_group_kcoeff_per_action.columns)
            df_group_kcoeff_per_action.loc['Focal/Ambient'] = ['ambient']*len(df_group_kcoeff_per_action.columns)

            # go through each action
            for x in range(len(df_group_kcoeff_per_action.columns)):
                kcoeff_mean = df_group_kcoeff_per_action.loc['Mean {}'.format(groups[i])][x]
                # check if mean is outside 2x standard deviation of overall mean and change to True if the case
                if kcoeff_mean > (mean_kcoeff_all + 2*stdev_kcoeff_all) or kcoeff_mean < mean_kcoeff_all - 2*stdev_kcoeff_all:
                    df_group_kcoeff_per_action.loc['Outside 2x Stdev'][x] = 'Yes'
                # change to focal if > 0
                if kcoeff_mean > 0:
                    df_group_kcoeff_per_action.loc['Focal/Ambient'][x] = 'Focal'

            # save pp df to csv
            df_group_kcoeff_per_action.to_csv(save_path / Path('{} K-Coefficient per Action.csv'.format(groups[i])))

            # visualisation of df
            vis_path = save_path / Path('visualisations')
            os.makedirs(vis_path, exist_ok=True)
            visualisations.vis_kcoeff_barplot_action(df_group_kcoeff_per_action,vis_path, groups[i], 'Whole Trial' )

            # take df_pp_action_kcoeff to group level -> visualisations        
            df_allgroups_kcoeff_per_action.loc['Mean {}'.format(groups[i])] = df_group_kcoeff_per_action.loc['Mean {}'.format(groups[i])]                


        ## sequence comparison
        if sequence_comp == True:
            df_group_seq_comp.index = ['trial0{}'.format(x) for x in range(1,len(df_group_seq_comp)+1)]
            analysispath = output_path / Path(groups[i]) / Path('sequence_comparison')
            os.makedirs(analysispath, exist_ok=True)
            df_group_seq_comp.to_csv(analysispath / '{} Sequence Comparison.csv'.format(groups[i]))
    
    ### summary of all groups

    ## general analysis

    # create directory and define output path
    save_path = output_path / Path('general_analysis')
    os.makedirs(save_path, exist_ok= True)

    # create directory and define output path of visualisations
    vis_path = save_path / Path('visualisations')
    os.makedirs(vis_path, exist_ok = True)

    for action in all_actions:
        df_allgroups_action_list = [df_allgroups_gen_action_dfs[action][x][0] for x in range(len(df_allgroups_gen_action_dfs))]
        df_summary_allgroups_action = general_metrics.summary_general_analysis(df_allgroups_action_list, 'All Groups', save_path, action)
                
        # visualisation of mean values per group
        visualisations.vis_gen_metrics_barplots(df_summary_allgroups_action, vis_path, 'All Groups', action) 


    # duration per step
    df_allgroups_duration_per_action.loc['Mean All Groups'] = df_allgroups_duration_per_action.mean()
    vis_path = save_path / Path('visualisations')
    os.makedirs(vis_path, exist_ok = True)
    visualisations.vis_gen_metrics_duration_per_action(df_allgroups_duration_per_action, vis_path,'All Groups')


    ## ooi analysis
    
    # create directory and define output path
    save_path = output_path / Path('ooi_analysis')
    os.makedirs(save_path, exist_ok= True)

    # create directory and define output path of visualisations
    vis_path = save_path / Path('visualisations')
    os.makedirs(vis_path, exist_ok = True)
    
    for action in all_actions:
        df_allgroups_action_list = [df_allgroups_ooi_action_dfs[action][x][0] for x in range(len(df_allgroups_ooi_action_dfs))]
        df_summary_allgroups_action, df_summary_allgroups_action_means = ooi_metrics.summary_ooi_analysis(df_allgroups_action_list,'All Groups', save_path, action)
        
        # visualisation of mean values of all groups
        visualisations.vis_ooi_metrics(df_summary_allgroups_action_means, vis_path, 'All Groups', action) 



    ## ooi-based general analysis
    for action in all_actions:
        df_allgroups_action_list = [df_allgroups_ooigen_action_dfs[action][x][0] for x in range(len(df_allgroups_ooigen_action_dfs))]
        df_summary_allgroups_action = ooi_metrics.summary_ooigen_analysis(df_allgroups_action_list,'All Groups', save_path, action)

                                    
        # visualisation of mean values of one participant
        visualisations.vis_ooigen_barplots(df_summary_allgroups_action, vis_path, 'All Groups', action) 


    ## k-coefficient
    if kcoeff_analysis == True:
        save_path = output_path / Path('k-coefficient_analysis')
        os.makedirs(save_path, exist_ok = True)
        # add row to participant df with mean 
        df_allgroups_kcoeff_per_action.loc['Mean All Groups'] = df_allgroups_kcoeff_per_action.mean()
        # add empty rows 
        df_allgroups_kcoeff_per_action.loc['Outside 2x Stdev'] = ['No']*len(df_allgroups_kcoeff_per_action.columns)
        df_allgroups_kcoeff_per_action.loc['Focal/Ambient'] = ['ambient']*len(df_allgroups_kcoeff_per_action.columns)

        # go through each action
        for x in range(len(df_allgroups_kcoeff_per_action.columns)):
            kcoeff_mean = df_allgroups_kcoeff_per_action.loc['Mean All Groups'][x]
            # check if mean is outside 2x standard deviation of overall mean and change to True if the case
            if kcoeff_mean > (mean_kcoeff_all + 2*stdev_kcoeff_all) or kcoeff_mean < mean_kcoeff_all - 2*stdev_kcoeff_all:
                df_allgroups_kcoeff_per_action.loc['Outside 2x Stdev'][x] = 'Yes'
            # change to focal if > 0
            if kcoeff_mean > 0:
                df_allgroups_kcoeff_per_action.loc['Focal/Ambient'][x] = 'Focal'

        # save pp df to csv
        df_allgroups_kcoeff_per_action.to_csv(save_path / Path('All Groups K-Coefficient per Action.csv'))


        # visualisation of df
        vis_path = save_path / Path('visualisations')
        os.makedirs(vis_path, exist_ok=True)
        visualisations.vis_kcoeff_barplot_action(df_allgroups_kcoeff_per_action,vis_path, 'All Groups', 'Whole Trial' )




#endregion


# _____________ STATISTICS (only implemented for entropy yet)
#region

if run_stats == True:
    
    # save overall mean and overall standard deviation of all trials (not stdev of means of group, similar to k-coefficient)
    
    # iterate through each trial and append to one list
    list_sge = []
    list_gte = []

    for i in range(len(groups)):
        for j in range(len(participants[i])):
            for k in range(len(trials[i][j])):
                # define path to csv file
                analysispath = output_path / Path(groups[i]) / Path(participants[i][j] / Path(trials[i][j][k])) / Path('ooi_analysis')
                df_ooi_gen_metrics_2 = pd.read_csv(analysispath / Path('{}_ooi-based_general_analysis.csv'.format(trials[i][j][k])))
                list_sge.append(df_ooi_gen_metrics_2['Normalised Stationary Gaze Entropy'][0])
                list_gte.append(df_ooi_gen_metrics_2['Normalised Gaze Transition Entropy'][0])

    # calculate mean and standard deviation
    mean_sge = statistics.mean(list_sge)
    stdev_sge= statistics.pstdev(list_sge)
    mean_gte = statistics.mean(list_gte)
    stdev_gte = statistics.pstdev(list_gte)

    
    metrics = ['Normalised Stationary Gaze Entropy', 'Normalised Gaze Transition Entropy' ]
    means = [mean_sge, mean_gte]
    stdevs = [stdev_sge, stdev_sge]


    # go through summaries and make barplots per participants and mark >2stdev
    for i in range(len(groups)):
        for j in range(len(participants[i])):
        
            # add col that states whether trial was outside 2x stdev or not 
            # can be made into a loop through  all metrics later

            # stats per participant
            analysispath = output_path / Path(groups[i]) / Path(participants[i][j]) / Path('ooi_analysis')
            pp_summary = pd.read_csv(analysispath / Path('{}_summary_ooi-based_general_analysis_Whole Trial.csv'.format(participants[i][j])), index_col=[0])
            vis_path = analysispath / Path('visualisations')

            
            y=0
            for metric in metrics:
                df_stats = pp_summary[[metric]]
                df_stats.drop(df_stats.tail(1).index,inplace=True)
                df_stats['Outside 2x Stdev'] = 'No' 
                for x in range(len(df_stats)):
                    val = df_stats[metric][x] 
                    if val > (mean_sge + 2*stdev_sge) or val < (mean_sge - 2*stdev_sge):
                        df_stats['Outside 2x Stdev'][x] = 'Yes'
                
                visualisations.vis_stats_ooi_gen(df_stats, vis_path, participants[i][j], metric, 'Whole Trial')
                
                y=y+1
        

        # stats per group
        analysispath = output_path / Path(groups[i]) / Path('ooi_analysis')
        group_summary = pd.read_csv(analysispath / Path('{}_summary_ooi-based_general_analysis_Whole Trial.csv'.format(groups[i])), index_col=[0])
        vis_path = analysispath / Path('visualisations')


        y=0
        for metric in metrics:
            df_stats = group_summary[[metric]]
            df_stats.drop(df_stats.tail(1).index,inplace=True)
            df_stats['Outside 2x Stdev'] = 'No' 
            for x in range(len(df_stats)):
                val = df_stats[metric][x] 
                if val > (mean_sge + 2*stdev_sge) or val < (mean_sge - 2*stdev_sge):
                    df_stats['Outside 2x Stdev'][x] = 'Yes'
            
            visualisations.vis_stats_ooi_gen(df_stats, vis_path, groups[i], metric, 'Whole Trial')
            
            y=y+1
    
    # stats per all groups
    analysispath = output_path / Path('ooi_analysis')
    allgroups_summary = pd.read_csv(analysispath / Path('{}_summary_ooi-based_general_analysis_Whole Trial.csv'.format('All Groups')), index_col=[0])
    vis_path = analysispath / Path('visualisations')


    y=0
    for metric in metrics:
        df_stats = allgroups_summary[[metric]]
        df_stats.drop(df_stats.tail(1).index,inplace=True)
        df_stats['Outside 2x Stdev'] = 'No' 
        for x in range(len(df_stats)):
            val = df_stats[metric][x] 
            if val > (mean_sge + 2*stdev_sge) or val < (mean_sge - 2*stdev_sge):
                df_stats['Outside 2x Stdev'][x] = 'Yes'
        
        visualisations.vis_stats_ooi_gen(df_stats, vis_path, 'All Groups', metric, 'Whole Trial')
        
        y=y+1



#endregion
    
   
# _____________ GET RESULTS SUMMARY REPORT
#region

if results_summary_report == True:

    ### only if it should be run separately
    #ooi_analysis = True
    #kcoeff_analysis = True
    #action_analysis = True

    
    img_import_path = output_path
    results_path = Path('Summary Report')
    os.makedirs(results_path, exist_ok = True)
    result_summaries.allgroups_groups_results(img_import_path, results_path, ooi_analysis, kcoeff_analysis, action_analysis, 'All Groups')

    # iterate through groups    
    for i in range(len(groups)):
        img_import_path = output_path / Path(groups[i])
        results_path = Path('Summary Report') / Path(groups[i])
        os.makedirs(results_path, exist_ok = True)
        result_summaries.allgroups_groups_results(img_import_path, results_path, ooi_analysis, kcoeff_analysis, action_analysis, groups[i])
        
        # iterate through participants
        for j in range(len(participants[i])):
            img_import_path = output_path / Path(groups[i]) / participants[i][j]
            results_path = Path('Summary Report') / Path(groups[i]) / participants[i][j]
            os.makedirs(results_path, exist_ok = True)
            result_summaries.participants_results(img_import_path, results_path, ooi_analysis, kcoeff_analysis, action_analysis, participants[i][j])


#endregion
    

