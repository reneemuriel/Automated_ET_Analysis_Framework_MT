# adapted from Thomas Kreiner

# new: takes event-based metrics export by tobii pro lab

import pandas as pd
import os
import glob
from pathlib import Path






def reformat(file, trial_path):    #ouput file location added by renee

    df_raw = pd.read_csv(file, sep='\t')

    #Filter by row e.g. only rows that are Fixations
    df_out = df_raw[df_raw["Event_type"]  == "Fixation"]

    #Select certain colums
    df_out = df_out[["Start", "Stop", "Duration", "FixationPointX", "FixationPointY"]]

    # multiply normalised coordinates by resolution (1920 x 1080)
    df_out['FixationPointX'] = df_out['FixationPointX']*1920
    df_out['FixationPointY'] = df_out['FixationPointY']*1080
    # and round to 1px
    df_out['FixationPointX'] = df_out['FixationPointX'].round(0)
    df_out['FixationPointY'] = df_out['FixationPointY'].round(0)


    # drop columns with no change in fixation coordinate(?)
    df_out[['change_x', 'change_y']] = df_out[['FixationPointX', 'FixationPointY']].diff()
    df_out = df_out[(df_out['change_x']!=0) & (df_out['change_y']!=0)]
    df_out = df_out.drop(['change_x', 'change_y'], 1)

    df_out.columns = ['Event Start Trial Time [ms]',"Event End Trial Time [ms]", 'Event Duration [ms]', 'Visual Intake Position X [px]', 'Visual Intake Position Y [px]']


    base = os.path.basename(file)
    file_string = os.path.splitext(base)[0]
  
    df_out.to_csv(trial_path + '_fixations.txt', sep='\t', index=False) 

     #print("file: {} was reformatted successfully".format(file_string))



