import pandas as pd
from pathlib import Path
import os

# split the one .tsv file named 'all_recordings.tsv' exported from the Metrics Export from Tobii Pro Lab to multiple .tsv files 
# according to the column "Participant" which are the trial names in the format participantxx_trialxx

# exported into subfolder "files" 

# read df that we want to split up
df_to_split = pd.read_csv('data/tobii/split/all_recordings.tsv', sep='\t')
participants = df_to_split['Participant'].unique()

# create subfolder to export files
os.makedirs(Path('data/tobii/split/tobii_files'), exist_ok= True)

for participant in participants:
    df_split = df_to_split[df_to_split['Participant'] == participant]
    df_split.to_csv(Path('data/tobii/split/tobii_files/{}_tobii.tsv'.format(participant)), sep = '\t')


