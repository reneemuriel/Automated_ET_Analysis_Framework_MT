from genericpath import exists
import pandas as pd
from matplotlib import image
from pathlib import Path
import cv2
from fpdf import FPDF
import os



### results for all groups and per group

def allgroups_groups_results(img_import_path, results_path, ooi_analysis, kcoeff_analysis, action_analysis, level):
    
    ### SUMMARY OF GAZE ANALYSIS: ALL GROUPS or GROUP X

    pdf = FPDF(unit='mm')
    pdf.add_page()

    # set title of the document
    pdf.set_font('Arial', 'B', 18)
    pdf.set_xy(10,10)
    pdf.cell(190, 20, 'Summary of Gaze Analysis - {}'.format(level), 1, 1, 'C')

    
    
    ### EFFICIENCY
    # (below title)

    pdf.set_font('Arial', 'B', 16)
    pdf.set_xy(10,35)
    pdf.cell(190,10, txt='1) Efficiency', align='C')


    ### first metric: total duration
    img_path = '{}/general_analysis/visualisations/Total Duration [ms]_boxplot_Whole Trial.png'.format(img_import_path)

    # title of metric
    pdf.set_font('Arial', 'B', 12)
    pdf.set_xy(10,45)
    pdf.cell(190,10, align = 'L', txt='Total Duration')

    # description
    pdf.set_font('Arial', '', 12)
    pdf.set_xy(10,55)
    pdf.multi_cell(190, 5 , align = 'L', txt='The average time [ms] is has taken the participant to complete the task. Generally, the shorter the duration, the more efficient the execution, and the higher the expertise.')

    # image
    # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
    img = cv2.imread(img_path)
    h, w, c = img.shape
    wh_ratio = w/h
    img_w = 80*wh_ratio
    if img_w > 190:
        # place image
        pdf.set_xy(10,70) 
        pdf.image(img_path, link='', type='PNG', w = 190) 
        # place frame
        img_h = 190/wh_ratio
        pdf.set_xy(10,70) 
        pdf.cell(w=190, h=img_h, border=1)

    else:
        # place image
        pdf.set_xy(10,70) 
        pdf.image(img_path, link='', type='PNG', h = 80)
        # place frame
        pdf.set_xy(10,70)
        pdf.cell(w=img_w, h=80, border=1)




    ### second metric (title page): total fixations
    img_path =  '{}/general_analysis/visualisations/Number of Fixations_boxplot_Whole Trial.png'.format(img_import_path)

    # title of metric
    pdf.set_font('Arial', 'B', 12)
    pdf.set_xy(10,160)
    pdf.cell(190,10, align = 'L', txt='Number of Fixations')

    # description
    pdf.set_font('Arial', '', 12)
    pdf.set_xy(10,170)
    pdf.multi_cell(190, 5 , align = 'L', txt='The average number of fixations per trial. Naturally, this correlates with the trial duration. Therefore, it is only useful if it is either normalised or if all recordings of a study have the same length. Generally, the number of fixations decreases with increasing expertise and in turn, increasing efficiency.')


    # image
    # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
    img = cv2.imread(img_path)
    h, w, c = img.shape
    wh_ratio = w/h
    img_w = 80*wh_ratio
    if img_w > 190:
        # place image
        pdf.set_xy(10,195) 
        pdf.image(img_path, link='', type='PNG', w = 190) 
        # place frame
        img_h = 190/wh_ratio
        pdf.set_xy(10,195) 
        pdf.cell(w=190, h=img_h, border=1)

    else:
        # place image
        pdf.set_xy(10, 195) 
        pdf.image(img_path, link='', type='PNG', h = 80)
        # place frame
        pdf.set_xy(10,195)
        pdf.cell(w=img_w, h=80, border=1)


    ### if ooi analysis and action analysis:
    if ooi_analysis == True and action_analysis == True:

        pdf.add_page()

        ## third metric (page without titles): duration per step -> to be done:O
        img_path = '{}/general_analysis/visualisations/Duration per Action [ms].png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,20)
        pdf.cell(190,10, align = 'L', txt='Average Duration per Action')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,30)
        pdf.multi_cell(190, 5 , align = 'L', txt='The average time [ms] it has taken the participants to complete each of the identified actions. Similar to "Total Duration", the faster they were, the more efficient the task was performed.')

        # image
        # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        if img_w > 190:
            # place image
            pdf.set_xy(10,55) 
            pdf.image(img_path, link='', type='PNG', w = 190) 
            # place frame
            img_h = 190/wh_ratio
            pdf.set_xy(10,55)
            pdf.cell(w=190, h=img_h, border=1)

        else:
            # place image
            pdf.set_xy(10,55) 
            pdf.image(img_path, link='', type='PNG', h = 80)
            # place frame
            pdf.set_xy(10,55)
            pdf.cell(w=img_w, h=80, border=1)



        ## fourth metric (page without titles): average dwell time
        img_path =  '{}/ooi_analysis/visualisations/Average Dwell Time [ms]_boxplot_Whole Trial.png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,145)
        pdf.cell(190,10, align = 'L', txt='Average Dwell Time')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,155)
        pdf.multi_cell(190, 5 , align = 'L', txt='The average duration per dwell [ms] on the defined OOIs. Longer dwell times can mean that the chosen OOIs keep up the attention for longer individual time periods.')


        # image
        # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        if img_w > 190:
            # place image
            pdf.set_xy(10,180) 
            pdf.image(img_path, link='', type='PNG', w = 190) 
            # place frame
            img_h = 190/wh_ratio
            pdf.set_xy(10,180)
            pdf.cell(w=190, h=img_h, border=1)

        else:
            # place image
            pdf.set_xy(10,180) 
            pdf.image(img_path, link='', type='PNG', h = 80)
            # place frame
            pdf.set_xy(10,180)
            pdf.cell(w=img_w, h=80, border=1)




    ### if only ooi analysis, no action analysis
    if ooi_analysis == True and action_analysis == False:

        pdf.add_page()

        ## third metric (page without titles): average dwell time
        img_path = '{}/ooi_analysis/visualisations/Average Dwell Time [ms]_boxplot_Whole Trial.png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,20)
        pdf.cell(190,10, align = 'L', txt='Average Dwell Time')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,30)
        pdf.multi_cell(190, 5 , align = 'L', txt='The average duration per dwell [ms] on the defined OOIs. Longer dwell times can mean that the chosen OOIs keep up the attention for longer individual time periods.')

        # image
        # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        if img_w > 190:
            # place image
            pdf.set_xy(10,55) 
            pdf.image(img_path, link='', type='PNG', w = 190) 
            # place frame
            img_h = 190/wh_ratio
            pdf.set_xy(10,55) 
            pdf.cell(w=190, h=img_h, border=1)

        else:
            # place image
            pdf.set_xy(10,55) 
            pdf.image(img_path, link='', type='PNG', h = 80)
            # place frame
            pdf.set_xy(10,55)
            pdf.cell(w=img_w, h=80, border=1)



    ## if only action analysis, no ooi analysis
    if ooi_analysis == False and action_analysis == True:

        pdf.add_page()

        ## third metric (page without titles): duration per step -> to be done:O
        img_path = '{}/general_analysis/visualisations/Duration per Action [ms].png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,20)
        pdf.cell(190,10, align = 'L', txt='Average Duration per Action')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,30)
        pdf.multi_cell(190, 5 , align = 'L', txt='The average time [ms] it has taken the participants to complete each of the identified actions. Similar to "Total Duration", the faster they were, the more efficient the task was performed.')

        # image
        # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        if img_w > 190:
            # place image
            pdf.set_xy(10,55) 
            pdf.image(img_path, link='', type='PNG', w = 190) 
            # place frame
            img_h = 190/wh_ratio
            pdf.set_xy(10,55) 
            pdf.cell(w=190, h=img_h, border=1)

        else:
            # place image
            pdf.set_xy(10,55) 
            pdf.image(img_path, link='', type='PNG', h = 80)
            # place frame
            pdf.set_xy(10,55)
            pdf.cell(w=img_w, h=80, border=1)



    ### FOCUS

    pdf.add_page()


    pdf.set_font('Arial', 'B', 16)
    pdf.set_xy(10,10)
    pdf.cell(190,10, txt='2) Focus', align='C')



    # first metric (on focus title page)): fixation/saccade duration
    img_path = '{}/general_analysis/visualisations/Relative Fixation Saccade Duration [%]_piecharts_Whole Trial.png'.format(img_import_path)

    # title of metric
    pdf.set_font('Arial', 'B', 12)
    pdf.set_xy(10,25)
    pdf.cell(190,10, align = 'L', txt='Relative Fixation/Saccade Duration')

    # description
    pdf.set_font('Arial', '', 12)
    pdf.set_xy(10,35)
    pdf.multi_cell(190, 5 , align = 'L', txt='Relative percentage of fixation and saccade durations, i.e. the total time the person has spent fixating compared to travelling from one fixation to the next. The higher the ratio, the more time is spent processing compared to searching.')


    # image
    # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
    img = cv2.imread(img_path)
    h, w, c = img.shape
    wh_ratio = w/h
    img_w = 80*wh_ratio
    if img_w > 190:
        # place image
        pdf.set_xy(10,60) 
        pdf.image(img_path, link='', type='PNG', w = 190) 
        # place frame
        img_h = 190/wh_ratio
        pdf.set_xy(10,60) 
        pdf.cell(w=190, h=img_h, border=1)

    else:
        # place image
        pdf.set_xy(10,60) 
        pdf.image(img_path, link='', type='PNG', h = 80)
        # place frame
        pdf.set_xy(10,60)
        pdf.cell(w=img_w, h=80, border=1)




    # if ooi analysis
    if ooi_analysis == True:
        
        # second metric first focus page: Normalised Stationary Gaze Entropy
        img_path =  '{}/ooi_analysis/visualisations/Normalised Stationary Gaze Entropy_barplot_Whole Trial.png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,150)
        pdf.cell(190,10, align = 'L', txt='Normalised Stationary Gaze Entropy')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,160)
        pdf.multi_cell(190, 5 , align = 'L', txt='A higher Stationary Gaze Entropy implies a more equal distribution of the visual attention between the OOIs. A lower value reflects when fixations tend to be concentrated on specific OOIs, either because they are more complex or more interesting to the subject.')

        # image
        # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        if img_w > 190:
            # place image
            pdf.set_xy(10,185) 
            pdf.image(img_path, link='', type='PNG', w = 190) 
            # place frame
            img_h = 190/wh_ratio
            pdf.set_xy(10,185)
            pdf.cell(w=190, h=img_h, border=1)

        else:
            # place image
            pdf.set_xy(10,185) 
            pdf.image(img_path, link='', type='PNG', h = 80)
            # place frame
            pdf.set_xy(10,185)
            pdf.cell(w=img_w, h=80, border=1)

        
        
        
        
        # third metric (no title): Normalised Gaze Transition Entropy
        pdf.add_page()
        img_path = '{}/ooi_analysis/visualisations/Normalised Gaze Transition Entropy_barplot_Whole Trial.png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,20)
        pdf.cell(190,10, align = 'L', txt='Normalised Gaze Transition Entropy')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,30)
        pdf.multi_cell(190, 5 , align = 'L', txt='In short, higher entropy can imply more randomness in the visual scanning pattern and in turn, less focus and efficiency.')

        # image
        # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        if img_w > 190:
            # place image
            pdf.set_xy(10,45) 
            pdf.image(img_path, link='', type='PNG', w = 190) 
            # place frame
            img_h = 190/wh_ratio
            pdf.set_xy(10,45) 
            pdf.cell(w=190, h=img_h, border=1)

        else:
            # place image
            pdf.set_xy(10,45) 
            pdf.image(img_path, link='', type='PNG', h = 80)
            # place frame
            pdf.set_xy(10,45)
            pdf.cell(w=img_w, h=80, border=1)




        # if k-coeff analysis
        if kcoeff_analysis == True:
            
        
            ## fourth metric (no title page): kcoeff
            img_path = '{}/k-coefficient_analysis/visualisations/K-Coefficients Summary.png'.format(img_import_path)

            # title of metric
            pdf.set_font('Arial', 'B', 12)
            pdf.set_xy(10,145)
            pdf.cell(190,10, align = 'L', txt='Average K-Coefficients')

            # description
            pdf.set_font('Arial', '', 12)
            pdf.set_xy(10,155)
            pdf.multi_cell(190, 5 , align = 'L', txt='K > 0 indicates relatively long fixations succeeded by short saccades, implying focal vision. K < 0 indicates relatively short fixations succeeded by long saccades, implying ambient vision.')

            # image
            # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
            img = cv2.imread(img_path)
            h, w, c = img.shape
            wh_ratio = w/h
            img_w = 80*wh_ratio
            if img_w > 190:
                # place image
                pdf.set_xy(10,170) 
                pdf.image(img_path, link='', type='PNG', w = 190) 
                # place frame
                img_h = 190/wh_ratio
                pdf.set_xy(10,170)
                pdf.cell(w=190, h=img_h, border=1)

            else:
                # place image
                pdf.set_xy(10,170) 
                pdf.image(img_path, link='', type='PNG', h = 80)
                # place frame
                pdf.set_xy(10,170)
                pdf.cell(w=img_w, h=80, border=1)


            if action_analysis == True:

                # fifth metric
                pdf.add_page()  
                img_path = '{}/k-coefficient_analysis/visualisations/K-Coefficients Summary per action.png'.format(img_import_path)

                # title of metric
                pdf.set_font('Arial', 'B', 12)
                pdf.set_xy(10,20)
                pdf.cell(190,10, align = 'L', txt='Average K-Coefficients per Action')

                # description
                pdf.set_font('Arial', '', 12)
                pdf.set_xy(10,30)
                pdf.multi_cell(190, 5 , align = 'L', txt='K > 0 indicates relatively long fixations succeeded by short saccades, implying focal vision. K < 0 indicates relatively short fixations succeeded by long saccades, implying ambient vision.')

                # image
                # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
                img = cv2.imread(img_path)
                h, w, c = img.shape
                wh_ratio = w/h
                img_w = 80*wh_ratio
                if img_w > 190:
                    # place image
                    pdf.set_xy(10,45) 
                    pdf.image(img_path, link='', type='PNG', w = 190) 
                    # place frame
                    img_h = 190/wh_ratio
                    pdf.set_xy(10,45) 
                    pdf.cell(w=190, h=img_h, border=1)

                else:
                    # place image
                    pdf.set_xy(10,45) 
                    pdf.image(img_path, link='', type='PNG', h = 80)
                    # place frame
                    pdf.set_xy(10,45)
                    pdf.cell(w=img_w, h=80, border=1)


    if ooi_analysis == False and kcoeff_analysis == True:
        # second metric first focus page: kcoeff 
        img_path = '{}/k-coefficient_analysis/visualisations/K-Coefficients Summary.png'.format(img_import_path)
        
        
        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,150)
        pdf.cell(190,10, align = 'L', txt='K-Coefficient')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,160)
        pdf.multi_cell(190, 5 , align = 'L', txt='K > 0 indicates relatively long fixations succeeded by short saccades, implying focal vision. K < 0 indicates relatively short fixations succeeded by long saccades, implying ambient vision.')

        # image
        # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        if img_w > 190:
            # place image
            pdf.set_xy(10,185) 
            pdf.image(img_path, link='', type='PNG', w = 190) 
            # place frame
            img_h = 190/wh_ratio
            pdf.set_xy(10,185)
            pdf.cell(w=190, h=img_h, border=1)

        else:
            # place image
            pdf.set_xy(10,185) 
            pdf.image(img_path, link='', type='PNG', h = 80)
            # place frame
            pdf.set_xy(10,185)
            pdf.cell(w=img_w, h=80, border=1)


        if action_analysis == True:
            # third metric (no title): k-coefficient per action
            pdf.add_page()
            img_path = '{}/k-coefficient_analysis/visualisations/K-Coefficients Summary per action.png'.format(img_import_path)
            
            
            # title of metric
            pdf.set_font('Arial', 'B', 12)
            pdf.set_xy(10,20)
            pdf.cell(190,10, align = 'L', txt='Average K-Coefficients per Action')

            # description
            pdf.set_font('Arial', '', 12)
            pdf.set_xy(10,30)
            pdf.multi_cell(190, 5 , align = 'L', txt='See Average K-Coefficient.')

            # image
            # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
            img = cv2.imread(img_path)
            h, w, c = img.shape
            wh_ratio = w/h
            img_w = 80*wh_ratio
            if img_w > 190:
                # place image
                pdf.set_xy(10,45) 
                pdf.image(img_path, link='', type='PNG', w = 190) 
                # place frame
                img_h = 190/wh_ratio
                pdf.set_xy(10,45) 
                pdf.cell(w=190, h=img_h, border=1)

            else:
                # place image
                pdf.set_xy(10,45) 
                pdf.image(img_path, link='', type='PNG', h = 80)
                # place frame
                pdf.set_xy(10,45)
                pdf.cell(w=img_w, h=80, border=1)



    ### ATTENTION
    if ooi_analysis == True:

        pdf.add_page()

        ### set sub-title of analysis: attention
        pdf.set_font('Arial', 'B', 16)
        pdf.set_xy(10,10)
        pdf.cell(190,10, txt='3) Attention / Object of Interest-based Analysis', align='C')


        ### first metric: hits per OOI
        img_path = '{}/ooi_analysis/visualisations/Hits per OOI_barplot_Whole Trial.png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,20)
        pdf.cell(190,10, align = 'L', txt='Hits per OOI')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,30)
        pdf.multi_cell(190, 5 , align = 'L', txt='The amount of fixations that were identified on the respective object of interest. In general, the more hits an object has, the higher its importance.')

        # image
        # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        if img_w > 190:
            # place image
            pdf.set_xy(10,45) 
            pdf.image(img_path, link='', type='PNG', w = 190) 
            # place frame
            img_h = 190/wh_ratio
            pdf.set_xy(10,45) 
            pdf.cell(w=190, h=img_h, border=1)

        else:
            # place image
            pdf.set_xy(10,45) 
            pdf.image(img_path, link='', type='PNG', h = 80)
            # place frame
            pdf.set_xy(10,45)
            pdf.cell(w=img_w, h=80, border=1)




        ### second metric: time to first fixation
        img_path =  '{}/ooi_analysis/visualisations/Time to First Fixation [ms] per OOI_barplot_Whole Trial.png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,145)
        pdf.cell(190,10, align = 'L', txt='Time to First Fixation per OOI')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,155)
        pdf.multi_cell(190, 5 , align = 'L', txt='The average time [ms] until the first fixation on a specific object took place. In general, the less time passes until the object is noticed, the higher its importance or the more noticeable it is.')


        # image
        # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        if img_w > 190:
            # place image
            pdf.set_xy(10,170) 
            pdf.image(img_path, link='', type='PNG', w = 190) 
            # place frame
            img_h = 190/wh_ratio
            pdf.set_xy(10,170)
            pdf.cell(w=190, h=img_h, border=1)

        else:
            # place image
            pdf.set_xy(10,170) 
            pdf.image(img_path, link='', type='PNG', h = 80)
            # place frame
            pdf.set_xy(10,170)
            pdf.cell(w=img_w, h=80, border=1)




        ### third metric: Relative Dwell Time [%] per OOI
        img_path =  '{}/ooi_analysis/visualisations/Relative Dwell Time [%] per OOI_piechart_Whole Trial.png'.format(img_import_path)

        # new page
        pdf.add_page()

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,20)
        pdf.cell(190,10, align = 'L', txt='Relative Dwell Time per OOI')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,30)
        pdf.multi_cell(190, 5 , align = 'L', txt='The relative amount of time the participants\' gaze was focused on each OOI. In general, the higher the percentage of dwell time, the higher the objects\' importance.')

        # image
        # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        if img_w > 190:
            # place image
            pdf.set_xy(10,55) 
            pdf.image(img_path, link='', type='PNG', w = 190) 
            # place frame
            img_h = 190/wh_ratio
            pdf.set_xy(10,55) 
            pdf.cell(w=190, h=img_h, border=1)

        else:
            # place image
            pdf.set_xy(10,55) 
            pdf.image(img_path, link='', type='PNG', h = 80)
            # place frame
            pdf.set_xy(10,55)
            pdf.cell(w=img_w, h=80, border=1)



        # fourth metric: Average Fixation Time [ms] per OOI_barplot_Whole Trial.png
        img_path =  '{}/ooi_analysis/visualisations/Average Fixation Time [ms] per OOI_boxplot_Whole Trial.png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,145)
        pdf.cell(190,10, align = 'L', txt='Average Fixation Time per OOI')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,155)
        pdf.multi_cell(190, 5 , align = 'L', txt='The average fixation time per OOI is the mean duration of all fixations placed onto a particular OOI. Generally, higher fixation durations can be associated with more focus, concentration or interest.')
        
        # image
        # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        if img_w > 190:
            # place image
            pdf.set_xy(10,180) 
            pdf.image(img_path, link='', type='PNG', w = 190) 
            # place frame
            img_h = 190/wh_ratio
            pdf.set_xy(10,160) 
            pdf.cell(w=190, h=img_h, border=1)

        else:
            # place image
            pdf.set_xy(10,180) 
            pdf.image(img_path, link='', type='PNG', h = 80)
            # place frame
            pdf.set_xy(10,180)
            pdf.cell(w=img_w, h=80, border=1)


    pdf.output(results_path / 'Results_Summary_{}.pdf'.format(level), 'F')



