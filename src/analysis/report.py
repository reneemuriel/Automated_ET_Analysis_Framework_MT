import os
import pandas as pd
import numpy as np
from pathlib import Path

import src.util.result_summaries as result_summaries


def get_summary(list_tuple: list, output_path: str, ooi_analysis: bool, kcoeff_analysis: bool, action_analysis: bool) -> tuple:

    # get individual lists from tuple
    trials, trial_paths, trials_only, participants, participant_paths, groups, group_paths, output_path_groups = list_tuple

    ### only if it should be run separately
    #ooi_analysis = True
    #kcoeff_analysis = True
    #action_analysis = True

    
    img_import_path = output_path
    results_path = Path('Summary Report')
    os.makedirs(results_path, exist_ok = True)
    result_summaries.allgroups_groups_results(img_import_path, results_path, ooi_analysis, kcoeff_analysis, action_analysis, 'All Groups')

    # iterate through groups    
    for i in range(len(groups)):
        img_import_path = output_path / Path(groups[i])
        results_path = Path('Summary Report') / Path(groups[i])
        os.makedirs(results_path, exist_ok = True)
        result_summaries.allgroups_groups_results(img_import_path, results_path, ooi_analysis, kcoeff_analysis, action_analysis, groups[i])
        
        # iterate through participants
        for j in range(len(participants[i])):
            img_import_path = output_path / Path(groups[i]) / participants[i][j]
            results_path = Path('Summary Report') / Path(groups[i]) / participants[i][j]
            os.makedirs(results_path, exist_ok = True)
            result_summaries.participants_results(img_import_path, results_path, ooi_analysis, kcoeff_analysis, action_analysis, participants[i][j])
