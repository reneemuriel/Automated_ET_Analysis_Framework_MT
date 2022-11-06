import pandas as pd

# split the "all_recordings.tsv" file to multiple .tsv files 
# according to the column "Participant" which are the trial names in the format participantxx_trialxx

df_to_split = pd.read_csv('large_tsv_to_tobii/all_recordings.tsv', sep='\t')
participants = df_to_split['Participant'].unique()

for participant in participants:
    df_split = df_to_split[df_to_split['Participant'] == participant]
    df_split.to_csv('large_tsv_to_tobii/{}_tobii.tsv'.format(participant), sep = '\t')


