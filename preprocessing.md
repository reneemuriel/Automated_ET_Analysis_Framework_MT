# How to: Data Pre-Processing for Automated ET Analysis Framework

## Export fixation/saccade file from Tobii Pro Lab

1.	Open your project in Tobii Pro Lab
2.  Rename the _Participant_ column in all recordings in the following format: `participantxx_trialyy`, where `xx` denotes the participant number and `yy` denotes the trial number (01-99)
3.	Go to _Metrics_
4.	_Select metrics for export_: tick all the boxes	
5.	Change the _Settings_ if needed
    - _Export format_: Event-based TSV file
    - _Gaze filter_: Tobii-IVT (Attention) 
        - This pre-set is optimized for wearable eye trackers and is used as the default pre-set for Tobii Glasses projects.
5.	_Data selection_: Select all the recordings you want to export (of all groups) 
6.	Click _Export_ and save the file as `all_recordings.tsv` into the directory `data/tobii/split`
7.	Run `split_tobii_output.py` in `scripts/` to split the `all_recordings.tsv` file into separate files per trial. They will be exported into `data/tobii/split/tobii_files`
    - Now they should be named correctly: `participantxx_trialxx_tobii.tsv`

## Create OGD files with cGOMSE

1.	Create OGD files with the tobii.tsv files according to the cGOMSE documentation.
    - If PVHMM for HAR was performed, action columnn should be named `action` or `Action`.
    - If needed, run `tobii_to_fixations.py` in `scripts/` to create the __fixations.txt_ files out of the __tobii.tsv_ files first. For this, dump the __tobii.tsv_ files into `data/tobii/to_fixations`. They are exported into `data/tobii/to_fixations/reformatted`.
2.	Once the OGD files were successfully created, add __ogd_ to the filenames with `append_input_type.py` in `scripts`. For this, dump the OGD files into `data/append_type/`. 
     - Attention: All files in the directory will get the appendix, so only save the files from the correct export in this directory!
     - If needed, change the _input_path_ to the directory where you saved the files and if needed, change the _input_type_ to "ogd".
3. The files should have the following format: `participantxx_trialxx_ogd.tsv`

## Prepare input structure
1.	Make sure all the files are named correctly after their participant and trial number, as well have the correct appendix.
    - Fixation/saccade files: `participantxx_trialxx_tobii.tsv`
    - OGD files created with cGOMSE: `participantxx_trialxx_ogd.txt`
2.  For a new analysis, create a new input folder: `data/input/analysis1/`
3.  For each group or condition, create a separate folder in this new directory and dump all the input files (Fixation/saccade file and if available, the OGD file) belonging to the same group in there: 
    - E.g. `data/input/analysis1/group_a/`
    - This structure has to be followed even if there are no groups: `data/input/analysis1/onlygroup/`
4.	You can also make an additional subdirectory, if there are multiple ways to group your data, so that you can run different analyses, 
    - e.g. `data/input/analysis1/grouped_by_difficulty/group_easy`
5.	When you have to provide the input path in the program later, you have to provide the directory where the group folders are placed.
