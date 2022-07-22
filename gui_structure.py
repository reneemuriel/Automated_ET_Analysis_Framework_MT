### GUI


# data structure module : folder_structure
# GUI: data structure must be like this:
# highest level of input: folder called "input"
# choose input folder in GUI and save it 
ui_gaze_input_path =  'Data/gaze_input/'         #folder selected from gui
gaze_input_path = Path(ui_input_path)


# are there 2 groups?
#   yes -> next question
two_groups = True
# are there 2 groups that should to be compared?
    #   yes -> there must be one subfolder per group below the level of the input folder
comparing_groups = True       
    #       are the folders named  correctly?
    #           yes -> next question
    #           no -> rename them (manually)
    #       save correct group names: 
group_names = []
group_names = [f for f in sorted(os.listdir(input_path))]
    #   no -> next question
comparing_groups = False
#   no -> next question
two_groups = False
comparing_groups = False


# are there multiple subsequent trials per subject?
#   yes -> save in variable
subs_trials = True
#   yes -> individual trial should be named like this: "participantxx_trialxx_typeofinput"
#       are the trials named correctly?
#           yes -> next question
#           no -> rename (maybe use append_input_type.py)                    
#   no -> save in variable
subs_trials = False
#   no -> individual trial files should still be saved in subject folder (as above) (not in input folder or group folder)
#       individual trial should be saved without trial number

## folder structure is done now and the entire directory/folder structure (empty) below input can be copied to output folder


