from glob import glob
import pandas as pd
import statistics
import math
import numpy as np
from pathlib import Path
import re

from src.util import add_columns as ac


### PREPARE OGD FILE
#region

def prepare_ogd_file(ogd_data, pixel_distance):

    global all_ooi
    
    # drop columns with any NaN values (don't know why they occur sometimes)
    ogd_data.dropna(inplace=True)
    ogd_data.reset_index(drop=True, inplace=True) 

    # turn [s] into [ms] for simplicity and change it back for output again (?)
    ogd_data['start_time'] = ogd_data['start_time']*1000
    ogd_data['end_time'] = ogd_data['end_time'] * 1000

    # rename last column to 'action' if it is named 'Action'
    if ogd_data.columns[-1] == 'Action':
        ogd_data.rename(columns={ogd_data.columns[-1]: 'action'}, inplace=True)
    
    # add columns
    ogd_final = ogd_data

    # if last column is action, call ac.add_fixation_object_action()
    if ogd_final.columns[-1] == 'action':
        ac.add_fixation_object_action(ogd_final,pixel_distance)
    # otherwise, call ac.add_fixation_object()
    else:
        ac.add_fixation_object(ogd_final,pixel_distance)
    
    return ogd_final


def extract_oois(ogd_data):
    # extract oois from ogd_data
    if ogd_data.columns.values[-1] == 'action' or ogd_data.columns.values[-1] == 'Action':
    # format: start_time, end_time, OOI_1, OOI_2, OOI_3, action
        all_ooi = ogd_data.columns.values.tolist()[2:-1]
    else:
        # format: start_time, end_time, OOI_1, OOI_2, OOI_3
        all_ooi = ogd_data.columns.values.tolist()[2:]
    
    return all_ooi


#endregion



### CALCULATION OF OOI-BASED METRICS
#region

### count total hits per ooi of entire trial
def count_hits_ooi(data, all_ooi):
    """ counting all hits per OOI from the ogdhar_final file"""
    global hits
    hits = []
    for ooi in all_ooi:
        hits.append(sum(x.count(ooi) for x in data['fixation_object']))
    return hits


### calculate fixation time per OOI of entire trial
def tot_fixation_time_ooi(data, all_ooi):
    global tot_fixation_time
    tot_fixation_time = [0]*len(all_ooi)
    i=0
    for ooi in all_ooi:
        for row in range(0,len(data)):
            if ooi in data.iloc[row]['fixation_object']:
                tot_fixation_time[i] = tot_fixation_time[i] + data.iloc[row]['fixation_time']
        i=i+1
    return tot_fixation_time   


### calculate average dwell time per OOI of entire trial 
def avg_dwell_time_ooi(data, all_ooi):
    
    global df_dwelltime

    # create df to fill in dwelltimes
    cols = all_ooi + ['BG']
    #cols.append('BG') 
    dwelltimes = pd.DataFrame(columns=cols) 
    dwelltimes.loc[len(dwelltimes)] = 0

    k=0
    start_dwell_row = 0
    for row in range (0, len(data)): # row by row through df

        fix_object = data.fixation_object[row] 
        
        # if we're in last row, calculate dwell time from start_dwell_row to current row
        if row == (len(data)-1):
            dwelltimes[fix_object][k] = data.end_time[row] - data.start_time[start_dwell_row]


        # if next fix obj is different, calculate dwell from start_dwell_row to current row
        # and change start_dwell_row to next row
        elif data.fixation_object[row] != data.fixation_object[row+1]:
            dwelltimes[fix_object][k] = data.end_time[row] - data.start_time[start_dwell_row]
            # add 1 to counter so that next row can be used in df_dwell_tme
            k=k+1
            # add empty row to df
            dwelltimes.loc[len(dwelltimes)] = 0
            # and change start_dwell_row to next row
            start_dwell_row = row+1


    df_dwelltime = pd.DataFrame(columns=all_ooi) # do not include BG
    df_dwelltime.loc[len(df_dwelltime)] = 0 # add new row

    for ooi in all_ooi:
        a = dwelltimes[ooi].values
        a = a[a!=0]
        a = a.tolist()
        # if list is empty (no dwells for this ooi), fill it with a zero for the calculation of the mean 
        if not a:
            a=[0]
        df_dwelltime[ooi]= [a]

    df_dwelltime.loc[len(df_dwelltime)] = 0 # add new row
    for ooi in all_ooi:
        df_dwelltime[ooi][1] = statistics.mean(df_dwelltime[ooi][0])

    e=2

    return df_dwelltime.iloc[1]


