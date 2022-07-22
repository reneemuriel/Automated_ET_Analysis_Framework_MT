# load packages
from ntpath import join
from webbrowser import get
import pandas as pd
from pyparsing import unicode_string
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from pathlib import Path
# from os import path
import os
# import glob
# from IPython.display import display

# probably not with a module, but differntly
def get_variables_gui():
    # number of OOIs
    global number_of_oois, pixel_distance, two_groups, comparing_groups, subs_trials, gaze_input_path, number_of_subs_trials, group_names

    number_of_oois = 5 # from gui

    # list of all OOIs
    # all_oois = ["ooi_1", "ooi_2", "ooi_3"] # better from OGD data than from gui input!


    # pixel distance for OOI hit (smaller or equal to)
    pixel_distance = 20 # from gui

    # folder structure
    two_groups = True
    comparing_groups = True
    subs_trials = True
    number_of_subs_trials = 4

    ui_gaze_input_path =  'Data/gaze_input/' # from gui
    gaze_input_path = Path(ui_gaze_input_path)  

    if comparing_groups == True:
    # get names from subfolders below gaze_input and save them
        group_names = []
        group_names = [f for f in sorted(os.listdir(gaze_input_path))]    

        # other variables?


## testing
get_variables_gui()
print(group_names)
   

        











##### old from python assessment:

# def get_folder_structure
# file path to data relative to root folder (use forward slashes)
data_path = Path('Data/TestSet/') # folder chosen by user in GUI


# file path to output/analysis relative to root folder (use forward slashes)
output_path = Path('Analysis/TestSet/') # folder chosen by user in GUI

# create subfolders for pixel distance -> can be changed to subfolders
px_output_path = output_path / '{}px pixel distance'.format(pixel_distance)
ind_output_path = px_output_path / 'Individual_Trials'


# create directories to save output if they do not exist yet
if not output_path.exists():            
    output_path.mkdir(parents=True)   
if not px_output_path.exists():
    px_output_path.mkdir(parents=True)  
if not ind_output_path.exists():
    ind_output_path.mkdir(parents=True)

