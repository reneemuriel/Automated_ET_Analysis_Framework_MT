import pandas as pd
import numpy as np

def calculate_difference(opt_seq, trial_seq, algo):

    # extract all actions that are present in the sequences and create dictionary
    string_list = opt_seq + trial_seq
    dict_actions = { i : string_list[i] for i in range(0, len(string_list) ) }
    



    if algo == 'levenshtein_distance':
        e=3

