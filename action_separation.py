import pandas as pd
import ooi_metrics
import numpy as np

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
    end_time_seconds = float(fixationdata['Event End Trial Time [ms]'].iloc[len(fixationdata)-1]/1000)
    df_actions['end_time_action'].iloc[len(df_actions)-1] = end_time_seconds
    # start of trial time
    df_actions['start_time_action'][0] = float(0)

    # add a new index
    df_actions.reset_index(inplace=True)
    # save the indeces in a column (can be used to separate the ogd file into new dfs)
    df_actions = df_actions.rename(columns = {'index':'action_change_index'})

    return df_actions

# separate ogd dataframe into new dataframes and calculate ooi_metrics
def get_ooi_metrics_per_action_df_list(df_actions, data, all_ooi):
        
    ooi_metrics_action_df_list = []

    step=0
    for step in range(0,len(df_actions)):
    
        ### OOI-based action-based analysis

        # create dataframe for one step

        # if last row of df_action, ogd_final from last change index until end
        if step == (len(df_actions)-1):
            ogd_action = data[df_actions['action_change_index'][step]:]
        
        # otherwise, from change_index to next change_index
        else:
            ogd_action = data[df_actions['action_change_index'][step]:df_actions['action_change_index'][step+1]]
        
        # reindex this dataframe
        ogd_action.reset_index(inplace = True, drop = True)  

        # calculate ooi metrics (all but time to first fixation)                
        df_ooi_metrics_action = ooi_metrics.calculate_ooi_metrics_per_action(ogd_action, all_ooi)
        # append to df list
        ooi_metrics_action_df_list.append(df_ooi_metrics_action)

    return ooi_metrics_action_df_list

# separate ogd dataframe into new dataframes and calculate general_ooi_metrics
def get_general_ooi_metrics_per_action_df_list(df_actions, data, all_ooi, trialname):
    
    general_ooi_metrics_action_df_list = []

    step=0
    for step in range(0,len(df_actions)):
        
        # create dataframe for one step

        # if last row of df_action, ogd_final from last change index until end
        if step == (len(df_actions)-1):
            ogd_action = data[df_actions['action_change_index'][step]:]
        
        # otherwise, from change_index to next change_index
        else:
            ogd_action = data[df_actions['action_change_index'][step]:df_actions['action_change_index'][step+1]]
        
        # reindex this dataframe
        ogd_action.reset_index(inplace = True, drop = True)  

        # calculate ooi metrics (all but time to first fixation)                
        df_general_ooi_metrics_action = ooi_metrics.calculate_general_ooi_metrics_per_action(ogd_action, all_ooi, trialname)
        # append to df list
        general_ooi_metrics_action_df_list.append(df_general_ooi_metrics_action)

    return general_ooi_metrics_action_df_list

# save summary per action for ooi metrics
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


def summary_ooi_general_metrics_per_action(gen_ooi_metrics_action_df_list, idx_action_dfs, df_summary_ooi):
    
    # create df_summary with identical columns 
    # and indeces of metrics that can be calculated by addition (df.add())

    # da ischs problemo
    df_summary_ooi_gen = pd.DataFrame(index=gen_ooi_metrics_action_df_list[0].index, columns=['Total Hits', 'Total Dwells'])

    # convert nans to 0
    df_summary_ooi_gen.fillna(0, inplace=True)

    # additions 
    for idx_action in idx_action_dfs:
        df_summary_ooi_gen = df_summary_ooi_gen.add(gen_ooi_metrics_action_df_list[idx_action], axis =0)
    df_summary_ooi_gen.fillna(0, inplace=True)

    # now calculate average dwelltime and average entropy 
    df_summary_ooi_gen['Average Dwelltime [ms]'] = sum(df_summary_ooi.loc['Total Dwelltime [ms]'])/df_summary_ooi_gen['Total Dwells']
    
    # calculate average stationary gaze entropy
 

    # calculate average gaze transition entropy
    

    return df_summary_ooi_gen