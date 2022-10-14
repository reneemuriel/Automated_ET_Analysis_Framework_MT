import pandas as pd
from matplotlib import image
from pathlib import Path
import cv2
from fpdf import FPDF

"""
Attention
    Hits per OOI
    Time to first fixation per OOI
    Relative dwell time per OOI
    Average Fixation Duration per OOI

Focus
    K-Coefficient
    Entropy
    Fixation/saccade time ratio


Efficiency
    Average dwell time per OOI 
    Duration per step / Total duration
    Total fixations

"""

ooi_analysis = True
kcoeff_analysis = True
action_analysis = True
img_import_path = 'Output'

### results 
def allgroups_results(img_import_path, ooi_analysis, kcoeff_analysis, action_analysis):
    
    ### SUMMARY OF GAZE ANALYSIS: ALL GROUPS

    pdf = FPDF(unit='mm')
    pdf.add_page()

    # set title of the document
    pdf.set_font('Arial', 'B', 18)
    pdf.set_xy(10,10)
    pdf.cell(190, 20, 'Summary of Gaze Analysis - All Groups', 1, 1, 'C')


    
    
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
    pdf.cell(190,10, align = 'L', txt='Total Duration [ms]')

    # description
    pdf.set_font('Arial', '', 12)
    pdf.set_xy(10,55)
    pdf.multi_cell(190, 5 , align = 'L', txt='The average time [ms] the participants\' have taken to complete the task. of fixations that were identified on the respective object of interest. The less time they took, the more efficient they were.')

    # image
    # place image
    pdf.set_xy(10,70) 
    pdf.image(img_path, link='', type='PNG', h = 80) 
    # calculate image width from ration and place frame
    img = cv2.imread(img_path)
    h, w, c = img.shape
    wh_ratio = w/h
    img_w = 80*wh_ratio
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
    pdf.multi_cell(190, 5 , align = 'L', txt='The average number of fixations over the entire trial. In general, the more fixations, the less efficient.')


    # image
    # place image
    pdf.set_xy(10,185) 
    pdf.image(img_path, link='', type='PNG', h = 80) 
    # calculate image width from ration and place frame
    img = cv2.imread(img_path)
    h, w, c = img.shape
    wh_ratio = w/h
    img_w = 80*wh_ratio
    pdf.set_xy(10,185) 
    pdf.cell(w=img_w, h=80, border=1)


    ### if ooi analysis and action analysis:
    if ooi_analysis == True and action_analysis == True:

        pdf.add_page()

        ## third metric (page without titles): duration per step -> to be done:O
        img_path = '{}/ooi_analysis/visualisations/Average Dwell Time [ms]_boxplot_Whole Trial.png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,20)
        pdf.cell(190,10, align = 'L', txt='Average Duration per Step')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,30)
        pdf.multi_cell(190, 5 , align = 'L', txt='The average time in miliseconds it has taken the participant(s) to complete each of the identified actions. The faster, the more efficient they were.')

        # image
        # place image
        pdf.set_xy(10,45) 
        pdf.image(img_path, link='', type='PNG', h = 80) 
        # calculate image width from ration and place frame
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        pdf.set_xy(10,45) 
        pdf.cell(w=img_w, h=80, border=1)



        ## fourth metric (page without titles): average dwell time
        img_path =  '{}/ooi_analysis/visualisations/Average Dwell Time [ms]_boxplot_Whole Trial.png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,135)
        pdf.cell(190,10, align = 'L', txt='Average Dwell Time [ms]')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,145)
        pdf.multi_cell(190, 5 , align = 'L', txt='The average duration per dwell in miliseconds on the defined OOI. Generally, the longer the dwell times, the higher the focus and concentration.')


        # image
        # place image
        pdf.set_xy(10,160) 
        pdf.image(img_path, link='', type='PNG', h = 80) 
        # calculate image width from ration and place frame
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        pdf.set_xy(10,150) 
        pdf.cell(w=img_w, h=80, border=1)





    ### if only ooi analysis, no action analysis
    if ooi_analysis == True and action_analysis == False:

        pdf.add_page()

        ## third metric (page without titles): average dwell time
        img_path = '{}/ooi_analysis/visualisations/Average Dwell Time [ms]_boxplot_Whole Trial.png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,20)
        pdf.cell(190,10, align = 'L', txt='Average Dwell Time [ms]')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,30)
        pdf.multi_cell(190, 5 , align = 'L', txt='The average duration per dwell in miliseconds on the defined OOI. Generally, the longer the dwell times, the higher the focus and concentration.')

        # image
        # place image
        pdf.set_xy(10,45) 
        pdf.image(img_path, link='', type='PNG', h = 80) 
        # calculate image width from ration and place frame
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        pdf.set_xy(10,45) 
        pdf.cell(w=img_w, h=80, border=1)



    ## if only action analysis, no ooi analysis
    if ooi_analysis == False and action_analysis == True:

        pdf.add_page()

        ## third metric (page without titles): duration per step -> to be done:O
        img_path = '{}/ooi_analysis/visualisations/Average Dwell Time [ms]_boxplot_Whole Trial.png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,20)
        pdf.cell(190,10, align = 'L', txt='Average Duration per Step')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,30)
        pdf.multi_cell(190, 5 , align = 'L', txt='The average time in miliseconds it has taken the participant(s) to complete each of the identified actions. The faster, the more efficient they were.')

        # image
        # place image
        pdf.set_xy(10,45) 
        pdf.image(img_path, link='', type='PNG', h = 80) 
        # calculate image width from ration and place frame
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        pdf.set_xy(10,45) 
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
    pdf.cell(190,10, align = 'L', txt='Relative Fixation Saccade Duration [%]')

    # description
    pdf.set_font('Arial', '', 12)
    pdf.set_xy(10,35)
    pdf.multi_cell(190, 5 , align = 'L', txt='Relative percentage of fixation and saccade durations.')

    # image
    # place image
    pdf.set_xy(10,50) 
    pdf.image(img_path, link='', type='PNG', h = 80) 
    # calculate image width from ration and place frame
    img = cv2.imread(img_path)
    h, w, c = img.shape
    wh_ratio = w/h
    img_w = 80*wh_ratio
    pdf.set_xy(10,50) 
    pdf.cell(w=img_w, h=80, border=1)



    # if ooi analysis
    if ooi_analysis == True:
        
        # second metric first focus page: Normalised Stationary Gaze Entropy
        img_path =  '{}/ooi_analysis/visualisations/Normalised Stationary Gaze Entropy_barplot_Whole Trial.png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,140)
        pdf.cell(190,10, align = 'L', txt='Normalised Stationary Gaze Entropy')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,150)
        pdf.multi_cell(190, 5 , align = 'L', txt='mimimiiii Normalised Stationary Gaze Entropy')

        # image
        # place image
        pdf.set_xy(10,165) 
        pdf.image(img_path, link='', type='PNG', h = 80) 
        # calculate image width from ration and place frame
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        pdf.set_xy(10,165) 
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
        pdf.multi_cell(190, 5 , align = 'L', txt='Normalised Gaze Transition Entropy desciptiiionn BliblaBlau')

        # image
        # place image
        pdf.set_xy(10,45) 
        pdf.image(img_path, link='', type='PNG', h = 80) 
        # calculate image width from ration and place frame
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        pdf.set_xy(10,45) 
        pdf.cell(w=img_w, h=80, border=1)



        # if k-coeff analysis
        if kcoeff_analysis == True:
            
        
            ## fourth metric (no title page): kcoeff
            img_path = '{}/k-coefficient_analysis/visualisations/All Groups K-Coefficients Summary.png'.format(img_import_path)

            # title of metric
            pdf.set_font('Arial', 'B', 12)
            pdf.set_xy(10,135)
            pdf.cell(190,10, align = 'L', txt='Average K-Coefficients')

            # description
            pdf.set_font('Arial', '', 12)
            pdf.set_xy(10,145)
            pdf.multi_cell(190, 5 , align = 'L', txt='K-Coefficient explained. And outside std dev')

            # image
            # place image
            pdf.set_xy(10,160) 
            pdf.image(img_path, link='', type='PNG', h = 80) 
            # calculate image width from ration and place frame
            img = cv2.imread(img_path)
            h, w, c = img.shape
            wh_ratio = w/h
            img_w = 80*wh_ratio
            pdf.set_xy(10,160) 
            pdf.cell(w=img_w, h=80, border=1)

            if action_analysis == True:

                # fifth metric
                pdf.add_page()  
                #img_path = '{}/k-coefficient_analysis/visualisations/All Groups K-Coefficients Summary per action.png'.format(img_import_path)

                # title of metric
                pdf.set_font('Arial', 'B', 12)
                pdf.set_xy(10,20)
                pdf.cell(190,10, align = 'L', txt='Average K-Coefficients of All Groups per Action')

                # description
                pdf.set_font('Arial', '', 12)
                pdf.set_xy(10,30)
                pdf.multi_cell(190, 5 , align = 'L', txt='K-Coefficient explained. and outside std dev ')

                # image
                # place image
                pdf.set_xy(10,45) 
                pdf.image(img_path, link='', type='PNG', h = 80) 
                # calculate image width from ration and place frame
                img = cv2.imread(img_path)
                h, w, c = img.shape
                wh_ratio = w/h
                img_w = 80*wh_ratio
                pdf.set_xy(10,45) 
                pdf.cell(w=img_w, h=80, border=1)

    if ooi_analysis == False and kcoeff_analysis == True:
        # second metric first focus page: kcoeff 
        img_path = '{}/k-coefficient_analysis/visualisations/All Groups K-Coefficients Summary.png'.format(img_import_path)
        
        
        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,140)
        pdf.cell(190,10, align = 'L', txt='K-Coefficient')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,150)
        pdf.multi_cell(190, 5 , align = 'L', txt='mimimiiii K-Coefficient description')

        # image
        # place image
        pdf.set_xy(10,165) 
        pdf.image(img_path, link='', type='PNG', h = 80) 
        # calculate image width from ration and place frame
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        pdf.set_xy(10,165) 
        pdf.cell(w=img_w, h=80, border=1)

        if action_analysis == True:
            # third metric (no title): k-coefficient per action
            pdf.add_page()
            #img_path = '{}/k-coefficient_analysis/visualisations/All Groups K-Coefficients Summary per action.png'.format(img_import_path)
            
            
            # title of metric
            pdf.set_font('Arial', 'B', 12)
            pdf.set_xy(10,20)
            pdf.cell(190,10, align = 'L', txt='Average K-Coefficients of All Groups per Action')

            # description
            pdf.set_font('Arial', '', 12)
            pdf.set_xy(10,30)
            pdf.multi_cell(190, 5 , align = 'L', txt='descriptionnnn Average K-Coefficients of All Groups per Action')

            # image
            # place image
            pdf.set_xy(10,45) 
            pdf.image(img_path, link='', type='PNG', h = 80) 
            # calculate image width from ration and place frame
            img = cv2.imread(img_path)
            h, w, c = img.shape
            wh_ratio = w/h
            img_w = 80*wh_ratio
            pdf.set_xy(10,45) 
            pdf.cell(w=img_w, h=80, border=1)


















    ### ATTENTION
    if ooi_analysis == True:

        pdf.add_page()

        ### set sub-title of analysis: attention
        pdf.set_font('Arial', 'B', 16)
        pdf.set_xy(10,10)
        pdf.cell(190,10, txt='2) Attention / Object of Interest-based Analysis', align='C')


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
        # place image
        pdf.set_xy(10,45) 
        pdf.image(img_path, link='', type='PNG', h = 80) 
        # calculate image width from ration and place frame
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        pdf.set_xy(10,45) 
        pdf.cell(w=img_w, h=80, border=1)



        ### second metric: time to first fixation
        img_path =  '{}/ooi_analysis/visualisations/Time to First Fixation [ms] per OOI_barplot_Whole Trial.png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,125)
        pdf.cell(190,10, align = 'L', txt='Time to First Fixation [ms] per OOI')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,135)
        pdf.multi_cell(190, 5 , align = 'L', txt='The average time in miliseconds until the first fixation on a specific object took place. In general, the less time passes until the object is noticed, the higher its importance or the more noticeable it is.')


        # image
        # place image
        pdf.set_xy(10,150) 
        pdf.image(img_path, link='', type='PNG', h = 80) 
        # calculate image width from ration and place frame
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        pdf.set_xy(10,150) 
        pdf.cell(w=img_w, h=80, border=1)



        ### third metric: Relative Dwelltime [%] per OOI
        img_path =  '{}/ooi_analysis/visualisations/Relative Dwelltime [%] per OOI_piechart_Whole Trial.png'.format(img_import_path)

        # new page
        pdf.add_page()

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,10)
        pdf.cell(190,10, align = 'L', txt='Relative Dwelltime [%] per OOI')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,20)
        pdf.multi_cell(190, 5 , align = 'L', txt='The relative amount of time the participants\' gaze was focused on each OOI. In general, the higher the percentage of dwell time, the higher the objects\' importance.')

        # image
        # place image
        pdf.set_xy(10,35) 
        pdf.image(img_path, link='', type='PNG', h = 80) 
        # calculate image width from ration and place frame
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        pdf.set_xy(10,35) 
        pdf.cell(w=img_w, h=80, border=1)



        # fourth metric: Average Fixation Time [ms] per OOI_barplot_Whole Trial.png
        img_path =  '{}/ooi_analysis/visualisations/Average Fixation Time [ms] per OOI_barplot_Whole Trial.png'.format(img_import_path)

        # title of metric
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(10,125)
        pdf.cell(190,10, align = 'L', txt='Relative Dwelltime [%] per OOI')

        # description
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10,135)
        pdf.multi_cell(190, 5 , align = 'L', txt='The average duration of a fixation on each OOI. Generally, higher fixation durations are associated with more focus and concentration. (?)')

        # image
        # place image
        pdf.set_xy(10,150) 
        pdf.image(img_path, link='', type='PNG', h = 80) 
        # calculate image width from ration and place frame
        img = cv2.imread(img_path)
        h, w, c = img.shape
        wh_ratio = w/h
        img_w = 80*wh_ratio
        pdf.set_xy(10,150) 
        pdf.cell(w=img_w, h=80, border=1)


    pdf.output('testpdf.pdf', 'F')
    


allgroups_results(img_import_path, ooi_analysis, kcoeff_analysis, action_analysis)

