'''
General analysis
'''


import os
import pandas as pd
import numpy as np
import logging as log
from pathlib import Path
import statistics

# local imports
import src.util.tobii_to_fixations_old as t2f
import src.util.tobii_to_saccades_old as t2s
import src.util.general_metrics as general_metrics
import src.util.visualisations as visualisations

def analyse(list_tuple: list, output_path: str) -> tuple:

    log.info("Starting general analysis.") 

    # get individual lists from tuple
    trials, trial_paths, trials_only, participants, participant_paths, groups, group_paths, output_path_groups = list_tuple

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

    log.info("Finished general analysis.")

    return