### calculate total dwell time per OOI of entire trial
def total_dwell_time(df_dwelltime, all_ooi):
    global tot_dwell_time
    tot_dwell_time = []
    for ooi in all_ooi:
        tot_dwell_time.append(sum(df_dwelltime[ooi][0]))
    return tot_dwell_time   

### calculate number of revisits per OOI (with df_dwelltime from previous function)
def revisits_per_ooi(df_dwelltime, all_ooi):
    
    global revisits

    revisits = []
    for ooi in all_ooi:
        # exception for 0, since otherwise it counts 1 revisit despite it being 0
        if df_dwelltime[ooi][0] == [0]:
            revisits.append(0)  
        else:
            revisits.append(len(df_dwelltime[ooi][0]))
    return revisits


### calculate average fixation time 
def avg_fixation_time_ooi(data, all_ooi):

    global df_fixationtime

    # fixation time list per OOI
    df_fixationtime = pd.DataFrame(columns=all_ooi) 
    df_fixationtime.loc[len(df_fixationtime)] = 0

    i=0
    for ooi in all_ooi: 
        fixation_times_list = []
        for row in range(0,len(data)):
            if ooi == data.iloc[row]['fixation_object']:
                fixation_times_list.append(data.iloc[row]['fixation_time'])  
        # if list is empty (no fixation on this ooi) add 0 to list
        if not fixation_times_list:
            fixation_times_list = [0]
        df_fixationtime[ooi] = [fixation_times_list]
        i=i+1

    # average fixation time per OOI
    df_fixationtime.loc[len(df_fixationtime)] = 0 # add new row
    for ooi in all_ooi:
        df_fixationtime[ooi][1] = statistics.mean(df_fixationtime[ooi][0])

    return df_fixationtime.iloc[1]


# calculate time to first fixation per OOI
def first_fixation_ooi(data, all_ooi):
    first_fixation = []
    for ooi in all_ooi:
        idx_first_fixation = (data['fixation_object'] == ooi).idxmax()
        first_fixation.append(data.iloc[idx_first_fixation]['start_time'])
    
    return first_fixation



# calculate relative dwell time per OOI in percent (with dwelltime from previous function)
def rel_dwell_time_ooi(tot_dwell_time):
    rel_dwell_time = []
    # if total dwell time = 0, revisits for each ooi = 0 (happens in certain steps)
    if sum(tot_dwell_time) == 0:
        rel_dwell_time = 0*len(tot_dwell_time)
    else:
        for dwell_time_ooi in tot_dwell_time:
            rel_dwell_time.append(dwell_time_ooi/sum(tot_dwell_time)*100)
    return rel_dwell_time



def calculate_ooi_metrics(data: pd.DataFrame, all_ooi: list) -> pd.DataFrame:
    '''
    description n
    '''
    # fill df_ooi_metrics with all the metrics per ooi: 
    #   hits per OOI
    #   total dwell time per OOI
    #   average dwell time per OOI
    #   number of revisits per OOI
    #   average fixation time per OOI
    #   time to first fixation per OOI

    df_ooi_metrics = pd.DataFrame(columns=all_ooi, dtype=float)


    # count total hits per OOI & add to df_ooi_metrics
    df_ooi_metrics.loc[len(df_ooi_metrics)] = count_hits_ooi(data, all_ooi)


    # calculate total fixation time per OOI & add to df_ooi_metrics
    df_ooi_metrics.loc[len(df_ooi_metrics)] = tot_fixation_time_ooi(data, all_ooi)


    # calculate average dwell time per OOI & add to df_ooi_metrics
    df_ooi_metrics.loc[len(df_ooi_metrics)] = avg_dwell_time_ooi(data, all_ooi)


    # calculate total dwell time per OOI & add to df_ooi_metrics
    df_ooi_metrics.loc[len(df_ooi_metrics)] = total_dwell_time(df_dwelltime, all_ooi)


    # calculate number of revisits per OOI & add to df_ooi_metrics
    df_ooi_metrics.loc[len(df_ooi_metrics)] = revisits_per_ooi(df_dwelltime, all_ooi)


    # calculate average fixation time per OOI & add to df_ooi_metrics
    df_ooi_metrics.loc[len(df_ooi_metrics)] = avg_fixation_time_ooi(data, all_ooi)


    # calculate time to first fixation per OOI & add to df_ooi_metrics
    df_ooi_metrics.loc[len(df_ooi_metrics)] = first_fixation_ooi(data, all_ooi)


    # calculate relative dwell time per OOI (percent) & add to df_ooi_metrics
    df_ooi_metrics.loc[len(df_ooi_metrics)] = rel_dwell_time_ooi(tot_dwell_time)

    # name rows of df
    # maybe convert back to seconds?
    df_ooi_metrics.index = ['Hits', 'Total Fixation Time [ms]', 'Average Dwell Time [ms]', 'Total Dwell Time [ms]', 'Revisits', 'Average Fixation Time [ms]', 'Time to First Fixation [ms]', 'Relative Dwell Time [%]']


    return df_ooi_metrics


