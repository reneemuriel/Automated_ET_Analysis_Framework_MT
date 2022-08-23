import pandas as pd
import statistics

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




#endregion


### calculations with saccade file
#region

# average saccade duration
def avg_saccade_duration_gen(saccadedata):
    return statistics.mean(saccadedata['Event Duration [ms]'])

# number of saccades
def tot_saccades_gen(saccadedata):
    return len(saccadedata)


#endregion


### calculations with both files
#region

# fixation saccade time ratio
def fix_sac_ratio(fixationdata, saccadedata):
    tot_fix = sum(fixationdata['Event Duration [ms]'])
    tot_sac = sum(saccadedata['Event Duration [ms]'])
    percent_fix = tot_fix / (tot_fix + tot_sac) * 100
    percent_sac = tot_sac / (tot_fix + tot_sac) * 100
    percentages = '{}/{}'.format(round(percent_fix), round(percent_sac))
    #ratio_a_string = '{}:{}'.format(round(percent_fix), round(percent_sac))
    
    return percentages


#endregion


def calculate_general_metrics(fixationdata, saccadedata, trialname):
    
    df_general_metrics = pd.DataFrame()

    # average fixation duration
    df_general_metrics['Average Fixation Duration [ms]'] = [avg_fixation_duration_gen(fixationdata)]

    # number of fixations
    df_general_metrics['Total Number of Fixations [ms]'] = [tot_fixations_gen(fixationdata)]

    # total duration of the trial
    df_general_metrics['Total Duration [ms]'] = tot_duration_gen(fixationdata)

    # time to first fixation 
    df_general_metrics['Time to First Fixation [ms]'] = first_fixation_gen(fixationdata)

    # average saccade duration
    df_general_metrics['Average Saccade Duration [ms]'] = avg_saccade_duration_gen(saccadedata)

    # number of saccades
    df_general_metrics['Number of Saccades'] = tot_saccades_gen(saccadedata)

    # fixation/saccade ratio (percent)
    df_general_metrics['Relative Fixation/Saccade Time [%]'] = fix_sac_ratio(fixationdata, saccadedata)

    df_general_metrics.index = [trialname]

    return df_general_metrics






    







    