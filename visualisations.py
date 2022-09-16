# load packages
from cmath import pi
from matplotlib.image import FigureImage
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# save general metrics from df_gen
def vis_gen_metrics(df, sac_dur_list, fix_dur_list, outputpath, filename, specification, x_labels):

    # barplots: all general metrics except relative

    for col in range(len(df.columns)-1):    # -1 because of relative percentage (in last column) that cannot be plotted 


        savepath = outputpath / '{}_barplot_{}'.format(df.columns[col], specification)
        sns.set_theme(style='whitegrid')
        barplot = sns.barplot(x=df.index.values[:-1], y=df.iloc[:-1,col], color='mediumseagreen')
        plt.title('{} ({})'.format(df.columns[col], specification), fontsize = 16, pad = 20, weight = 'bold')
        plt.text(1.1,1.1, filename, transform=plt.gca().transAxes)
        plt.ylabel(df.columns[col],  labelpad=20)
        fig = barplot.get_figure()
        fig.savefig(savepath, bbox_inches='tight', dpi=300)
        plt.clf()


    # boxplots: saccade duration
    savepath=outputpath /'Average Saccade Duration [ms]_boxplot_{}.jpg'.format(specification)
    sns.set_theme(style='whitegrid')
    boxplot = sns.boxplot(data=sac_dur_list, color='mediumseagreen')
    boxplot.set_xticklabels(x_labels)
    plt.title('Average Saccade Duration ({})'.format(specification), fontsize = 16, pad = 20, weight = 'bold')
    plt.text(1.1,1.1, filename, transform=plt.gca().transAxes)
    fig = boxplot.get_figure()
    fig.savefig(savepath, bbox_inches='tight', dpi=300)
    plt.clf()


    # boxplots: fixation duration
    savepath=outputpath /'Average Fixation Duration [ms]_boxplot_{}.jpg'.format(specification)
    boxplot = sns.boxplot(data=fix_dur_list, color='mediumseagreen')
    boxplot.set_xticklabels(x_labels)
    plt.title('Average Fixation Duration ({})'.format(specification), fontsize = 16, pad = 20, weight = 'bold')
    plt.text(1.1,1.1, filename, transform=plt.gca().transAxes)
    fig = boxplot.get_figure()
    fig.savefig(savepath, bbox_inches='tight', dpi=300)
    plt.clf()

    # relative fixation/saccade duration pie chart

    
    

    




    



# save ooi-based ooi metrics from df_ooi 
def vis_ooi_metrics(df, outputpath, filename, specification):
    
    # barplots for all metrics
    for i in range(len(df)):
        savepath=outputpath /'{}_barplot_{}.jpg'.format(df.index[i], specification)
        sns.set_theme(style='whitegrid')
        barplot = sns.barplot(df.columns, df.iloc[i], color='mediumseagreen')
        plt.title('{} per OOI ({})'.format(df.index[i], specification), fontsize = 16, pad = 20, weight = 'bold')
        plt.text(1.1,1.1, filename, transform=plt.gca().transAxes)
        plt.ylabel(df.index[i],  labelpad=20)
        fig = barplot.get_figure()
        fig.savefig(savepath, bbox_inches='tight', dpi=300)
        plt.clf()

    # cake plot for Relative Dwelltime [%]:

    # only plot if greater than 0% 
    piedata = df.loc['Relative Dwelltime [%]'] 
    piedata = piedata[piedata!=0]

    # make pie chart
    savepath=outputpath /'{}_pieplot_{}.jpg'.format('Relative Dwelltime [%]', specification)
    number_cols = len(piedata)
    clrs = sns.color_palette('pastel')[0:number_cols]
    lbls = piedata.index
    plt.pie(piedata, labels = lbls, colors = clrs, autopct='%.0f%%' )
    plt.text(1.3,1.1, filename, transform=plt.gca().transAxes)
    plt.title('Relative Dwelltime [%] per OOI ({})'.format(specification), fontsize = 16, pad = 20, weight = 'bold')
    #plt.tight_layout()
    plt.savefig(savepath, bbox_inches = 'tight', dpi = 300)
    plt.clf()






# visualisation transition matrix
def vis_transition_matrix(transition_matrix, dict_ooi, outputpath, trialname, specification):
    # switch key and value in dict_ooi
    dict_ooi_switched = {y: x for x, y in dict_ooi.items()}
    df_tm = pd.DataFrame(transition_matrix)
    df_tm.columns = df_tm.columns.map(dict_ooi_switched)
    df_tm.index = df_tm.index.map(dict_ooi_switched)

    # create path to save
    savepath=outputpath /'Transition Matrix (GTE)_{}.jpg'.format(specification)

    
    sns.color_palette('pastel')[0:len(df_tm)]
    sns.heatmap(df_tm, annot=True)
    sns.axes_style({'ytick.top': True})
    plt.tick_params(axis='both', which='major', labelsize=10, labelbottom = False, bottom=False, top = False, labeltop=True)
    plt.text(1.3,1.1, trialname, transform=plt.gca().transAxes)
    plt.title('Transition Matrix ({})'.format(specification), fontsize = 16, pad = 20, weight = 'bold')
    #plt.tight_layout()
    plt.savefig(savepath, bbox_inches = 'tight', dpi = 300)
    plt.clf()

    e=3


# visualisation of k-coefficient
def vis_kcoeff(df, outputpath, trialname, specification):
        savepath=outputpath /'K-Coefficient_{}.jpg'.format(specification)
        sns.set_theme(style='whitegrid')
        lineplot = sns.lineplot(df['start_time'], df['K-coefficient'], color='mediumseagreen')
        plt.title('K-Coefficient ({})'.format(specification), fontsize = 16, pad = 20, weight = 'bold')
        plt.text(1.1,1.1, trialname, transform=plt.gca().transAxes)
        plt.ylabel('K-Coefficient',  labelpad=20)
        plt.xlabel('Time [ms]',  labelpad=20)
        fig = lineplot.get_figure()
        fig.savefig(savepath, bbox_inches='tight', dpi=300)
        plt.clf()