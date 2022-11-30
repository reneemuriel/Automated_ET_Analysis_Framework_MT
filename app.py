'''
Date: 3/12/2022
Author: Renée Saethre (renees@ethz.ch)
Brief: entry point for the eye-tracking analyis framework
'''

# Python standard library imports
import sys, os
from glob import glob
import yaml
import argparse
import logging as log
from pathlib import Path
from ntpath import join

# PyQT5 imports for GUI and application event-loop
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# local imports
from src.gui.window import MainWindow
from src.analysis import general_analysis
from src.analysis import kcoeff_analysis
from src.analysis import ooi_analysis
from src.analysis import action_analysis
from src.analysis import stats
from src.analysis import report

def get_lists(input_path: str, output_path: str) -> tuple:
    # same folder structure for one group and multiple groups: input/groupname/data
    groups = [f for f in sorted(os.listdir(input_path))] 

    trials = []
    trials_only = []
    trial_paths = []
    participants = []
    participant_paths = []
    group_paths = []
    output_path_groups = []

    for i in range(len(groups)):

        group_paths.append(input_path / Path(groups[i]))
        output_path_groups.append(output_path / Path(groups[i]))

        # copy group folder structure to output 
        os.makedirs(output_path / Path(groups[i]), exist_ok=True)
        
        # take all files from tobii input (to get one name per trial)
        filepaths = glob(join(group_paths[i],'*_tobii.tsv'))
        filenames =  [os.path.basename(filenames) for filenames in filepaths]
        
        # save all participants (participants[0] for group 1 and participants[1] for group 2)
        participant_paths.insert(i,[Path(filepath[:-18]) for filepath in filepaths]) # -18 to get participantxx
        participant_paths[i] = set(participant_paths[i]) # remove duplicates
        participant_paths[i] = list(participant_paths[i]) # convert to list
        participant_paths[i] = sorted(participant_paths[i]) # sort alphabetically
        participants.insert(i,[os.path.basename(participant) for participant in participant_paths[i]])
        participants[i] = sorted(participants[i]) # sort alphabetically

        # iterate through participants to save trial paths per participants
        trials.append([])
        trials_only.append([]) # not used yet, but could be useful later if trial number want to be compared to each other (e.g. all first trials vs. all third trials)
        trial_paths.append([])
        j=0
        for j in range(len(participants[i])):

            # create ouput folder for participant[i][j]
            os.makedirs(output_path / Path(groups[i]) / Path(participants[i][j]), exist_ok=True)
            
            # list all trials of participant[i][j]
            trial_path_list = []
            for file in filepaths:
                if '{}'.format(participants[i][j]) in file:
                    trial_name = file[:-10] # to get trialname only
                    trial_path_list.append(trial_name)
            trials_list = [os.path.basename(trial) for trial in trial_path_list]
            trials_only_list = [trial[14:] for trial in trials_list]
            
            # create ouput folder for each trial
            [os.makedirs(output_path / Path(groups[i]) / Path(participants[i][j]) / trial, exist_ok = True) for trial in trials_list]

            # add to trial list & sort alphabetically
            trials[i].insert(j,trials_list)
            trials[i][j] = sorted(trials[i][j])
            # add to trials_only list & sort alphabetically
            trials_only[i].insert(j, trials_only_list)
            trials_only[i][j] = sorted(trials_only[i][j])
            # add to trial_paths list
            trial_paths[i].insert(j,trial_path_list) 
            trial_paths[i][j] = sorted(trial_paths[i][j])

    groups = sorted(groups) # sort groups alphabetically

    return trials, trial_paths, trials_only, participants, participant_paths, groups, group_paths, output_path_groups


def start_analysis(config: dict) -> None:
    
    # extract parameters from the user interface (main-window)
    try:
        # get input and output paths first
        path_input = config['paths']['input']
        path_output = config['paths']['output']

        # get analysis options
        flag_general_analysis = config['executionOptions']['general_analysis']
        flag_kcoeff_analysis = config['executionOptions']['kcoeff_analysis']
        flag_action_analysis = config['executionOptions']['action_analysis']
        flag_ooi_analysis = config['executionOptions']['ooi_analysis']
        flag_sequence_comparison = config['executionOptions']['sequence_comparison']
        flag_entropy_stats = config['executionOptions']['entropy_stats']
        flag_novice_results = config['executionOptions']['novice_results']
        pixel_distance = config['executionOptions']['hitradius'] 

        # get action list and template sequence (will be an empty list if not applicable)
        all_actions = config['action_list']
        template_sequence = config['template_sequence']

    except:
        log.error("ERROR: could not read configuration dict. Terminating.")
        sys.exit(-1)

    # get paths and data from all trials and participants
    all_lists = get_lists(path_input, path_output)
    trials, trial_paths, trials_only, participants, participant_paths, groups, group_paths, output_path_groups = all_lists

    # set default values, e.g. for mean kcoeff that is required as input for action_analysis even if kcoeff analysis did not take place
    mean_kcoeff_all, stdev_kcoeff_all = [1,1]
    algrthm = 'levenshtein_distance'


    # do the individual parts of the analysis
    if flag_general_analysis:
        general_analysis.analyse(all_lists, path_output)

    if flag_kcoeff_analysis:
        mean_kcoeff_all, stdev_kcoeff_all = kcoeff_analysis.analyse(all_lists, path_output)

    if flag_ooi_analysis:
        ooi_analysis.analyse(all_lists, path_output, pixel_distance)

    if flag_action_analysis:
        action_analysis.analyse(all_lists, path_output, pixel_distance, all_actions, template_sequence, flag_sequence_comparison, flag_kcoeff_analysis, mean_kcoeff_all, stdev_kcoeff_all, algrthm)

    if flag_entropy_stats:
        stats.analyse(all_lists, path_output)

    if flag_novice_results:
        report.get_summary(all_lists, path_output, flag_ooi_analysis, flag_kcoeff_analysis, flag_action_analysis)



if __name__ == "__main__":
    # set-up logging environment
    log.basicConfig(format='%(levelname).1s [%(module)15s @ %(asctime)s]: %(message)s', datefmt='%H:%M:%S', level=log.INFO)
    log.info("set-up logging environment.")

    # parse command line arguments to see whether user wants to skip GUI
    parser = argparse.ArgumentParser(usage = '')
    parser.add_argument('--config', type = str, help = "path to config file to skip GUI and run directly")
    args = parser.parse_args()

    # skip gui if run with --config and path provided
    if args.config:
        config_file = args.config

        # open yaml file and turn it into a dictionary
        with open(config_file, 'r', encoding = "utf-8") as infile:
            config_dict = yaml.load(infile, Loader=yaml.FullLoader)

        # start analysis without showing GUI
        log.info("starting analysis without GUI.")
        start_analysis(config_dict)

    # run with GUI (default case)
    else:
        # allow the application to scale to high DPI screens
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

        # create an application with the command-line arguments, show window
        application = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        
        # start the application event-loop - terminate, when the window is closed
        log.info("start program with GUI.")
        exit_code = application.exec()
        log.info("application window closed with status {}.".format(exit_code))
        sys.exit(exit_code)
    