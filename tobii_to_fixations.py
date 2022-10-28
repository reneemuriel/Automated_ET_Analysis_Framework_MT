#Author Thomas Kreiner
#Requires python3 and pandas

# old name: tobii_to_cgom
# changes by renee: changed location where file is saved and filename
# tobii output: in microseconds, multiple standard files (meaning one .tsv file per recording)

import pandas as pd
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import glob
from pathlib import Path

### Reformat _tobii.tsv files to _fixations.txt files 

# If the files are named correctly (participantxx_trialxx_tobii.tsv), the files will be correctly named to "participantxx_trialxx_fixations.txt"

# place tobii files in subdirectory 'tobii_to_fixations' of where this .py file is located
path = os.getcwd()
filenames = glob.glob(path + '/tobii_to_fixations' + "/*.tsv")
# choose output path
output_path = path + '/tobii_to_fixations/'



def insert_row(idx, df, df_insert):
    dfA = df.iloc[:idx, ]
    dfB = df.iloc[idx:, ]

    df = dfA.append(df_insert).append(dfB).reset_index(drop = True)

    return df



def reformat(file, trial_path):    #ouput file location added by renee

    df_raw = pd.read_csv(file, sep='\t')

    #Filter by row e.g. only rows that are Fixations
    df_out = df_raw[df_raw["Eye movement type"]  == "Fixation"]

    #Select certain colums
    df_out = df_out[["Recording timestamp", "Gaze event duration", "Fixation point X", "Fixation point Y"]]


    ## tobii ouput file: in microseconds
    df_out['Recording timestamp'] = df_out['Recording timestamp'].div(1000).round()
    df_out[['change_x', 'change_y']] = df_out[['Fixation point X', 'Fixation point Y']].diff()
    df_out = df_out[(df_out['change_x']!=0) & (df_out['change_y']!=0)]
    df_out = df_out.drop(['change_x', 'change_y'], 1)

    df_out.columns = ['Event Start Trial Time [ms]', 'Event Duration [ms]', 'Visual Intake Position X [px]', 'Visual Intake Position Y [px]']

    sum_column = df_out["Event Start Trial Time [ms]"] + df_out["Event Duration [ms]"]
    df_out["Event End Trial Time [ms]"] = sum_column

    df_out = df_out[["Event Start Trial Time [ms]", "Event End Trial Time [ms]", "Event Duration [ms]", "Visual Intake Position X [px]", "Visual Intake Position Y [px]"]]


    base = os.path.basename(file)
    file_string = os.path.splitext(base)[0]
  
    df_out.to_csv(trial_path + '_fixations.txt', sep='\t', index=False) 

    print("file: {} was reformatted successfully".format(file_string))



def reformat_sep(file, output_path):

    df_raw = pd.read_csv(file, sep='\t')

    #Filter by row e.g. only rows that are Fixations
    df_out = df_raw[df_raw["Eye movement type"]  == "Fixation"]

    #Select certain colums
    df_out = df_out[["Recording timestamp", "Gaze event duration", "Fixation point X", "Fixation point Y"]]


    ## tobii ouput file: in microseconds
    df_out['Recording timestamp'] = df_out['Recording timestamp'].div(1000).round()
    df_out[['change_x', 'change_y']] = df_out[['Fixation point X', 'Fixation point Y']].diff()
    df_out = df_out[(df_out['change_x']!=0) & (df_out['change_y']!=0)]
    df_out = df_out.drop(['change_x', 'change_y'], 1)

    df_out.columns = ['Event Start Trial Time [ms]', 'Event Duration [ms]', 'Visual Intake Position X [px]', 'Visual Intake Position Y [px]']

    sum_column = df_out["Event Start Trial Time [ms]"] + df_out["Event Duration [ms]"]
    df_out["Event End Trial Time [ms]"] = sum_column

    df_out = df_out[["Event Start Trial Time [ms]", "Event End Trial Time [ms]", "Event Duration [ms]", "Visual Intake Position X [px]", "Visual Intake Position Y [px]"]]


    base = os.path.basename(file)
    file_string = os.path.splitext(base)[0]
    file_string_trialonly = file_string[:-6]

    save_path = output_path + '{}_fixations.txt'.format(file_string_trialonly)
   
    df_out.to_csv(save_path, sep='\t', index=False) 

    print("file: {} was reformatted successfully".format(file_string_trialonly))

# reformat 
for filename in filenames:
    reformat_sep(filename, output_path)