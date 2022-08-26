import pandas as pd
import statistics
import math


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


### calculate total dwell time/fixation time per OOI of entire trial
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


### calculate average dwell time per OOI of entire trial (only one single OOI per fixation)
def avg_dwell_time_ooi(data, all_ooi):
    
    global df_dwelltime

    # create dataframe to fill with dwell times (one row per dwell time in respective columns, rest is filled with zeroes)
    dwelltimes = pd.DataFrame(columns= all_ooi + ['Non-OOI']) 
    dwelltimes.loc[len(dwelltimes)] = 0

    k=0
    for row in range (1, len(data)): # row by row through df
        if data.fixation_object[row] == data.fixation_object[row-1]: # if same fixation obj in row before
            
            # current dwelltime = new fixation from last row + current dwelltime
            fix_object = data.fixation_object[row] 
            dwelltimes[fix_object][k] =   data.fixation_time[row-1] + dwelltimes[fix_object][k]

            # if the next fix object is not the same 
            # or if it is the last row
            # then add current fix time and end dwell here by changing k
            if row == (len(data)-1):
                dwelltimes[fix_object][k] = data.fixation_time[row] + dwelltimes[fix_object][k] # add fixation time from current row
                # add empty row to df
                dwelltimes.loc[len(dwelltimes)] = 0
                # add 1 to counter so that next row can be used in df_dwell_time
                k=k+1
            elif data.fixation_object[row] != data.fixation_object[row+1]:
                dwelltimes[fix_object][k] = data.fixation_time[row] + dwelltimes[fix_object][k] # add fixation time from current row
                # add empty row to df
                dwelltimes.loc[len(dwelltimes)] = 0
                # add 1 to counter so that next row can be used in df_dwell_tme
                k=k+1

    df_dwelltime = pd.DataFrame(columns=all_ooi) # do not include Non-OOI
    df_dwelltime.loc[len(df_dwelltime)] = 0 # add new row

    for ooi in all_ooi:
        a = dwelltimes[ooi].values
        a = a[a!=0]
        a = a.tolist()
        df_dwelltime[ooi]= [a]

    df_dwelltime.loc[len(df_dwelltime)] = 0 # add new row
    for ooi in all_ooi:
        df_dwelltime[ooi][1] = statistics.mean(df_dwelltime[ooi][0])

    return df_dwelltime.iloc[1]


### calculate number of revisits per OOI (with df_dwelltime from previous function)
def revisits_per_ooi(df_dwelltime, all_ooi):
    
    global revisits

    revisits = []
    for ooi in all_ooi:
        revisits.append(len(df_dwelltime.iloc[0][ooi]))
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
def rel_dwell_time_ooi(tot_fixation_time):
    rel_dwell_time = []
    for fix_time_ooi in tot_fixation_time:
        rel_dwell_time.append(fix_time_ooi/sum(tot_fixation_time)*100)
    a = sum(rel_dwell_time)
    return rel_dwell_time



#endregion


def calculate_ooi_metrics(data: pd.DataFrame, all_ooi: list) -> pd.DataFrame:
    '''
    description
    '''
    # fill df_ooi_metrics with all the metrics per ooi: 
    #   hits per OOI
    #   total dwell time per OOI
    #   average dwell time per OOI
    #   number of revisits per OOI
    #   average fixation time per OOI
    #   time to first fixation per OOI

    df_ooi_metrics = pd.DataFrame(columns=all_ooi)


    # count total hits per OOI & add to df_ooi_metrics
    df_ooi_metrics.loc[len(df_ooi_metrics)] = count_hits_ooi(data, all_ooi)


    # calculate total dwell/fixation time per OOI & add to df_ooi_metrics
    df_ooi_metrics.loc[len(df_ooi_metrics)] = tot_fixation_time_ooi(data, all_ooi)


    # calculate average dwell time per OOI & add to df_ooi_metrics
    df_ooi_metrics.loc[len(df_ooi_metrics)] = avg_dwell_time_ooi(data, all_ooi)


    # calculate number of revisits per OOI & add to df_ooi_metrics
    df_ooi_metrics.loc[len(df_ooi_metrics)] = revisits_per_ooi(df_dwelltime, all_ooi)


    # calculate average fixation time per OOI & add to df_ooi_metrics
    df_ooi_metrics.loc[len(df_ooi_metrics)] = avg_fixation_time_ooi(data, all_ooi)


    # calculate time to first fixation per OOI & add to df_ooi_metrics
    df_ooi_metrics.loc[len(df_ooi_metrics)] = first_fixation_ooi(data, all_ooi)


    # calculate relative dwell time per OOI (percent) & add to df_ooi_metrics
    df_ooi_metrics.loc[len(df_ooi_metrics)] = rel_dwell_time_ooi(tot_fixation_time)

    # name rows of df
    df_ooi_metrics.index = ['Hits', 'Total Fixation Time [s]', 'Average Dwelltime [s]', 'Revisits', 'Average Fixation Time [s]', 'Time to First Fixation [s]', 'Relative Dwelltime [%]']


    return df_ooi_metrics


### CALCULATION OF GENERAL OOI-BASED METRICS
#region

