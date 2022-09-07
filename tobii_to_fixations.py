#Author Thomas Kreiner
#Requires python3 and pandas

# old name: tobii_to_cgom
#Changes by renee: changed location where file is saved and filename

import pandas as pd
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import glob
from pathlib import Path

path = os.getcwd()
filenames = glob.glob(path + '/To_be_formatted' + "/*.tsv")

#Import tsv into pandas dataframe: data.tsv must be in the same folder as python script

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
    

    # changed location where file is saved and filename
    df_out.to_csv(trial_path + '_fixations.txt', sep='\t', index=False) 

    print("file: {} was reformatted successfully".format(file_string))



for filename in filenames:
    reformat(filename)