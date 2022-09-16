import pandas as pd
import os

def reformat(filepath, trial_path):
    # similar to tobii_to_fixations.py
    e=3

    df_raw = pd.read_csv(filepath, sep='\t')

    # filter for whole events (?) 
    df_out = df_raw[df_raw["Validity"]  == "Whole"]
    #df_out = df_raw

    # select certain colums to keep
    # event-based tobii ouput file here: already in milliseconds
    df_out = df_out[['Event_type', 'Start', 'Stop', 'Duration', 'Saccade_amplitude']]

    df_out.rename(columns = {'Event_type':'event_type', 'Start':'start_time', 'Stop':'end_time', 'Duration':'duration', 'Saccade_amplitude':'saccade_amplitude'}, inplace = True)


    base = os.path.basename(filepath)
    file_string = os.path.splitext(base)[0]
    

    # changed location where file is saved and filename
    df_out.to_csv(trial_path + '_kcoeff.txt', sep='\t', index=False) 

    print("file: {} was reformatted successfully".format(file_string))