# calculate average dwell time (with df_dwelltime)
def avg_dwell_time(all_ooi):
    all_dwell_times = []
    for i in range(len(all_ooi)):
        for j in range (len(df_dwelltime.iloc[0][i])):
            all_dwell_times.append((df_dwelltime.iloc[0][i][j]))
    return statistics.mean(all_dwell_times)



# calculate total hits (with df_hits)
def tot_hits():
    return sum(hits)


# calculate total dwells (with revisits)
def tot_dwells(revisits_per_ooi):
    return sum(revisits_per_ooi)


# calculate stationary gaze entropy (inclusive Non-OOI / BG)
def stationary_gaze_entropy(all_ooi, data):

    global proportions # for tge calculation

    hits_with_BG = []
    all_ooi_BG = all_ooi + ['Non-OOI']
    
    # calculate hits per OOI, inclusive Non-OOI/BG
    for ooi in all_ooi_BG:
        hits_with_BG.append(sum(x.count(ooi) for x in data['fixation_object']))
    
    # calculate proportion of hits (stationary distribution values)
    proportions = []
    for i in range(len(hits_with_BG)):
        proportions.append(hits_with_BG[i]/sum(hits_with_BG))
    
    # stationary gaze entropy (Shannon's equation)
    sge_list = []
    i=0
    for i in range(len(all_ooi_BG)): #only here -1, because non-ooi is in there
        if proportions[i] == 0:
            sge_list.append(0)
        else:
            sge_list.append(proportions[i] * math.log2(proportions[i]))
    sge = -sum(sge_list)

    # normalize sge with maxmimum entropy
    max_entropy = math.log2(len(all_ooi_BG))
    sge_normalised = sge / max_entropy
    return sge_normalised # 1 = max entropy, 0 = minimum entropy


# calculate transition gaze entropy (inclusive Non-OOI / BG)
def transition_gaze_entropy(all_ooi, data):
     
    def transition_matrix(transitions, number_of_states):

        # from https://gist.github.com/tg12/d7efa579ceee4afbeaec97eb442a6b72 

        #the following code takes a list such as
        #[1,1,2,6,8,5,5,7,8,8,1,1,4,5,5,0,0,0,1,1,4,4,5,1,3,3,4,5,4,1,1]
        #with states labeled as successive integers starting with 0
        #and returns a transition matrix, M,
        #where M[i][j] is the probability of transitioning from i to j

        M = [[0]*number_of_states for _ in range(number_of_states)]

        for (i,j) in zip(transitions,transitions[1:]):
            M[i][j] += 1

        #now convert to probabilities:
        for row in M:
            s = sum(row)
            if s > 0:
                row[:] = [f/s for f in row]
        return M
    
    # add
    all_ooi_BG = all_ooi + ['Non-OOI']

    # number of states as input for transition_matrix()
    number_of_states= len(data['fixation_object'].unique())

    # convert fixation_object list to list of numbers as input for transition_matrix()
    transitions = data['fixation_object'].to_list()
    dict_ooi = {k: v for v, k in enumerate(all_ooi_BG)}
    transitions_series = (pd.Series(transitions)).map(dict_ooi)
    transitions_list = transitions_series.to_list()

    # calculate matrix m
    m = transition_matrix(transitions_list, number_of_states)
    #for row in m: print(' '.join('{0:.2f}'.format(x) for x in row))

    # create new matrix with same size as m
    n= len(data['fixation_object'].unique())
    m2 = [[0]*n for _ in range(n)]

    # multiply each value in the matrix by its log and fill in new matrix
    i=0
    j=0
    for i in range (len(all_ooi_BG)):
        for j in range(len(all_ooi_BG)):
            if m[i][j] <= 0.0001: # or = 0 ?
                m2[i][j] = 0
            else:
                m2[i][j] = math.log2(m[i][j]) * m[i][j]

    # conduct inner summation (each row) and multiply by stationary distribution value (from sge)
    inner_summation = []
    for i in range(len(all_ooi_BG)):
        inner_summation.append(sum(m2[i][:])*proportions[0])

    # conduct outer summation (sum of all inner summations) and negative
    outer_summation = sum(inner_summation)
    tge = -outer_summation
    
    # normalize stge with maxmimum entropy
    max_entropy = math.log2(len(all_ooi_BG))
    tge_normalised = tge / max_entropy
    return tge_normalised 
    # 1 = max entropy, 0 = minimum entropy







def calculate_general_ooi_metrics(data, all_ooi, trialname):
    
    df_general_ooi_metrics = pd.DataFrame()

    # calculate average dwell time 
    df_general_ooi_metrics['Average Dwell Time [s]'] = [avg_dwell_time(all_ooi)]
    
    # calculate total hits
    df_general_ooi_metrics['Total Hits'] = [tot_hits()]
    
    # calculate total dwells 
    df_general_ooi_metrics['Total Dwells'] = [tot_dwells(revisits)]

    # calculate stationary gaze entropy 
    df_general_ooi_metrics['Normalised Stationary Gaze Entropy'] = [stationary_gaze_entropy(all_ooi, data)]

    # calculate transition gaze entropy
    df_general_ooi_metrics['Normalised Transition Gaze Entropy'] = [transition_gaze_entropy(all_ooi, data)]

    df_general_ooi_metrics.index = [trialname]

    return df_general_ooi_metrics

    e=2

#endregion