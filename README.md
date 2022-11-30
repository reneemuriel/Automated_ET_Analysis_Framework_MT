# Automated ET Analysis Framework

This is the repository for the Master Thesis of Renée Muriel Saethre conducted at pdz at ETH Zurich.

## Abstract

## Table of Contents
- [Getting Started](#getting-started)
- [Directory Structure](#directory-structure)
- [Running the Framework](#running-the-framework)
- [Deliverables](#deliverables)
- [License](#license)

## Getting Started 

### Requirements
- Python 3.6.12 or newer 
- Conda 4.10 or newer
- QT Creator 4 or newer (for changes to the GUI)    

### Setting up the Repository 
Open a new Anaconda prompt window on Windows (on Linux and MacOS a normal shell will do). Set-up the project repository by running the following:
```bash
# clone repository
git clone https://github.com/reneemuriel/Automated_ET_Analysis_Framework_MT.git et-analysis && cd et-analysis

# create new conda environment and activate it
conda create --name et-env python=3.6.12 pip
conda activate et-env

# install requirements
pip install -r requirements.txt
```

### Data Pre-Processing
For the data pre-processing and correct data structure follow the instructions from [here](preprocessing.md).


## Directory Structure
- `app.py`: executable file for automated ET analysis framework
- `config/`: folder containing configuration files
- `data/`: main data directory
    - `append_type/`:  adds a desired string to filenames without
changing the extension, e.g. to append ’_ogd’ to exported OGD files
    - `input/`: folder that holds the eye tracking input data, if specified so in the configurations
    - `output/`: folder where the computed metrics will get exported to, if specified so in the configurations
    - `report/`: folder where the summary reports will be exported to 
    - `tobii/`: folder that holds tobii export files that are used by the scripts 
- `scripts/`: directory containing various utility scripts
- `src/`: directory containing source code of the project
    - `analysis/`: source files for the main analysis modules, i.e. general analysis, ooi-based analysis, k-coefficient analysis, action-based analysis, report, statistics
    - `gui/`: source files for the gui. `.ui` files can be edited with QT Creator. `.py` files within `resources/` must not be modified manually as they are auto-generated, see [here](https://stackoverflow.com/questions/43028904/converting-ui-to-py-with-python-3-6-on-pyqt5).
    - `utils/`: source files for the analysis modules

## Running the Framework
The ET analysis framework allows for two different execution modes: In _interactive mode_, the user is presented with a graphical user interface where key information can be declared, such as input and output paths, and the specific types of analysis that should be conducted. In _non-interactive mode_, there is no graphical user interface and the user provides the required information in a config file.

### Interactive Mode
Run the ET analysis framework in _interactive mode_ by running the following:
```bash
python app.py
```
ET analysis can then be started by performing the following 3 steps:

1. Enter the paths to the input and output paths.
2. Specify execution options.
3. Press the "Start Analysis" button. Execution may take a few hours, and the GUI may freeze in this time, without there being a problem. Do not force quit the application in case this happens, as all progress will be lost.

### Non-Interactive Mode
Run the ET analysis framework in _non-interactive mode_ by specifying a path to a `.yaml` configuration file. An example is provided [here](config/example.yaml).
```bash
python app.py --config config/example.yaml
```
The program will then start and run to completion without further interaction. This may take a few hours.

## Deliverables
The written thesis can be found [here](TODO:) while a comprehensive guide on the data pre-processing and input structure can be found [here](preprocessing.md).

## License
The graphical user interface (GUI) in this framework is written with PyQt5, i.e. Python bindings for the QT framework. These are licensed under the General Public License (GPL). Consequently, this repository is also licensed under the GPL. In essence, this means that users provided with a copy of this framework must be provided with access to the underlying source code. Since the framework is entirely written in Python and no individual binaries are distributed, this requirement is always satisfied.

