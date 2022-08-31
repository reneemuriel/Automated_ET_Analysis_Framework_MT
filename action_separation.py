import pandas as pd

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

    return df_actions

# separate dataframe ogd_data into actions for further calculations


# first try: separate ogd dataframe into new dataframes and calculate ooi_metrics