def calculate_ooi_metrics_per_action(data, all_ooi):
    
    df_ooi_metrics = pd.DataFrame(columns=all_ooi, dtype=float)


    # count total hits per OOI & add to df_ooi_metrics
    df_ooi_metrics.loc[len(df_ooi_metrics)] = count_hits_ooi(data, all_ooi)


    # calculate fixation time per OOI & add to df_ooi_metrics
    df_ooi_metrics.loc[len(df_ooi_metrics)] = tot_fixation_time_ooi(data, all_ooi)

    
    # calculate average dwell time per OOI & add to df_ooi_metrics
    df_ooi_metrics.loc[len(df_ooi_metrics)] = avg_dwell_time_ooi(data, all_ooi)

    
    # calculate total dwell time per OOI & add to df_ooi_metrics
    df_ooi_metrics.loc[len(df_ooi_metrics)] = total_dwell_time(df_dwelltime, all_ooi)


    # calculate number of revisits per OOI & add to df_ooi_metrics
    df_ooi_metrics.loc[len(df_ooi_metrics)] = revisits_per_ooi(df_dwelltime, all_ooi)


    # calculate average fixation time per OOI & add to df_ooi_metrics
    df_ooi_metrics.loc[len(df_ooi_metrics)] = avg_fixation_time_ooi(data, all_ooi)

    
    # calculate relative dwell time per OOI (percent) & add to df_ooi_metrics
    df_ooi_metrics.loc[len(df_ooi_metrics)] = rel_dwell_time_ooi(tot_dwell_time)

    # calculate time to first fixation per OOI & add to df_ooi_metrics
    # df_ooi_metrics.loc[len(df_ooi_metrics)] = first_fixation_ooi(data, all_ooi)


    # name rows of df
    # maybe convert back to seconds?
    df_ooi_metrics.index = ['Hits', 'Total Fixation Time [ms]', 'Average Dwell Time [ms]', 'Total Dwell Time [ms]', 'Revisits', 'Average Fixation Time [ms]', 'Relative Dwell Time [%]']


    return df_ooi_metrics

#endregion



### CALCULATION OF GENERAL OOI-BASED METRICS
#region

# calculate average dwell time (with df_dwelltime)
def avg_dwell_time(all_ooi):
    all_dwell_times_zeroes = []
    for i in range(len(all_ooi)):
        for j in range (len(df_dwelltime.iloc[0][i])):
            all_dwell_times_zeroes.append((df_dwelltime.iloc[0][i][j]))
    # remove zeroes from list, otherwise they are used to calculate mean
    all_dwell_times = [x for x in all_dwell_times_zeroes if x != 0]
    if sum(all_dwell_times) == 0:
        return 0
    else:
        return statistics.mean(all_dwell_times)


# calculate total hits (with df_hits)
def tot_hits():
    return sum(hits)

# calculate total dwells (with revisits)
def tot_dwells(revisits_per_ooi):
    total_dwelllls = sum(revisits_per_ooi)
    return sum(revisits_per_ooi)


# calculate stationary gaze entropy (inclusive BG / BG)
def stationary_gaze_entropy(all_ooi, data):

    global proportions # for tge calculation

    hits_with_BG = []
    all_ooi_BG = all_ooi + ['BG']
    
    # calculate hits per OOI, inclusive BG/BG
    for ooi in all_ooi_BG:
        hits_with_BG.append(sum(x.count(ooi) for x in data['fixation_object']))
    
    # calculate proportion of hits (stationary distribution values)
    proportions = []
    for i in range(len(hits_with_BG)):
        proportions.append(hits_with_BG[i]/sum(hits_with_BG))
    
    # stationary gaze entropy (Shannon's equation)
    sge_list = []
    i=0
    for i in range(len(all_ooi_BG)): #only here -1, because BG is in there
        if proportions[i] == 0:
            sge_list.append(0)
        else:
            sge_list.append(proportions[i] * math.log2(proportions[i]))
    sge = -sum(sge_list)

    # normalize sge with maxmimum entropy
    max_entropy = math.log2(len(all_ooi_BG))
    sge_normalised = sge / max_entropy
    return sge_normalised # 1 = max entropy, 0 = minimum entropy

