#Author Thomas Kreiner
#Requires python3 and pandas

# tobii file expert in microseconds!

#Changes from cgom: 

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

    #Filter by row e.g. only rows that are Saccades
    df_out = df_raw[df_raw["Event_type"]  == "Saccade"]

    #Select certain colums
    df_out = df_out[["Start", "Stop", "Duration"]]

    df_out.columns = ['Event Start Trial Time [ms]',"Event End Trial Time [ms]", 'Event Duration [ms]']

    base = os.path.basename(file)
    file_string = os.path.splitext(base)[0]
    

    # changed location where file is saved and filename
    df_out.to_csv(trial_path + '_saccades.txt', sep='\t', index=False) 

    print("file: {} was reformatted successfully".format(file_string))



for filename in filenames:
    reformat(filename)