import os
import pandas as pd
import numpy as np
from pathlib import Path
import statistics

# local imports
import src.util.general_metrics as general_metrics
import src.util.ooi_metrics as ooi_metrics
import src.util.action_separation as action_separation
import src.util.sequence_comparisons as sequence_comparisons

import src.util.visualisations as visualisations


def analyse(list_tuple: list, output_path: str, pixel_distance: int, all_actions: list, template_sequence, sequence_comp: bool, kcoeff_analysis: bool, kcoeff_stats_list, mean_kcoeff_all, stdev_kcoeff_all) -> tuple:


    # get individual lists from tuple
    trials, trial_paths, trials_only, participants, participant_paths, groups, group_paths, output_path_groups = list_tuple

    # create a df that stores all general/ooi/ooi-based general analysis summary dfs per action of all groups
    df_allgroups_gen_action_dfs = pd.DataFrame(columns=all_actions)
    df_allgroups_ooi_action_dfs = pd.DataFrame(columns=all_actions)
    df_allgroups_ooigen_action_dfs = pd.DataFrame(columns=all_actions)

    df_allgroups_kcoeff_per_action = pd.DataFrame(columns = all_actions)

    df_allgroups_duration_per_action = pd.DataFrame(columns = all_actions)

    # can be integrated to gui later
    algrthm = 'levenshtein_distance'

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
                    distance = sequence_comparisons.calculate_difference(template_sequence, action_sequence, algrthm)
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
