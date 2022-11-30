''' 
Converts tobii export (.tsv) into saccades file (.txt)
'''

import pandas as pd
import os
from pathlib import Path

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

    #print("file: {} was reformatted successfully".format(file_string))

