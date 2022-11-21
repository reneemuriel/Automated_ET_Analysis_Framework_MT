import os
import pandas as pd
import numpy as np
from pathlib import Path
import statistics
import math

# local imports
import src.util.kcoefficient_calculation as kcoefficient_calculation
import src.util.visualisations as visualisations


def analyse(list_tuple: list, output_path: str) -> tuple:

    # get individual lists from tuple
    trials, trial_paths, trials_only, participants, participant_paths, groups, group_paths, output_path_groups = list_tuple


    fixation_durations = []
    saccade_amplitudes = []

    # iterate through groups    
    for i in range(len(groups)):
        
        # iterate through participants
        for j in range(len(participants[i])):

            # iterate through each trial
            for k in range(len(trials[i][j])):
                
                kcoeff_path = trial_paths[i][j][k] + '_tobii_kcoeff.tsv' # change to '_tobii_kcoeff.tsv' if old tobii export is used

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

    return mean_kcoeff_all, stdev_kcoeff_all

