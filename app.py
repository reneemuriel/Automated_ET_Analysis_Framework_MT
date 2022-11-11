#TODO: update copyright notice
'''
Date:
Author: Renée Saethre (renees@ethz.ch)
Brief: entry point for the eye-tracking analyis framework
'''

# Python standard library imports
import sys, os
import yaml
import argparse
import logging as log

# PyQT5 imports for GUI and application event-loop
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# local imports
from src.gui.window import MainWindow

def start_analysis(config: dict) -> None:
    ''' TODO: document behaviour '''

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
        action_list = config['action_list']
        template_sequence = config['template_sequence']

    except:
        log.error("ERROR: could not read configuration dict. Terminating.")
        sys.exit(-1)

    # TODO: here the real analysis begins


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
    