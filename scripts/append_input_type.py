'''
Append string to filename, e.g. to append '_ogd' to OGD files 
'''

from pathlib import Path
import os

# set variables
input_type = 'tobii' # without filename extension or _, just e.g. "tobii", "tobii_kcoeff", "ogd"

def append_input_type(filename, input_type):
    path = Path(filename)
    new_path = path.with_name(f'{path.stem}_{input_type}{path.suffix}')
    os.rename(filename, new_path)
    #os.rename(filename, path.with_stem(f"{path.stem}_{input_type}")) # for python versions >= 3.9
    

input_path = Path('data/append_type')
filename_list = os.listdir(input_path)

if input('Do you want to append <_{}> to the filename? Then type yes:\n'.format(input_type)) == 'yes':

    for i in range(len(filename_list)):
        filename1 = input_path / filename_list[i]
        append_input_type(filename1, input_type)
    print('Successfully added the suffix <{}> to the filenames!'.format(input_type))

