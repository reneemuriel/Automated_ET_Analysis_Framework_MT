from re import I
import pandas as pd
import ooi_metrics
import numpy as np
import general_metrics

# separate trial into actions
def action_times(data, fixationdata, all_actions) -> pd.DataFrame():
                
    # initialize the action df
    df_actions = pd.DataFrame()
    df_actions['action'] = data['action']
    df_actions['start_time'] = data['start_time']
    df_actions['end_time'] = data['end_time']

    # add column with action as numbers to simplify finding changes
    #all_actions = data['action'].unique().tolist()
    dict_actions = {k: v for v, k in enumerate(all_actions)}
    df_actions['action_numbers'] = (df_actions['action']).map(dict_actions)


    # create a variable called 'change' that tells whether the event changed (calculates the difference to previous row)
    df_actions['change'] = df_actions['action_numbers'].diff()

    # remove rows where the event did not change:
    df_actions = df_actions.loc[df_actions['change'] !=0 ,:]

    # 
    df_actions['start_time_action'] = df_actions['start_time']
    df_actions['end_time_action'] = df_actions['start_time'].shift(-1)


    # add time of first and last action
    # end of trial time
    end_time_seconds = float(fixationdata['Event End Trial Time [ms]'].iloc[len(fixationdata)-1])
    df_actions['end_time_action'].iloc[len(df_actions)-1] = end_time_seconds
    # start of trial time
    df_actions['start_time_action'][0] = float(0)

    # add a new index
    df_actions.reset_index(inplace=True)
    # save the indeces in a column (can be used to separate the ogd file into new dfs)
    df_actions = df_actions.rename(columns = {'index':'action_change_index_ogd'}) # changed

    return df_actions




### OGD DATA (ooi-based analysis)
#region

# separate ogd dataframe into new dataframes and calculate ooi_metrics
def get_ooi_metrics_per_action_df_list(df_actions, data, all_ooi):
        
    ooi_metrics_action_df_list = []

    step=0
    for step in range(0,len(df_actions)):
    
        ### OOI-based action-based analysis

        # create dataframe for one step

        # if last row of df_action, ogd_final from last change index until end
        if step == (len(df_actions)-1):
            ogd_action = data[df_actions['action_change_index_ogd'][step]:]
        
        # otherwise, from change_index to next change_index
        else:
            ogd_action = data[df_actions['action_change_index_ogd'][step]:df_actions['action_change_index_ogd'][step+1]]
        
        # reindex this dataframe
        ogd_action.reset_index(inplace = True, drop = True)  

        # calculate ooi metrics (all but time to first fixation)                
        df_ooi_metrics_action = ooi_metrics.calculate_ooi_metrics_per_action(ogd_action, all_ooi)
        # append to df list
        ooi_metrics_action_df_list.append(df_ooi_metrics_action)

    return ooi_metrics_action_df_list

# separate ogd dataframe into new dataframes per action and calculate general_ooi_metrics
def get_general_ooi_metrics_per_action_df_list(df_actions, data, all_ooi, trialname):
    
    general_ooi_metrics_action_df_list = []

    step=0
    for step in range(0,len(df_actions)):
        
        # create dataframe for one step

        # if last row of df_action, ogd_final from last change index until end
        if step == (len(df_actions)-1):
            ogd_action = data[df_actions['action_change_index_ogd'][step]:]
        
        # otherwise, from change_index to next change_index
        else:
            ogd_action = data[df_actions['action_change_index_ogd'][step]:df_actions['action_change_index_ogd'][step+1]]
        
        # reindex this dataframe
        ogd_action.reset_index(inplace = True, drop = True)  

        # calculate ooi metrics (all but time to first fixation)                
        df_general_ooi_metrics_action = ooi_metrics.calculate_general_ooi_metrics_per_action(ogd_action, all_ooi, trialname)
        # append to df list
        general_ooi_metrics_action_df_list.append(df_general_ooi_metrics_action)

    return general_ooi_metrics_action_df_list


