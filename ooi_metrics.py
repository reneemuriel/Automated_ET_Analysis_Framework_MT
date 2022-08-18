import pandas as pd
import statistics


### CALCULATION OF OOI-BASED METRICS
#region

### count total hits per ooi of entire trial
def count_hits_ooi(data, all_ooi_fun):
    """ counting all hits per OOI from the ogdhar_final file"""
    global hits
    hits = []
    for ooi in all_ooi_fun:
        hits.append(sum(x.count(ooi) for x in data['fixation_object']))
    return hits


### calculate total dwell time/fixation time per OOI of entire trial
def tot_fixation_time_ooi(data, all_ooi_fun):
    global tot_fixation_time
    tot_fixation_time = [0]*len(all_ooi_fun)
    i=0
    for ooi in all_ooi_fun:
        for row in range(0,len(data)):
            if ooi in data.iloc[row]['fixation_object']:
                tot_fixation_time[i] = tot_fixation_time[i] + data.iloc[row]['fixation_time']
        i=i+1
    return tot_fixation_time   


### calculate average dwell time per OOI of entire trial (only one single OOI per fixation)
def avg_dwell_time_ooi(data, all_ooi_fun):
    
    global df_dwelltime

    # create dataframe to fill with dwell times (one row per dwell time in respective columns, rest is filled with zeroes)
    dwelltimes = pd.DataFrame(columns= all_ooi_fun + ['Non-OOI']) 
    dwelltimes.loc[len(dwelltimes)] = 0

    k=0
    for row in range (1, len(data)): # row by row through df
        if data.fixation_object[row] == data.fixation_object[row-1]: # if same fixation obj in row before
            
            # current dwelltime = new fixation from last row + current dwelltime
            fix_object = data.fixation_object[row] 
            dwelltimes[fix_object][k] =   data.fixation_time[row-1] + dwelltimes[fix_object][k]

            # if the next fix object is not the same, add current fix time and end dwell here by changing k
            if data.fixation_object[row] != data.fixation_object[row+1]:
                dwelltimes[fix_object][k] = data.fixation_time[row] + dwelltimes[fix_object][k] # add fixation time from current row
                # add empty row to df
                dwelltimes.loc[len(dwelltimes)] = 0
                # add 1 to counter so that next row can be used in df_dwell_tme
                k=k+1

    df_dwelltime = pd.DataFrame(columns=all_ooi_fun) # do not include Non-OOI
    df_dwelltime.loc[len(df_dwelltime)] = 0 # add new row

    for ooi in all_ooi_fun:
        a = dwelltimes[ooi].values
        a = a[a!=0]
        a = a.tolist()
        df_dwelltime[ooi]= [a]

    df_dwelltime.loc[len(df_dwelltime)] = 0 # add new row
    for ooi in all_ooi_fun:
        df_dwelltime[ooi][1] = statistics.fmean(df_dwelltime[ooi][0])

    return df_dwelltime.iloc[1]


### calculate number of revisits per OOI (with df_dwelltime from previous function)
def revisits_per_ooi(df_dwelltime_fun, all_ooi_fun):
    
    global revisits

    revisits = []
    for ooi in all_ooi_fun:
        revisits.append(len(df_dwelltime_fun.iloc[0][ooi]))
    return revisits


### calculate average fixation time 
def avg_fixation_time_ooi(data, all_ooi_fun):

    global df_fixationtime

    # fixation time list per OOI
    df_fixationtime = pd.DataFrame(columns=all_ooi_fun) 
    df_fixationtime.loc[len(df_fixationtime)] = 0

    i=0
    for ooi in all_ooi_fun: 
        fixation_times_list = []
        for row in range(0,len(data)):
            if ooi == data.iloc[row]['fixation_object']:
                fixation_times_list.append(data.iloc[row]['fixation_time'])  
        df_fixationtime[ooi] = [fixation_times_list]
        i=i+1

    # average fixation time per OOI
    df_fixationtime.loc[len(df_fixationtime)] = 0 # add new row
    for ooi in all_ooi_fun:
        df_fixationtime[ooi][1] = statistics.fmean(df_fixationtime[ooi][0])

    return df_fixationtime.iloc[1]


# calculate time to first fixation per OOI
def first_fixation_ooi(data, all_ooi_fun):
    first_fixation = []
    for ooi in all_ooi_fun:
        idx_first_fixation = (data['fixation_object'] == ooi).idxmax()
        first_fixation.append(data.iloc[idx_first_fixation]['start_time'])
    
    return first_fixation



# calculate relative dwell time per OOI in percent (with dwelltime from previous function)
def rel_dwell_time_ooi(tot_fixation_time_fun):
    rel_dwell_time = []
    for fix_time_ooi in tot_fixation_time:
        rel_dwell_time.append(fix_time_ooi/sum(tot_fixation_time_fun)*100)
    a = sum(rel_dwell_time)
    return rel_dwell_time



#endregion


def calculate_ooi_metrics(data, all_ooi):
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


    return df_ooi_metrics


### CALCULATION OF GENERAL OOI-BASED METRICS
#region

# calculate average dwell time (with df_dwelltime)
def avg_dwell_time(all_ooi):
    all_dwell_times = []
    for i in range(len(all_ooi)):
        for j in range (len(df_dwelltime.iloc[0][i])):
            all_dwell_times.append((df_dwelltime.iloc[0][i][j]))
    return statistics.fmean(all_dwell_times)



# calculate total hits (with df_hits)
def tot_hits():
    return sum(hits)


# calculate total dwells (with revisits)
def tot_dwells(revisits_per_ooi_fun):
    return sum(revisits_per_ooi_fun)


# calculate 





def calculate_general_ooi_metrics(data, all_ooi):
    
    # calculate average dwell time 
    average_dwell_time = avg_dwell_time(all_ooi)


    # calculate total hits
    total_hits = tot_hits()


    # calculate total dwells 
    total_dwells = tot_dwells(revisits)


    # calculate entropy 
    # muchos fön

    e=9


#endregion