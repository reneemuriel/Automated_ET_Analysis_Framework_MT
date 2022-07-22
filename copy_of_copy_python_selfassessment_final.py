#### PYTHON SELFASSESSMENT ####

# load packages
from ntpath import join
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from pathlib import Path
# from os import path
# import os
# import glob
from IPython.display import display


# import own functions
from metrics_calculations import count_hits_per_ooi


### FUNCTIONS

### visualize

# hits
def visualize_hits(df, trial):
    global fig_hits
    fig_hits = plt.figure(figsize=(8,8))
    sns.set_theme(style='whitegrid')
    plt.bar(df.columns, df.iloc[trial], color='lightblue')
    plt.title('Hits per OOI ({})'.format(txt_filenames[trial]), fontsize = 16)
    plt.ylabel('Number of hits', weight = 'bold')
    plt.xlabel('OOI', weight = 'bold')
    #plt.show()

# dwell_time
def visualize_dwelltime(df, trial):
    global fig_dwelltime
    fig_dwelltime = plt.figure(figsize=(8,8))
    sns.set_theme(style='whitegrid')
    plt.bar(df.columns, df.iloc[trial], color='lightblue')
    plt.title('Dwell time per OOI ({})'.format(txt_filenames[trial]), fontsize = 16)
    plt.ylabel('Dwell time [s]', weight = 'bold')
    plt.xlabel('OOI', weight = 'bold')
    #plt.show()

# relative_dwell_time_ooi
def visualize_rel_dwelltime(df, trial):
    global fig_rel_dwelltime
    fig_rel_dwelltime = plt.figure(figsize=(8,8))
    sns.set_theme(style='whitegrid')
    plt.bar(df.columns, df.iloc[trial], color='lightblue')
    plt.title('Relative percentages of dwell time per OOI ({})'.format(txt_filenames[trial]), fontsize = 16)
    plt.ylabel('Relative dwell time [%]', weight = 'bold')
    plt.xlabel('OOI', weight = 'bold')
    #plt.show()

# save all 3 plots per trial
def save_plots_per_trial(trial):
    fig_hits.savefig(join(ind_output_path,'fig_{}_hits_{}px.png'.format(txt_filenames[trial], pixel_distance)))
    fig_dwelltime.savefig(join(ind_output_path, 'fig_{}_dwelltime_{}px.png'.format(txt_filenames[trial], pixel_distance)))
    fig_rel_dwelltime.savefig(join(ind_output_path, 'fig_{}_rel_dwelltime_{}px.png'.format(txt_filenames[trial], pixel_distance)))



### calculations

# add column fixation_object
def add_fixation_object():
    fixation_object = [] 
    for row in range(0,len(data)):
        fixation_object.append([])                                  # make sublist for every row so that multiple OOI can be added
        for col in range (2,len(data.columns)):
            if data.iloc[row][col] <= pixel_distance:               # if the given distance is smaller than or equal to the pre-defined pixel distance
                fixation_object[row].append(data.columns[col])      # fill the respective column name into the list
        if fixation_object[row] == []:                              # if there is no fixation on an OOI,'Non-OOI' is filled into the list
            fixation_object[row] = ['Non-IOO']
    data['fixation_object'] = fixation_object

# count hits per fixation via the fixation_object column
def count_hits():
    hits = []
    for ooi in all_ooi:
        hits.append(sum(x.count(ooi) for x in data['fixation_object']))
    # df_hits.loc[len(df)] = hits
    return hits

# calculate fixation time per fixation/row
def calculate_fixation_time():
    fixation_time = [0]*len(data)
    for row in range (0,len(data)):
        fixation_time[row] = data['end_time'][row]-data['start_time'][row]
    data['fixation_time'] = fixation_time

