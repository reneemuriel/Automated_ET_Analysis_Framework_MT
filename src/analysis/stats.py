'''
Calculation of statistics. To date only implemented for SGE and GTE.
'''

import os
import pandas as pd
import numpy as np
from pathlib import Path
import statistics
import logging as log

# local imports
import src.util.visualisations as visualisations

def analyse(list_tuple: list, output_path: str) -> tuple:

    log.info("Started to calculate statistics.") 

    # get individual lists from tuple
    trials, trial_paths, trials_only, participants, participant_paths, groups, group_paths, output_path_groups = list_tuple

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
    stdevs = [stdev_sge, stdev_gte]

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
                    if val > (means[y] + 2*stdevs[y]) or val < (means[y] - 2*stdevs[y]):
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
                if val > (means[y] + 2*stdevs[y]) or val < (means[y] - 2*stdevs[y]):
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
            if val > (means[y] + 2*stdevs[y]) or val < (means[y] - 2*stdevs[y]):
                df_stats['Outside 2x Stdev'][x] = 'Yes'
        
        visualisations.vis_stats_ooi_gen(df_stats, vis_path, 'All Groups', metric, 'Whole Trial')
        
        y=y+1

    log.info("Finished to calculate statistics.") 