# calculate transition gaze entropy (inclusive BG / BG)
def gaze_transition_entropy(all_ooi, data):

    # make transition matrix global variable so that it can be saved as ouput
    global transition_matrix
    global dict_ooi

    # add
    # all_ooi_BG = all_ooi + ['BG']

    # number of states as input for transition_matrix() -> only take objects that are looked at in this timeframe -> maybe change
    number_of_states = len(data['fixation_object'].unique())
    ooi_recognised = data['fixation_object'].unique()

    # convert fixation_object list to list of numbers as input for transition_matrix()
    transitions = data['fixation_object'].to_list()
    
    dict_ooi = {k: v for v, k in enumerate(ooi_recognised)}
    transitions_series = (pd.Series(transitions)).map(dict_ooi)
    transitions = transitions_series.to_list()


    # from https://gist.github.com/tg12/d7efa579ceee4afbeaec97eb442a6b72 

    #the following code takes a list such as
    #[1,1,2,6,8,5,5,7,8,8,1,1,4,5,5,0,0,0,1,1,4,4,5,1,3,3,4,5,4,1,1]
    #with states labeled as successive integers starting with 0
    #and returns a transition matrix, M,
    #where M[i][j] is the probability of transitioning from i to j

    # calculate matrix m
    transition_matrix = [[0]*number_of_states for _ in range(number_of_states)]

    for (x,y) in zip(transitions,transitions[1:]):
        transition_matrix[x][y] += 1

    #now convert to probabilities:
    for row in transition_matrix:
        s = sum(row)
        if s > 0:
            row[:] = [f/s for f in row]

    # create new matrix with same size as m
    n= len(data['fixation_object'].unique())
    m2 = [[0]*n for _ in range(n)]

    # multiply each value in the matrix by its log and fill in new matrix
    i=0
    j=0
    for i in range (len(ooi_recognised)):
        for j in range(len(ooi_recognised)):
            if transition_matrix[i][j] <= 0.0001: # or = 0 ?
                m2[i][j] = 0
            else:
                m2[i][j] = math.log2(transition_matrix[i][j]) * transition_matrix[i][j]

    # conduct inner summation (each row) and multiply by stationary distribution value (from sge)
    inner_summation = []
    for i in range(len(ooi_recognised)):
        inner_summation.append(sum(m2[i][:])*proportions[0])

    # conduct outer summation (sum of all inner summations) and negative
    outer_summation = sum(inner_summation)
    tge = -outer_summation
    
    # normalize stge with maxmimum entropy
    max_entropy = math.log2(len(ooi_recognised))
    if max_entropy == 0:    # only one ooi fixated in this action -> too little to calculate entropy?
        tge_normalised = np.nan    
    else: 
        tge_normalised = tge / max_entropy
    return tge_normalised 
# 1 = max entropy, 0 = minimum entropy







def calculate_general_ooi_metrics(data, all_ooi, trialname):
    
    df_general_ooi_metrics = pd.DataFrame(dtype=float)

    # calculate average dwell time 
    df_general_ooi_metrics['Average Dwell Time [ms]'] = [avg_dwell_time(all_ooi)]
    
    # calculate total hits
    df_general_ooi_metrics['Total Hits'] = [tot_hits()]
    
    # calculate total dwells 
    df_general_ooi_metrics['Total Dwells'] = [tot_dwells(revisits)]

    # calculate stationary gaze entropy 
    df_general_ooi_metrics['Normalised Stationary Gaze Entropy'] = [stationary_gaze_entropy(all_ooi, data)]

    # calculate transition gaze entropy
    df_general_ooi_metrics['Normalised Gaze Transition Entropy'] = [gaze_transition_entropy(all_ooi, data)]

    df_general_ooi_metrics.index = [trialname]

    return df_general_ooi_metrics, transition_matrix, dict_ooi

    e=2


def calculate_general_ooi_metrics_per_action(data, all_ooi, trialname):
    
    df_general_ooi_metrics = pd.DataFrame(dtype=float)

    # calculate average dwell time 
    df_general_ooi_metrics['Average Dwell Time [ms]'] = [avg_dwell_time(all_ooi)]
    
    # calculate total hits
    df_general_ooi_metrics['Total Hits'] = [tot_hits()]
    
    # calculate total dwells 
    df_general_ooi_metrics['Total Dwells'] = [tot_dwells(revisits)]

    # calculate stationary gaze entropy 
    df_general_ooi_metrics['Normalised Stationary Gaze Entropy'] = [stationary_gaze_entropy(all_ooi, data)]

    # calculate transition gaze entropy
    df_general_ooi_metrics['Normalised Gaze Transition Entropy'] = [gaze_transition_entropy(all_ooi, data)]

    df_general_ooi_metrics.index = [trialname]

    return df_general_ooi_metrics

    e=2


#endregion



### SUMMARY CALCULATIONS
#region

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

    #endregion