import pandas as pd
import os
import glob
from pathlib import Path


def reformat(file, trial_path):    

    df_raw = pd.read_csv(file, sep='\t')

    #Filter by row e.g. only rows that are Sacccades
    df_out = df_raw[df_raw["Eye movement type"]  == "Saccade"]


    #Select certain colums
    df_out = df_out[["Recording timestamp", "Gaze event duration"]]

    df_out['Recording timestamp'] = df_out['Recording timestamp'].div(1000)
    #df_out[['change_x', 'change_y']] = df_out[['Fixation point X', 'Fixation point Y']].diff()
    #df_out = df_out[(df_out['change_x']!=0) & (df_out['change_y']!=0)]
    #df_out = df_out.drop(['change_x', 'change_y'], 1)

    df_out.columns = ['Event Start Trial Time [ms]', 'Event Duration [ms]']

    sum_column = df_out["Event Start Trial Time [ms]"] + df_out["Event Duration [ms]"]
    df_out["Event End Trial Time [ms]"] = sum_column

    df_out = df_out[["Event Start Trial Time [ms]", "Event End Trial Time [ms]", "Event Duration [ms]"]]

    base = os.path.basename(file)
    file_string = os.path.splitext(base)[0]
    

    # changed location where file is saved and filename
    df_out.to_csv(trial_path + '_saccades.txt', sep='\t', index=False) 

    print("file: {} was reformatted successfully".format(file_string))


