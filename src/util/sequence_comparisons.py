'''
Sequence comparison
'''

import pandas as pd
import numpy as np
import string
import pylev

def calculate_difference(opt_seq, trial_seq, algo):

    # make list of alphabet for dictionary
    alphabet = string.ascii_lowercase

    ## make strings out of lists
    
    # extract all actions that are present in the sequences and create dictionary with all actions
    string_list = trial_seq + opt_seq
    string_set_unique = set(string_list)
    string_list_unique = list(string_set_unique)
    dict_actions = { string_list_unique[i] : alphabet[i] for i in range(0, len(string_list_unique) ) }
    # create strings from the sequences
    trial_seq_list = list(map(dict_actions.get, trial_seq))
    trial_seq_string = ''.join(trial_seq_list)
    opt_seq_list = list(map(dict_actions.get, opt_seq))
    opt_seq_string = ''.join(opt_seq_list)
      
    if algo == 'levenshtein_distance':
        distance = pylev.levenshtein(trial_seq_string, opt_seq_string)
    
    return distance

