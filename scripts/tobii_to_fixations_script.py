'''
Reformat _tobii.tsv (metrics export) files to _fixations.txt files 

Place tobii files data/tobii/to_fixations/. 

If the files are named correctly (participantxx_trialxx_tobii.tsv), the new files will be named "participantxx_trialxx_fixations.txt".

These files can be used in the OGD algorithm.
'''




# import
import pandas as pd
import os
import glob
from pathlib import Path

filenames = glob.glob('data/tobii/to_fixations/*.tsv')

# choose output path
output_path = 'data/tobii/to_fixations/reformatted/'
os.makedirs(output_path, exist_ok=True)

def reformat(file, output_path):

    df_raw = pd.read_csv(file, sep='\t')

    # filter by row e.g. only rows that are fixations
    df_out = df_raw[df_raw["Event_type"]  == "Fixation"]

    # select colums
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

    # rename columns
    df_out.columns = ['Event Start Trial Time [ms]',"Event End Trial Time [ms]", 'Event Duration [ms]', 'Visual Intake Position X [px]', 'Visual Intake Position Y [px]']

    # save file
    base = os.path.basename(file)
    file_string = os.path.splitext(base)[0]
    file_string_trialonly = file_string[:-6]
    save_path = output_path + '{}_fixations.txt'.format(file_string_trialonly) 
    df_out.to_csv(save_path, sep='\t', index=False) 
    print("file: {} was reformatted successfully".format(file_string_trialonly))

# reformat 
for filename in filenames:
    reformat(filename, output_path)