### results per participant

def participants_results(img_import_path, results_path, ooi_analysis, kcoeff_analysis, action_analysis, level):
    
    ### SUMMARY OF GAZE ANALYSIS: PARTICIPANT

    pdf = FPDF(unit='mm')
    pdf.add_page()

    # set title of the document
    pdf.set_font('Arial', 'B', 18)
    pdf.set_xy(10,10)
    pdf.cell(190, 20, 'Summary of Gaze Analysis - {}'.format(level), 1, 1, 'C')

    
    
    ### EFFICIENCY
    # (below title)

    pdf.set_font('Arial', 'B', 16)
    pdf.set_xy(10,35)
    pdf.cell(190,10, txt='1) Efficiency', align='C')


    ### first metric: total duration
    img_path = '{}/general_analysis/visualisations/Total Duration [ms]_barplot_Whole Trial.png'.format(img_import_path)

    # title of metric
    pdf.set_font('Arial', 'B', 12)
    pdf.set_xy(10,45)
    pdf.cell(190,10, align = 'L', txt='Total Duration')

    # description
    pdf.set_font('Arial', '', 12)
    pdf.set_xy(10,55)
    pdf.multi_cell(190, 5 , align = 'L', txt='The average time [ms] it has taken the participants to complete the task. Generally, the shorter the duration, the more efficient the execution, and the higher the expertise.')

    # image
    # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
    img = cv2.imread(img_path)
    h, w, c = img.shape
    wh_ratio = w/h
    img_w = 80*wh_ratio
    if img_w > 190:
        # place image
        pdf.set_xy(10,70) 
        pdf.image(img_path, link='', type='PNG', w = 190) 
        # place frame
        img_h = 190/wh_ratio
        pdf.set_xy(10,70) 
        pdf.cell(w=190, h=img_h, border=1)

    else:
        # place image
        pdf.set_xy(10,70) 
        pdf.image(img_path, link='', type='PNG', h = 80)
        # place frame
        pdf.set_xy(10,70)
        pdf.cell(w=img_w, h=80, border=1)




    ### second metric (title page): total fixations
    img_path =  '{}/general_analysis/visualisations/Number of Fixations_barplot_Whole Trial.png'.format(img_import_path)

    # title of metric
    pdf.set_font('Arial', 'B', 12)
    pdf.set_xy(10,160)
    pdf.cell(190,10, align = 'L', txt='Number of Fixations')

    # description
    pdf.set_font('Arial', '', 12)
    pdf.set_xy(10,170)
    pdf.multi_cell(190, 5 , align = 'L', txt='The average number of fixations per trial. Naturally, this number strongly correlates with the trial duration. Therefore, it is only useful if it is either normalised or if all recordings of a study have the same length. Generally, the number of fixations decreases with increasing expertise and efficiency.')


    # image
    # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
    img = cv2.imread(img_path)
    h, w, c = img.shape
    wh_ratio = w/h
    img_w = 80*wh_ratio
    if img_w > 190:
        # place image
        pdf.set_xy(10,195) 
        pdf.image(img_path, link='', type='PNG', w = 190) 
        # place frame
        img_h = 190/wh_ratio
        pdf.set_xy(10,195)
        pdf.cell(w=190, h=img_h, border=1)

    else:
        # place image
        pdf.set_xy(10, 195) 
        pdf.image(img_path, link='', type='PNG', h = 80)
        # place frame
        pdf.set_xy(10,195)
        pdf.cell(w=img_w, h=80, border=1)


    ### if ooi analysis and action analysis:
    if ooi_analysis == True and action_analysis == True:

        pdf.add_page()

        ## third metric (page without titles): duration per action
        img_path = '{}/general_analysis/visualisations/Duration per Action [ms].png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,20)
        pdf.cell(190,10, align = 'L', txt='Average Duration per Action')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,30)
        pdf.multi_cell(190, 5 , align = 'L', txt='The average time [ms] it has taken the participant to complete each of the identified actions. Similar to "Total Duration", the faster they were, the more efficient the task was performed.')

        # image
        # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        if img_w > 190:
            # place image
            pdf.set_xy(10,55) 
            pdf.image(img_path, link='', type='PNG', w = 190) 
            # place frame
            img_h = 190/wh_ratio
            pdf.set_xy(10,55) 
            pdf.cell(w=190, h=img_h, border=1)

        else:
            # place image
            pdf.set_xy(10,55) 
            pdf.image(img_path, link='', type='PNG', h = 80)
            # place frame
            pdf.set_xy(10,55)
            pdf.cell(w=img_w, h=80, border=1)



        ## fourth metric (page without titles): average dwell time
        img_path =  '{}/ooi_analysis/visualisations/Average Dwell Time [ms]_barplot_Whole Trial.png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,145)
        pdf.cell(190,10, align = 'L', txt='Average Dwell Time')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,155)
        pdf.multi_cell(190, 5 , align = 'L', txt='The average duration per dwell [ms] on the defined OOIs. Longer dwell times can mean that the chosen OOIs keep up the attention for longer individual time periods.')


        # image
        # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        if img_w > 190:
            # place image
            pdf.set_xy(10,180) 
            pdf.image(img_path, link='', type='PNG', w = 190) 
            # place frame
            img_h = 190/wh_ratio
            pdf.set_xy(10,180) 
            pdf.cell(w=190, h=img_h, border=1)

        else:
            # place image
            pdf.set_xy(10,180) 
            pdf.image(img_path, link='', type='PNG', h = 80)
            # place frame
            pdf.set_xy(10,180)
            pdf.cell(w=img_w, h=80, border=1)




    ### if only ooi analysis, no action analysis
    if ooi_analysis == True and action_analysis == False:

        pdf.add_page()

        ## third metric (page without titles): average dwell time
        img_path = '{}/ooi_analysis/visualisations/Average Dwell Time [ms]_barplot_Whole Trial.png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,20)
        pdf.cell(190,10, align = 'L', txt='Average Dwell Time')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,30)
        pdf.multi_cell(190, 5 , align = 'L', txt='The average duration per dwell [ms] on the defined OOI. Longer dwell times can mean that the chosen OOIs keep up the attention for longer individual time periods.')

        # image
        # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        if img_w > 190:
            # place image
            pdf.set_xy(10,55) 
            pdf.image(img_path, link='', type='PNG', w = 190) 
            # place frame
            img_h = 190/wh_ratio
            pdf.set_xy(10,55) 
            pdf.cell(w=190, h=img_h, border=1)

        else:
            # place image
            pdf.set_xy(10,55) 
            pdf.image(img_path, link='', type='PNG', h = 80)
            # place frame
            pdf.set_xy(10,55)
            pdf.cell(w=img_w, h=80, border=1)



    ## if only action analysis, no ooi analysis
    if ooi_analysis == False and action_analysis == True:

        pdf.add_page()

        ## third metric (page without titles): duration per step -> to be done:O
        img_path = '{}/general_analysis/visualisations/Duration per Action [ms].png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,20)
        pdf.cell(190,10, align = 'L', txt='Average Duration per Action')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,30)
        pdf.multi_cell(190, 5 , align = 'L', txt='The average time [ms] it has taken the participant to complete each of the identified actions. Similar to "Total Duration", the faster they were, the more efficient the task was performed.')

        # image
        # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        if img_w > 190:
            # place image
            pdf.set_xy(10,55) 
            pdf.image(img_path, link='', type='PNG', w = 190) 
            # place frame
            img_h = 190/wh_ratio
            pdf.set_xy(10,55) 
            pdf.cell(w=190, h=img_h, border=1)

        else:
            # place image
            pdf.set_xy(10,55) 
            pdf.image(img_path, link='', type='PNG', h = 80)
            # place frame
            pdf.set_xy(10,55)
            pdf.cell(w=img_w, h=80, border=1)



    ### FOCUS

    pdf.add_page()


    pdf.set_font('Arial', 'B', 16)
    pdf.set_xy(10,10)
    pdf.cell(190,10, txt='2) Focus', align='C')



    # first metric (on focus title page)): fixation/saccade duration
    img_path = '{}/general_analysis/visualisations/Relative Fixation Saccade Duration [%]_piecharts_Whole Trial.png'.format(img_import_path)

    # title of metric
    pdf.set_font('Arial', 'B', 12)
    pdf.set_xy(10,25)
    pdf.cell(190,10, align = 'L', txt='Relative Fixation/Saccade Duration')

    # description
    pdf.set_font('Arial', '', 12)
    pdf.set_xy(10,35)
    pdf.multi_cell(190, 5 , align = 'L', txt='Relative percentage of fixation and saccade durations, i.e. the total time the person has spent fixating compared to travelling from one fixation to the next. The higher the ratio, the more time is spent processing compared to searching.')

    # image
    # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
    img = cv2.imread(img_path)
    h, w, c = img.shape
    wh_ratio = w/h
    img_w = 80*wh_ratio
    if img_w > 190:
        # place image
        pdf.set_xy(10,60) 
        pdf.image(img_path, link='', type='PNG', w = 190) 
        # place frame
        img_h = 190/wh_ratio
        pdf.set_xy(10,60)
        pdf.cell(w=190, h=img_h, border=1)

    else:
        # place image
        pdf.set_xy(10,60) 
        pdf.image(img_path, link='', type='PNG', h = 80)
        # place frame
        pdf.set_xy(10,60)
        pdf.cell(w=img_w, h=80, border=1)




    # if ooi analysis
    if ooi_analysis == True:
        
        # second metric first focus page: Normalised Stationary Gaze Entropy
        img_path =  '{}/ooi_analysis/visualisations/Normalised Stationary Gaze Entropy_barplot_Whole Trial.png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,150)
        pdf.cell(190,10, align = 'L', txt='Normalised Stationary Gaze Entropy')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,160)
        pdf.multi_cell(190, 5 , align = 'L', txt='A higher SGE implies a more equal distribution of the visual attention between the OOIs. A lower value reflects when fixations tend to be concentrated on specific OOIs, either because they are more complex or more interesting to the subject.')

        # image
        # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        if img_w > 190:
            # place image
            pdf.set_xy(10,185) 
            pdf.image(img_path, link='', type='PNG', w = 190) 
            # place frame
            img_h = 190/wh_ratio
            pdf.set_xy(10,185) 
            pdf.cell(w=190, h=img_h, border=1)

        else:
            # place image
            pdf.set_xy(10,185) 
            pdf.image(img_path, link='', type='PNG', h = 80)
            # place frame
            pdf.set_xy(10,185)
            pdf.cell(w=img_w, h=80, border=1)

        
        
        
        
        # third metric (no title): Normalised Gaze Transition Entropy
        pdf.add_page()
        img_path = '{}/ooi_analysis/visualisations/Normalised Gaze Transition Entropy_barplot_Whole Trial.png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,20)
        pdf.cell(190,10, align = 'L', txt='Normalised Gaze Transition Entropy')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,30)
        pdf.multi_cell(190, 5 , align = 'L', txt='In short, higher entropy can imply more randomness in the visual scanning pattern and in turn, less focus and efficiency.')

        # image
        # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        if img_w > 190:
            # place image
            pdf.set_xy(10,55) 
            pdf.image(img_path, link='', type='PNG', w = 190) 
            # place frame
            img_h = 190/wh_ratio
            pdf.set_xy(10,55) 
            pdf.cell(w=190, h=img_h, border=1)

        else:
            # place image
            pdf.set_xy(10,55) 
            pdf.image(img_path, link='', type='PNG', h = 80)
            # place frame
            pdf.set_xy(10,55)
            pdf.cell(w=img_w, h=80, border=1)




        # if k-coeff analysis
        if kcoeff_analysis == True:
            
        
            ## fourth metric (no title page): kcoeff
            img_path = '{}/k-coefficient_analysis/visualisations/K-Coefficients Summary.png'.format(img_import_path)

            # title of metric
            pdf.set_font('Arial', 'B', 12)
            pdf.set_xy(10,145)
            pdf.cell(190,10, align = 'L', txt='Average K-Coefficients')

            # description
            pdf.set_font('Arial', '', 12)
            pdf.set_xy(10,155)
            pdf.multi_cell(190, 5 , align = 'L', txt='K > 0 indicates relatively long fixations succeeded by short saccades, implying focal vision. K < 0 indicates relatively short fixations succeeded by long saccades, implying ambient vision.')

            # image
            # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
            img = cv2.imread(img_path)
            h, w, c = img.shape
            wh_ratio = w/h
            img_w = 80*wh_ratio
            if img_w > 190:
                # place image
                pdf.set_xy(10,180) 
                pdf.image(img_path, link='', type='PNG', w = 190) 
                # place frame
                img_h = 190/wh_ratio
                pdf.set_xy(10,180) 
                pdf.cell(w=190, h=img_h, border=1)

            else:
                # place image
                pdf.set_xy(10,180) 
                pdf.image(img_path, link='', type='PNG', h = 80)
                # place frame
                pdf.set_xy(10,180)
                pdf.cell(w=img_w, h=80, border=1)


            if action_analysis == True:

                # fifth metric
                pdf.add_page()  
                img_path = '{}/k-coefficient_analysis/visualisations/K-Coefficients Summary per action.png'.format(img_import_path)

                # title of metric
                pdf.set_font('Arial', 'B', 12)
                pdf.set_xy(10,20)
                pdf.cell(190,10, align = 'L', txt='Average K-Coefficients per Action')

                # description
                pdf.set_font('Arial', '', 12)
                pdf.set_xy(10,30)
                pdf.multi_cell(190, 5 , align = 'L', txt='K > 0 indicates relatively long fixations succeeded by short saccades, implying focal vision. K < 0 indicates relatively short fixations succeeded by long saccades, implying ambient vision.')

                # image
                # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
                img = cv2.imread(img_path)
                h, w, c = img.shape
                wh_ratio = w/h
                img_w = 80*wh_ratio
                if img_w > 190:
                    # place image
                    pdf.set_xy(10,55) 
                    pdf.image(img_path, link='', type='PNG', w = 190) 
                    # place frame
                    img_h = 190/wh_ratio
                    pdf.set_xy(10,55) 
                    pdf.cell(w=190, h=img_h, border=1)

                else:
                    # place image
                    pdf.set_xy(10,55) 
                    pdf.image(img_path, link='', type='PNG', h = 80)
                    # place frame
                    pdf.set_xy(10,55)
                    pdf.cell(w=img_w, h=80, border=1)


    if ooi_analysis == False and kcoeff_analysis == True:
        # second metric first focus page: kcoeff 
        img_path = '{}/k-coefficient_analysis/visualisations/K-Coefficients Summary.png'.format(img_import_path)
        
        
        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,150)
        pdf.cell(190,10, align = 'L', txt='K-Coefficient')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,160)
        pdf.multi_cell(190, 5 , align = 'L', txt='K > 0 indicates relatively long fixations succeeded by short saccades, implying focal vision. K < 0 indicates relatively short fixations succeeded by long saccades, implying ambient vision.')

        # image
        # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        if img_w > 190:
            # place image
            pdf.set_xy(10,185) 
            pdf.image(img_path, link='', type='PNG', w = 190) 
            # place frame
            img_h = 190/wh_ratio
            pdf.set_xy(10,185)
            pdf.cell(w=190, h=img_h, border=1)

        else:
            # place image
            pdf.set_xy(10,185) 
            pdf.image(img_path, link='', type='PNG', h = 80)
            # place frame
            pdf.set_xy(10,185)
            pdf.cell(w=img_w, h=80, border=1)


        if action_analysis == True:
            # third metric (no title): k-coefficient per action
            pdf.add_page()
            img_path = '{}/k-coefficient_analysis/visualisations/K-Coefficients Summary per action.png'.format(img_import_path)
            
            
            # title of metric
            pdf.set_font('Arial', 'B', 12)
            pdf.set_xy(10,20)
            pdf.cell(190,10, align = 'L', txt='Average K-Coefficients per Action')

            # description
            pdf.set_font('Arial', '', 12)
            pdf.set_xy(10,30)
            pdf.multi_cell(190, 5 , align = 'L', txt='See Average K-Coefficient.')

            # image
            # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
            img = cv2.imread(img_path)
            h, w, c = img.shape
            wh_ratio = w/h
            img_w = 80*wh_ratio
            if img_w > 190:
                # place image
                pdf.set_xy(10,55) 
                pdf.image(img_path, link='', type='PNG', w = 190) 
                # place frame
                img_h = 190/wh_ratio
                pdf.set_xy(10,55) 
                pdf.cell(w=190, h=img_h, border=1)

            else:
                # place image
                pdf.set_xy(10,55) 
                pdf.image(img_path, link='', type='PNG', h = 80)
                # place frame
                pdf.set_xy(10,55)
                pdf.cell(w=img_w, h=80, border=1)



    ### ATTENTION
    if ooi_analysis == True:

        pdf.add_page()

        ### set sub-title of analysis: attention
        pdf.set_font('Arial', 'B', 16)
        pdf.set_xy(10,10)
        pdf.cell(190,10, txt='3) Attention / Object of Interest-based Analysis', align='C')


        ### first metric: hits per OOI
        img_path = '{}/ooi_analysis/visualisations/Hits per OOI_barplot_Whole Trial.png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,20)
        pdf.cell(190,10, align = 'L', txt='Hits per OOI')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,30)
        pdf.multi_cell(190, 5 , align = 'L', txt='The amount of fixations that were identified on the respective object of interest. In general, the more hits an object has, the higher its importance.')

        # image
        # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        if img_w > 190:
            # place image
            pdf.set_xy(10,55) 
            pdf.image(img_path, link='', type='PNG', w = 190) 
            # place frame
            img_h = 190/wh_ratio
            pdf.set_xy(10,55)
            pdf.cell(w=190, h=img_h, border=1)

        else:
            # place image
            pdf.set_xy(10,55) 
            pdf.image(img_path, link='', type='PNG', h = 80)
            # place frame
            pdf.set_xy(10,55)
            pdf.cell(w=img_w, h=80, border=1)




        ### second metric: time to first fixation
        img_path =  '{}/ooi_analysis/visualisations/Time to First Fixation [ms] per OOI_barplot_Whole Trial.png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,145)
        pdf.cell(190,10, align = 'L', txt='Time to First Fixation per OOI')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,155)
        pdf.multi_cell(190, 5 , align = 'L', txt='The average time [ms] until the first fixation on a specific object took place. In general, the less time passes until the object is noticed, the higher its importance or the more noticeable it is.')


        # image
        # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        if img_w > 190:
            # place image
            pdf.set_xy(10,180) 
            pdf.image(img_path, link='', type='PNG', w = 190) 
            # place frame
            img_h = 190/wh_ratio
            pdf.set_xy(10,180) 
            pdf.cell(w=190, h=img_h, border=1)

        else:
            # place image
            pdf.set_xy(10,180) 
            pdf.image(img_path, link='', type='PNG', h = 80)
            # place frame
            pdf.set_xy(10,180)
            pdf.cell(w=img_w, h=80, border=1)




        ### third metric: Relative Dwell Time [%] per OOI
        img_path =  '{}/ooi_analysis/visualisations/Relative Dwell Time [%] per OOI_piechart_Whole Trial.png'.format(img_import_path)

        # new page
        pdf.add_page()

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,20)
        pdf.cell(190,10, align = 'L', txt='Relative Dwell Time per OOI')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,30)
        pdf.multi_cell(190, 5 , align = 'L', txt='The relative amount of time the participants\' gaze was focused on each OOI. In general, the higher the percentage of dwell time, the higher the objects\' importance.')

        # image
        # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        if img_w > 190:
            # place image
            pdf.set_xy(10,55) 
            pdf.image(img_path, link='', type='PNG', w = 190) 
            # place frame
            img_h = 190/wh_ratio
            pdf.set_xy(10,55) 
            pdf.cell(w=190, h=img_h, border=1)

        else:
            # place image
            pdf.set_xy(10,55) 
            pdf.image(img_path, link='', type='PNG', h = 80)
            # place frame
            pdf.set_xy(10,55)
            pdf.cell(w=img_w, h=80, border=1)



        # fourth metric: Average Fixation Time [ms] per OOI_barplot_Whole Trial.png
        img_path =  '{}/ooi_analysis/visualisations/Average Fixation Time [ms] per OOI_barplot_Whole Trial.png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,145)
        pdf.cell(190,10, align = 'L', txt='Average Fixation Time per OOI')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,155)
        pdf.multi_cell(190, 5 , align = 'L', txt='The average fixation time per OOI is the mean duration of all fixations placed onto a particular OOI. Generally, higher fixation durations can be associated with more focus, concentration or interest.')
        
        # image
        # calculate image width from ration (if width is >190 at a height of 80, make w = 190) 
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        if img_w > 190:
            # place image
            pdf.set_xy(10,180) 
            pdf.image(img_path, link='', type='PNG', w = 190) 
            # place frame
            img_h = 190/wh_ratio
            pdf.set_xy(10,180) 
            pdf.cell(w=190, h=img_h, border=1)

        else:
            # place image
            pdf.set_xy(10,180) 
            pdf.image(img_path, link='', type='PNG', h = 80)
            # place frame
            pdf.set_xy(10,180)
            pdf.cell(w=img_w, h=80, border=1)


    pdf.output(results_path / 'Results_Summary_{}.pdf'.format(level), 'F')







### generate results manually separately from main.py


# which analyses took place? 
# general_analysis: always true 
#ooi_analysis = True
#kcoeff_analysis = True
#action_analysis = True

#level = 'participant03'
#img_import_path = 'Output_backup/group_easy/participant03'
#results_path = Path('Summary_Report_Sep/group_easy/participant03')
#os.makedirs(results_path, exist_ok = True)

#allgroups_groups_results(img_import_path, results_path, ooi_analysis, kcoeff_analysis, action_analysis, level)
#participants_results(img_import_path, results_path, ooi_analysis, kcoeff_analysis, action_analysis, level)