# summary per action for ooi metrics
def summary_ooi_metrics_per_action(ooi_metrics_action_df_list, idx_action_dfs):
    
    # create df_summary with identical columns 
    # and indeces of metrics that can be calculated by addition (df.add())
    df_summary_ooi = pd.DataFrame(columns=ooi_metrics_action_df_list[0].columns, index=['Hits', 'Total Fixation Time [ms]', 'Total Dwelltime [ms]' , 'Revisits', 'Relative Dwelltime [%]'])
    
    # convert nans to 0
    df_summary_ooi.fillna(0, inplace=True)

    # additions 
    for idx_action in idx_action_dfs:
        df_summary_ooi = df_summary_ooi.add(ooi_metrics_action_df_list[idx_action], axis =0)
    df_summary_ooi.fillna(0, inplace=True)

    # now calculate average fixation time and average dwelltime
    df_summary_ooi.loc['Average Fixation Time [ms]'] = df_summary_ooi.loc['Total Fixation Time [ms]'] / df_summary_ooi.loc['Hits'].replace({ 0 : np.nan })
    df_summary_ooi.loc['Average Dwelltime [ms]'] = df_summary_ooi.loc['Total Dwelltime [ms]'] / df_summary_ooi.loc['Revisits'].replace({ 0 : np.nan })

    # convert nans to 0 again
    df_summary_ooi.fillna(0, inplace=True)

    return df_summary_ooi

# summary per action for general ooi metrics
def summary_ooi_general_metrics_per_action(gen_ooi_metrics_action_df_list, idx_action_dfs, df_summary_ooi, general_metrics_action_df_list):

    
    # create df_summary with identical columns 
    # and indeces of metrics that can be calculated by addition (df.add())

    df_summary_ooi_gen = pd.DataFrame(index=gen_ooi_metrics_action_df_list[0].index, columns=['Total Hits', 'Total Dwells'])

    # convert nans to 0
    df_summary_ooi_gen.fillna(0, inplace=True)

    # additions 
    for idx_action in idx_action_dfs:
        df_summary_ooi_gen = df_summary_ooi_gen.add(gen_ooi_metrics_action_df_list[idx_action], axis =0)
    df_summary_ooi_gen.fillna(0, inplace=True)

    # calculate average dwelltime 
    tot_dwelltime_action = sum(df_summary_ooi.loc['Total Dwelltime [ms]'])
    tot_dwells_action = df_summary_ooi_gen['Total Dwells'][0]
    df_summary_ooi_gen['Average Dwelltime [ms]'] = tot_dwelltime_action / tot_dwells_action
    
    # calculate average stationary gaze entropy with duration per action: sum(GE_i*duration_i) / sum(durations)
    list_sum_sge = []
    list_total_duration = []
    for idx_action in idx_action_dfs:
        list_sum_sge.append(gen_ooi_metrics_action_df_list[idx_action]['Normalised Stationary Gaze Entropy'][0]*general_metrics_action_df_list[idx_action]['Total Duration [ms]'][0])
        list_total_duration.append(general_metrics_action_df_list[idx_action]['Total Duration [ms]'][0])
    
    sge_per_step = sum(list_sum_sge) / sum(list_total_duration)
    #df_summary_ooi_gen['Normalised Stationary Gaze Entropy'] =  df_summary_ooi_gen['Normalised Stationary Gaze Entropy'].replace([0], sge_per_step)
    df_summary_ooi_gen['Normalised Stationary Gaze Entropy'] = sge_per_step

    # calculate average gaze transition entropy (with duration per action)
    list_sum_gte = []
    list_total_duration = []
    for idx_action in idx_action_dfs:
        list_sum_gte.append(gen_ooi_metrics_action_df_list[idx_action]['Normalised Gaze Transition Entropy'][0]*general_metrics_action_df_list[idx_action]['Total Duration [ms]'][0])
        list_total_duration.append(general_metrics_action_df_list[idx_action]['Total Duration [ms]'][0])
    
    tge_per_step = sum(list_sum_gte) / sum(list_total_duration)
    df_summary_ooi_gen['Normalised Gaze Transition Entropy'] = tge_per_step


    return df_summary_ooi_gen

#endregion




### FIXATION/SACCADE DATA (general analysis)
#region