# calculate dwell time via the fixation_object and fixation_time column (can be improved)
def calculate_dwell_time():
    global dwell_time
    dwell_time = [0]*len(all_ooi)
    i=0
    for ooi in all_ooi:
        for row in range(0,len(data)):
            if ooi in data.iloc[row]['fixation_object']:
                dwell_time[i] = dwell_time[i] + data.iloc[row]['fixation_time']
        i=i+1
    return dwell_time

# create and save boxplots of all trials 
def get_boxplots():
    # boxplot hits
    fig_boxplot_hits = plt.figure(figsize=(12,5))
    sns.set_theme(style='whitegrid')
    sns.set(font_scale = 1.2)
    sns.boxplot(data=df_hits_all, width= 0.5, color="lightblue")
    plt.title('Hits per OOI of all trials', fontsize = 16)
    plt.ylabel('Number of hits', weight = 'bold')
    plt.xlabel('OOI', weight = 'bold')
    # plt.show()

    # boxplot dwelltime
    fig_boxplot_dwelltime = plt.figure(figsize=(12,5))
    sns.set_theme(style ='whitegrid')
    sns.set(font_scale = 1.2)
    sns.boxplot(data=df_dwelltime_all, width= 0.5, color="lightblue")
    plt.title('Dwell time per OOI of all trials', fontsize = 16)
    plt.ylabel('Dwell Time [s]', weight = 'bold')
    plt.xlabel('OOI', weight = 'bold')
    # plt.show()

    # boxplot relative dwelltime
    fig_boxplot_rel_dwelltime = plt.figure(figsize=(12,5))
    sns.set_theme(style ='whitegrid')
    sns.set(font_scale = 1.2)
    sns.boxplot(data=df_rel_dwelltime_all, width= 0.5, color="lightblue")
    plt.title('Relative percentages of dwell time per OOI of all trials', fontsize = 16)
    plt.ylabel('Relative Dwell Time [%]', weight = 'bold')
    plt.xlabel('OOI', weight = 'bold')
    # plt.show()

    # save boxplots
    fig_boxplot_hits.savefig(join(px_output_path, 'fig_boxplot_hits_{}px.png'.format(pixel_distance)))
    fig_boxplot_dwelltime.savefig(join(px_output_path,'fig_boxplot_dwelltime_{}px.png'.format(pixel_distance)))
    fig_boxplot_rel_dwelltime.savefig(join(px_output_path, 'fig_boxplot_rel_dwelltime_{}px.png'.format(pixel_distance)))



### DEFINE VARIABLES

# pixel distance for OOI hit (smaller or equal to)
pixel_distance = 20

# file path to data relative to root folder (use forward slashes)
data_path = Path('Data/TestSet/')

# check if there are columns that need to be dropped
columns_to_drop = []

# file path to output/analysis relative to root folder (use forward slashes)
output_path = Path('Analysis/TestSet/')
px_output_path = output_path / '{}px pixel distance'.format(pixel_distance)
ind_output_path = px_output_path / 'Individual_Trials'


# create directories to save output if they do not exist yet
if not output_path.exists():            
    output_path.mkdir(parents=True)   
if not px_output_path.exists():
    px_output_path.mkdir(parents=True)  
if not ind_output_path.exists():
    ind_output_path.mkdir(parents=True)

### LOOP THROUGH ALL TRIALS

# extract filenames
txt_file_paths = sorted(glob(join(data_path,'*.txt')))   # finds all txt files in the specified folder and saves paths
txt_filenames = []

