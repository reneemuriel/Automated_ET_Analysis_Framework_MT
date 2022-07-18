#### PYTHON SELFASSESSMENT V1 ####

# load packages
import pandas as pd
import seaborn as sns
from IPython.display import display
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import stats

### FUNCTIONS

# visualize with barplots
# hits
def visualize_hits():
    global fig_hits
    fig_hits = plt.figure(figsize=(8,8))
    sns.set_theme(style='whitegrid')
    plt.bar(df.columns, df.iloc[0], color='lightblue')
    plt.title('Hits per OOI', fontsize = 16)
    plt.ylabel('Number of hits', weight = 'bold')
    plt.xlabel('OOI', weight = 'bold')
    #plt.show()

# dwell_time
def visualize_dwelltime():
    global fig_dwelltime
    fig_dwelltime = plt.figure(figsize=(8,8))
    sns.set_theme(style='whitegrid')
    plt.bar(df.columns, df.iloc[1], color='lightblue')
    plt.title('Dwell time per OOI', fontsize = 16)
    plt.ylabel('Dwell time [s]', weight = 'bold')
    plt.xlabel('OOI', weight = 'bold')
    #plt.show()

# relative_dwell_time_ooi
def visualize_rel_dwelltime():
    global fig_rel_dwelltime
    fig_rel_dwelltime = plt.figure(figsize=(8,8))
    sns.set_theme(style='whitegrid')
    plt.bar(df.columns, df.iloc[2], color='lightblue')
    plt.title('Relative Dwell Time per OOI to total OOI fixation time in percent', fontsize = 16)
    plt.ylabel('Relative dwell time [%]', weight = 'bold')
    plt.xlabel('OOI', weight = 'bold')
    #plt.show()

# save all plots
def save_plots():
    fig_hits.savefig('Analysis/TrainData/fig_hits_{}px.png'.format(pixel_distance))
    fig_dwelltime.savefig('Analysis/TrainData/fig_dwelltime_{}px.png'.format(pixel_distance))
    fig_rel_dwelltime.savefig('Analysis/TrainData/fig_rel_dwelltime_{}px.png'.format(pixel_distance))



### DEFINE VARIABLES

# pixel distance for OOI hit (smaller or equal to)
pixel_distance = 0



### LOAD AND PREPARE DATA 

# read data
data = pd.read_csv('Data/TrainSet/Participant_Case1.txt', sep='\t')

# view data
# display(data)

# drop unnecessary columns
data.drop(columns = ['Action'], inplace = True) 

# create list of all OOIs
all_ooi = data.columns.values.tolist()[2:len(data)]

# add column to data that states the fixation object(s) of the fixation (question: can there be multiple OOI in one fixation? assumed: yes)
fixation_object = [] 
for row in range(0,len(data)):
    fixation_object.append([])                                  # make sublist for every row so that multiple OOI can be added
    for col in range (2,len(data.columns)):
        if data.iloc[row][col] <= pixel_distance:               # if the given distance is smaller than or equal to the pre-defined pixel distance
            fixation_object[row].append(data.columns[col])      # fill the respective column name into the list
    if fixation_object[row] == []:                              # if there is no fixation on an OOI,'Non-OOI' is filled into the list
        fixation_object[row] = ['Non-IOO']
data['fixation_object'] = fixation_object


### 2A-D

# create new dataframe that collects the new information
df = pd.DataFrame(columns = data.columns[2:-1])

# 2a: count hits per OOI (multiple OOI per fixation possible)
hits = []
for i in all_ooi:
    hits.append(sum(x.count(i) for x in data['fixation_object']))
df.loc[len(df)] = hits

# calculate fixation time 
fixation_time = [0]*len(data)
for row in range (0,len(data)):
    fixation_time[row] = data['end_time'][row]-data['start_time'][row]
data['fixation_time'] = fixation_time

# 2b: calculate total fixation time (= dwell time) per object and add to df 
# can be improved
dwell_time = [0]*len(all_ooi)
i=0
for ooi in all_ooi:
    for row in range(0,len(data)):
        if ooi in data.iloc[row]['fixation_object']:
            dwell_time[i] = dwell_time[i] + data.iloc[row]['fixation_time']
    i=i+1
df.loc[len(df)] = dwell_time

# 2c: calculate relative percentages that the participant spend looking at individual OOIs over the trial
# assuming total time = total fixation time of hits (without saccades and without Non-OOIs, but multiple hits per fixation)
relative_dwell_time_hits = [x/sum(df.loc[1])*100 for x in dwell_time] # sum(df.loc[1]): total fixation time of all the hits
df.loc[len(df)] = relative_dwell_time_hits

# rename rows of df with index and save it to excel
df.index = ['Hits', 'Dwell time [s]', 'Relative Dwell Time [%]']
df.to_csv('Analysis/TrainData/analysis_{}px.csv'.format(pixel_distance))

# 2d: visualize using barplots
visualize_hits()
visualize_dwelltime()
visualize_rel_dwelltime()

# save all plots
save_plots()



### 3A-B

# 3a: Repeat 2a-d for this case. Done by changing the variable pixel_distance.

# 3b: What is the difference to distance 0?
# - more hits and dwell time in total
# - more relative dwell time [%] of physical objects compared to the App screen in 20px compared to 0px
# - App has most hits with 0px, while Pen has most hits with 20px



### 4: OTHER METRICS



print('finito')







