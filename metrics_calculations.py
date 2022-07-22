# count total hits per ooi of entire trial
def count_hits_per_ooi(all_ooi, fixation_objects):
    """ counting all hits per OOI from the OGD file"""
    hits = []
    for ooi in all_ooi:
        hits.append(sum(x.count(ooi) for x in fixation_objects))
        # df_hits.loc[len(df)] = hits
    return hits


# count hits per ooi per step



# calculate total dwell time per OOI of entire trial
# via the fixation_object and fixation_time column (can be improved)
def calculate_dwell_time(data, all_ooi):
    global dwell_time
    dwell_time = [0]*len(all_ooi)
    i=0
    for ooi in all_ooi:
        for row in range(0,len(data)):
            if ooi in data.iloc[row]['fixation_object']:
                dwell_time[i] = dwell_time[i] + data.iloc[row]['fixation_time']


# calculate total dwell time per OOI per step


# calculate average dwell time per OOI of entire trial


# calculate average dwell time per OOI per step