# loop through all the trials/participants
for i in range(0,len(txt_file_paths)): 

    # read data 
    data = pd.read_csv(txt_file_paths[i], sep='\t') 

    # drop unused columns
    data.drop(columns = columns_to_drop, inplace = True)

    # create list with filenames from 
    txt_filenames.append(Path(txt_file_paths[i]).stem)


    if i == 0:  # only in the first iteration
        # create new dataframes that collects hits, dwell time and relative dwell time of all trials, with columns raw data
        df_hits_all = pd.DataFrame(columns= data.columns[2:])
        df_dwelltime_all = pd.DataFrame(columns= data.columns[2:])
        df_rel_dwelltime_all = pd.DataFrame(columns= data.columns[2:])

    # create temporary dataframes 
    df_hits = pd.DataFrame(columns= data.columns[2:])
    df_dwelltime = pd.DataFrame(columns= data.columns[2:])
    df_rel_dwelltime = pd.DataFrame(columns= data.columns[2:])

    # create list of all OOIs (used in functions)
    all_ooi = data.columns.values.tolist()[2:len(data)]

    # add column to data that states the fixation object(s) for each row (assuming multiple hits per fixation/row)
    add_fixation_object()

    # count hits per OOI (multiple OOI per fixation possible) and add to df
    #new
    df_hits.loc[len(df_hits)] = count_hits_per_ooi(all_ooi, data['fixation_object']) 
    df_hits_all = pd.concat([df_hits_all, df_hits], join='outer', ignore_index=True) # add to df

    # calculate fixation time  and add to data
    calculate_fixation_time()

    # calculate dwell time(= total fixation time) per object and add to df 
    df_dwelltime.loc[len(df_dwelltime)] = calculate_dwell_time()
    df_dwelltime_all = pd.concat([df_dwelltime_all, df_dwelltime], join='outer', ignore_index=True) # add to df
    
    # calculate relative percentages
    # assuming total time = total fixation time of hits (without saccades and without Non-OOIs, but multiple hits per fixation)
    relative_dwell_time_hits = [x/sum(df_dwelltime.loc[0])*100 for x in dwell_time] # (df_dwelltime.loc[0]): total fixation time of all the hits
    df_rel_dwelltime.loc[len(df_rel_dwelltime)] = relative_dwell_time_hits
    df_rel_dwelltime_all = pd.concat([df_rel_dwelltime_all, df_rel_dwelltime], join='outer', ignore_index=True) # add to df

display(data)

### STATISTICS  
# create dataframe df_stats that collects the mean, median and standard deviation of hits, dwelltime and relative dwelltime of all OOI
df_stats = pd.DataFrame(columns= df_hits_all.columns)
stats = ['mean_hits', 'median_hits', 'std_hits','mean_dwelltime', 'median_dwelltime', 'std_dwelltime', 'mean_rel_dwelltime', 'median_rel_dwelltime', 'std_rel_dwelltime', ]
for row_index in stats: # create empty rows and name them
    df_stats.append(pd.Series(name=row_index)) 

# fill the dataframe with the values calculated from the previous dataframes 
df_stats.loc['mean_hits'] = df_hits_all.mean()
df_stats.loc['median_hits'] = df_hits_all.median()
df_stats.loc['std_hits'] = df_hits_all.std()

df_stats.loc['mean_dwelltime'] = df_dwelltime_all.mean()
df_stats.loc['median_dwelltime'] = df_dwelltime_all.median()
df_stats.loc['std_dwelltime'] = df_dwelltime_all.std()

df_stats.loc['mean_rel_dwelltime'] = df_rel_dwelltime_all.mean()
df_stats.loc['median_rel_dwelltime'] = df_rel_dwelltime_all.median()
df_stats.loc['std_rel_dwelltime'] = df_rel_dwelltime_all.std()

stats_path = px_output_path / 'statistics_summary_{}px.csv'.format(pixel_distance)
df_stats.to_csv(stats_path)


### VISUALIZE

# visualize single trials using barplots (in the end: replace case = i by .txt filename)
for j in range(0,len(txt_filenames)):
    visualize_hits(df=df_hits_all, trial=j)
    visualize_dwelltime(df=df_dwelltime_all, trial=j)
    visualize_rel_dwelltime(df=df_rel_dwelltime_all, trial=j)
    save_plots_per_trial(trial=j)

# visualize all trials as boxplots and save them
get_boxplots()

print('finito')