# separate fixationdata/saccadedata dataframe into new dataframes per action 
def fix_sac_data_per_action(df_actions, data, fixationorsaccadestring):
    i=0
    action_change_idx = [0]
    action_list = []
    for row in range(len(data)):
        action_list.append(df_actions['action'][i])
        # if last row
        if row == len(data)-1:
            break
        # if we are already in the last row of df_action, do not add 1 to i and continue with the loop
        if i == (len(df_actions)-1):
            continue

        # save change     
        elif data['Event End Trial Time [ms]'][row+1] > df_actions['end_time_action'][i]:
            action_change_idx.append(row+1)
            i = i + 1 
    data['action'] = action_list    
    df_actions['action_change_index_{}'.format(fixationorsaccadestring)] = action_change_idx

    return df_actions

# calculate general metrics of the cut dataframes
def get_general_metrics_per_action_df_list(df_actions, fixationdata, saccadedata, trialname):
        
    general_metrics_action_df_list = []

    step=0
    for step in range(0,len(df_actions)):
    
        # create dataframes for one step

        # if last row of df_action, ogd_final from last change index until end
        if step == (len(df_actions)-1):
            fixationdata_action = fixationdata[df_actions['action_change_index_fixations'][step]:]
            saccadedata_action = saccadedata[df_actions['action_change_index_saccades'][step]:]
        
        # otherwise, from change_index to next change_index
        else:
            fixationdata_action = fixationdata[df_actions['action_change_index_fixations'][step]:df_actions['action_change_index_fixations'][step+1]]
            saccadedata_action = saccadedata[df_actions['action_change_index_saccades'][step]:df_actions['action_change_index_saccades'][step+1]]
        
        # reindex dataframes
        fixationdata_action.reset_index(inplace = True, drop = True)  
        saccadedata_action.reset_index(inplace = True, drop = True)  

        # calculate  metrics (all but time to first fixation)                
        df_general_metrics_action = general_metrics.calculate_general_metrics_per_action(fixationdata_action, saccadedata_action, trialname)
        # append to df list
        general_metrics_action_df_list.append(df_general_metrics_action)

    return general_metrics_action_df_list

# summary per action for general metrics
def summary_general_metrics_per_action(general_metrics_action_df_list, idx_action_dfs):

    # create df_summary with identical columns 
    # and indeces of metrics that can be calculated by addition (df.add())
    df_summary_gen = pd.DataFrame(index = general_metrics_action_df_list[0].index, columns=['Number of Fixations', 'Total Fixation Duration [ms]', 'Total Saccade Duration [ms]', 'Number of Saccades', 'Total Duration [ms]'])
        
    # convert nans to 0
    df_summary_gen.fillna(0, inplace=True)

    # additions 
    for idx_action in idx_action_dfs:
        df_summary_gen = df_summary_gen.add(general_metrics_action_df_list[idx_action], axis = 1) # axis = ?
    df_summary_gen.fillna(0, inplace=True)

    # now calculate average fixation and saccade duration, and relative fix/saccade duration
    df_summary_gen['Average Fixation Duration [ms]'] = df_summary_gen['Total Fixation Duration [ms]'] / df_summary_gen['Number of Fixations']
    df_summary_gen['Average Saccade Duration [ms]'] = df_summary_gen['Total Saccade Duration [ms]'] / df_summary_gen['Number of Saccades']
    
    tot_fix = df_summary_gen['Total Fixation Duration [ms]'][0]
    tot_sac = df_summary_gen['Total Saccade Duration [ms]'][0]
    percent_fix = tot_fix / (tot_fix + tot_sac) * 100
    percent_sac = tot_sac / (tot_fix + tot_sac) * 100
    percentages = '{}/{}'.format(round(percent_fix), round(percent_sac))
    #idx = df_summary_gen.index[0] # to fill in calculated percentages (replace the current value (0))
    
    df_summary_gen['Relative Fixation/Saccade Duration [%]'] =    df_summary_gen['Relative Fixation/Saccade Duration [%]'].replace([0], percentages)


    # convert nans to 0 again    
    df_summary_gen.fillna(0, inplace=True)

    return df_summary_gen






#endregion