'''
OOI-based analysis
'''

import os
import pandas as pd
import numpy as np
from pathlib import Path
import statistics
import logging as log

# local imports
import src.util.ooi_metrics as ooi_metrics
import src.util.visualisations as visualisations

def analyse(list_tuple: list, output_path: str, pixel_distance) -> tuple:

    log.info("Starting ooi-based analysis.") 

    # get individual lists from tuple
    trials, trial_paths, trials_only, participants, participant_paths, groups, group_paths, output_path_groups = list_tuple

    # prepare data
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
        visualisations.vis_gen_metrics_boxplots_group(allgroups_nested_list, vis_path, 'All Groups', 'Whole Trial', metric, x_labels)
    
    log.info("Finished ooi-based analysis.") 
