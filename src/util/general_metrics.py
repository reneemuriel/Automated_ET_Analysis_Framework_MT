'''
Calculation of metrics of general analysis
'''

from numpy import fix
import pandas as pd
import statistics
import re
from pathlib import Path


### calculations with fixation (cgom) file
#region

# average fixation duration
def avg_fixation_duration_gen(fixationdata):
    return statistics.mean(fixationdata['Event Duration [ms]'])

# number of fixations
def tot_fixations_gen(fixationdata):
    return (len(fixationdata))

# total duration
def tot_duration_gen(fixationdata):
    return fixationdata.iloc[-1]['Event End Trial Time [ms]']
        
# time to first fixation
def first_fixation_gen(fixationdata):
    return fixationdata.iloc[1]['Event Start Trial Time [ms]']

# total fixation duration
def tot_fixation_duration(fixationdata):
    return sum(fixationdata['Event Duration [ms]'])

#endregion

### calculations with saccade file
#region

# average saccade duration
def avg_saccade_duration_gen(saccadedata):
    return statistics.mean(saccadedata['Event Duration [ms]'])

# number of saccades
def tot_saccades_gen(saccadedata):
    return len(saccadedata)

def tot_saccade_duration(saccadedata):
    return sum(saccadedata['Event Duration [ms]'])

#endregion

### calculations with both files
#region

# fixation saccade time ratio
def fix_sac_ratio(fixationdata, saccadedata):
    tot_fix = sum(fixationdata['Event Duration [ms]'])
    tot_sac = sum(saccadedata['Event Duration [ms]'])

    percent_fix = round(tot_fix / (tot_fix + tot_sac) * 100)
    percent_sac = round(tot_sac / (tot_fix + tot_sac) * 100)

    percentages = '{}/{}'.format(round(percent_fix), round(percent_sac))
    #ratio_as_string = '{}:{}'.format(round(percent_fix), round(percent_sac)) # does not work since excel converts it to time format
    
    return percentages

#endregion

def calculate_general_metrics(fixationdata, saccadedata, trialname):
    
    df_general_metrics = pd.DataFrame()

    # average fixation duration 
    df_general_metrics['Average Fixation Duration [ms]'] = [avg_fixation_duration_gen(fixationdata)]

    # number of fixations
    df_general_metrics['Number of Fixations'] = [tot_fixations_gen(fixationdata)]

    # total fixation duration
    df_general_metrics['Total Fixation Duration [ms]'] = [tot_fixation_duration(fixationdata)]

    # total duration of the trial (maybe divide by 1000 to get seconds)
    df_general_metrics['Total Duration [ms]'] = [tot_duration_gen(fixationdata)]  #/1000

    # time to first fixation 
    #df_general_metrics['Time to First Fixation [ms]'] = [first_fixation_gen(fixationdata)]

    # average saccade duration
    df_general_metrics['Average Saccade Duration [ms]'] = [avg_saccade_duration_gen(saccadedata)]

    # number of saccades
    df_general_metrics['Number of Saccades'] = [tot_saccades_gen(saccadedata)]

    # total saccade duration
    df_general_metrics['Total Saccade Duration [ms]'] = [tot_saccade_duration(saccadedata)]

    # fixation/saccade ratio (percent)
    df_general_metrics['Relative Fixation/Saccade Duration [%]'] = [fix_sac_ratio(fixationdata, saccadedata)]

    df_general_metrics.index = [trialname]

    return df_general_metrics

def calculate_general_metrics_per_action(fixationdata, saccadedata, trialname):
     
    df_general_metrics = pd.DataFrame()

    # average fixation duration 
    df_general_metrics['Average Fixation Duration [ms]'] = [avg_fixation_duration_gen(fixationdata)]

    # number of fixations
    df_general_metrics['Number of Fixations'] = [tot_fixations_gen(fixationdata)]

    # total duration of the trial (maybe later: divide by 1000 to get seconds)
    df_general_metrics['Total Duration [ms]'] = [tot_duration_gen(fixationdata)]

    # total fixation duration
    df_general_metrics['Total Fixation Duration [ms]'] = [tot_fixation_duration(fixationdata)]


    # time to first fixation 
    #df_general_metrics['Time to First Fixation [ms]'] = [first_fixation_gen(fixationdata)]

    # average saccade duration
    df_general_metrics['Average Saccade Duration [ms]'] = [avg_saccade_duration_gen(saccadedata)]

    # number of saccades
    df_general_metrics['Number of Saccades'] = [tot_saccades_gen(saccadedata)]

    # total saccade duration
    df_general_metrics['Total Saccade Duration [ms]'] = [tot_saccade_duration(saccadedata)]

    # fixation/saccade ratio (percent)
    df_general_metrics['Relative Fixation/Saccade Duration [%]'] = [fix_sac_ratio(fixationdata, saccadedata)]

    df_general_metrics.index = [trialname]

    return df_general_metrics   

def summary_general_analysis(df_list, spec, save_path, action):
           
    # concatenate all dfs 
    df_summary = pd.concat(df_list)
    # add mean to all columns
    df_summary.loc['Mean {}'.format(spec)] = df_summary.mean()
    # add standard deviation to all columns
    df_summary.loc['Standard Deviation {}'.format(spec)] = df_summary.iloc[0:-1].std()
    
    ### add mean and standard deviation of relative percentages of fixation/saccade duration
    
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
    
    # calculate standard deviation (in percent) and add to df / if only 1 sample, stdev = 0
    if len(df_list) == 1:
        perc_fixation_stdv = 0
    else:
        perc_fixation_stdv = round(statistics.stdev(perc_fixation_list))

    stdv_ratio_string = '{}'.format(perc_fixation_stdv)
    df_summary.at['Standard Deviation {}'.format(spec),'Relative Fixation/Saccade Duration [%]'] = stdv_ratio_string # replace nan with calculated value

    # save dataframe per participant
    df_summary.to_csv(save_path / Path('{}_summary_general_analysis_{}.csv'.format(spec, action)))

    return df_summary




    