import pandas as pd
import statistics
import re
from pathlib import Path

def summary_general_analysis(df_list, spec, save_path, action):
           
    # concatenate all dfs 
    df_summary = pd.concat(df_list)
    # add mean to all columns
    df_summary.loc['Mean {}'.format(spec)] = df_summary.mean()
    # add standard deviation to all columns
    df_summary.loc['Standard Deviation {}'.format(spec)] = df_summary.iloc[0:-1].std()
    
    ### manually add mean and standard deviation of relative percentages of fixation/saccade duration
    
    # extract numbers 
    perc_fixation_list = []
    perc_saccade_list = []
    for row in range(len(df_summary)-2):
        perc_string = df_summary['Relative Fixation/Saccade Duration [%]'][row] # extract numbers from string
        temp = re.findall(r'\d+', perc_string)
        perc_list = list(map(int, temp))
        perc_fixation_list.append(perc_list[0]) # extract fix percentage
        perc_saccade_list.append(perc_list[1])  # extract saccade percentage
    
    # calculate mean and add to df
    perc_fixation_mean = statistics.mean(perc_fixation_list)
    perc_saccade_mean = 100 - perc_fixation_mean
    mean_ratio_string = '{}/{}'.format(round(perc_fixation_mean), round(perc_saccade_mean))
    df_summary.at['Mean {}'.format(spec),'Relative Fixation/Saccade Duration [%]'] = mean_ratio_string # replace nan with calculated value
    
    # calculate standard deviation (in percent) and add to df
    perc_fixation_stdv = round(statistics.stdev(perc_fixation_list))
    stdv_ratio_string = '{}'.format(perc_fixation_stdv)
    df_summary.at['Standard Deviation {}'.format(spec),'Relative Fixation/Saccade Duration [%]'] = stdv_ratio_string # replace nan with calculated value

    # save dataframe per participant
    df_summary.to_csv(save_path / Path('{}_summary_general_analysis_{}.csv'.format(spec, action)))

    return df_summary




def summary_ooi_analysis(df_list, spec, save_path, action):
    # calculate mean of all ellements of dfs and store them in new df
    df_summary_means = pd.concat(df_list).groupby(level=0).mean()
    # rename indeces: add 'Mean' to all indeces
    df_summary_means_prefix = df_summary_means.T.add_prefix('Mean ').T

    # calculate stdev of all ellements of dfs and store them in new df
    df_summary_stdev = pd.concat(df_list).groupby(level=0).std()
    # rename indeces: add 'Standard Deviation' to all indeces
    df_summary_stdev = df_summary_stdev.T.add_prefix('Standard Deviation ').T

    # combine the two dfs
    df_summary = pd.concat([df_summary_means_prefix, df_summary_stdev])

    # save dataframe per participant
    df_summary.to_csv(save_path / Path('{}_summary_ooi_analysis_{}.csv'.format(spec, action)))

    # also return mean df (without prefix) for further calculation of 
    return df_summary, df_summary_means


def summary_ooigen_analysis(df_list, spec, save_path, action):
    e=2

    # concatenate all dfs 
    df_summary = pd.concat(df_list)
    # add mean to all columns
    df_summary.loc['Mean {}'.format(spec)] = df_summary.mean()
    # add standard deviation to all columns
    df_summary.loc['Standard Deviation {}'.format(spec)] = df_summary.iloc[0:-1].std()
    # save dataframe 
    df_summary.to_csv(save_path / Path('{}_summary_ooi-based_general_analysis_{}.csv'.format(spec, action)))
    
    return df_summary