'''
Generation of Summary Reports
'''

import os
import pandas as pd
import numpy as np
from pathlib import Path
import logging as log

# local imports
import src.util.result_summaries as result_summaries

def get_summary(list_tuple: list, output_path: str, ooi_analysis: bool, kcoeff_analysis: bool, action_analysis: bool) -> tuple:

    # collects which modules have been executed -> only these end up on report
    # output path is needed to import graphs 

    log.info("All modules executed. Starting to generate summary reports.") 

    # get individual lists from tuple
    trials, trial_paths, trials_only, participants, participant_paths, groups, group_paths, output_path_groups = list_tuple
    
    # import exported figures from output directory
    img_import_path = output_path
    # create new output irectory if it not exists yet
    results_path = Path('data/report')
    os.makedirs(results_path, exist_ok = True)

    # call result_summaries function to generate reports (overview over all groups)
    result_summaries.allgroups_groups_results(img_import_path, results_path, ooi_analysis, kcoeff_analysis, action_analysis, 'All Groups')

    # iterate through groups  
    for i in range(len(groups)):
        # change import path to the respective group
        img_import_path = output_path / Path(groups[i])
        # create new directory for the group if it does not exist yet
        results_path = Path('data/report') / Path(groups[i])
        os.makedirs(results_path, exist_ok = True)
        # call result_summaries function to generate reports (overview over all participants per group)
        result_summaries.allgroups_groups_results(img_import_path, results_path, ooi_analysis, kcoeff_analysis, action_analysis, groups[i])
        
        # iterate through participants
        for j in range(len(participants[i])):
            img_import_path = output_path / Path(groups[i]) / participants[i][j]
            results_path = Path('data/report') / Path(groups[i]) / participants[i][j]
            os.makedirs(results_path, exist_ok = True)
            # call result_summaries function to generate reports (overview over all participants per participant)
            result_summaries.participants_results(img_import_path, results_path, ooi_analysis, kcoeff_analysis, action_analysis, participants[i][j])

    log.info("Finished creating all summary reports.") 
