import pandas as pd
import statistics

### calculations with cgom file
#region

# average fixation duration
def avg_fixation_duration_gen(data):
    return statistics.fmean(data['Event Duration [ms]'])


# number of fixations
def tot_fixations_gen(data):
    return (len(data))

#endregion


### calculations with saccade information
#region



#endregion


# general metrics

def calculate_general_metrics(ooi, data):
    
    avg_fixation_duration = avg_fixation_duration_gen(data)
    
    tot_fixations = tot_fixations_gen(data)

    