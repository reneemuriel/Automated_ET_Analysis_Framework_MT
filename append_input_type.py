from pathlib import Path
import os


def append_input_type(filename, input_type):
    path = Path(filename)
    os.rename(filename, path.with_stem(f"{path.stem}_{input_type}")) 
    #return path.with_stem(f"{path.stem}_{input_type}")


def remove_input_type(filename, input_type):
    path = Path(filename)
    os.rename() 


# set variables
input_path = Path('Data/gaze_input/TrainSet')
input_type = 'fixationdata'


filename_list = os.listdir(input_path)

if input('Do you want to append <_{}> to the filename? Then type yes:\n'.format(input_type)) == 'yes':

    for i in range(len(filename_list)):
        filename1 = input_path / filename_list[i]
        append_input_type(filename1, input_type)

