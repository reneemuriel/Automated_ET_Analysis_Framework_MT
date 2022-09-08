# load packages
from cmath import pi
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# save ooi-based ooi metrics from df_ooi 
def vis_ooi_metrics(df, outputpath, trialname, specification):
    
    # barplots for all metrics
    for i in range(len(df)):
        savepath=outputpath /'{}_barplot_{}.jpg'.format(df.index[i], specification)
        sns.set_theme(style='whitegrid')
        barplot = sns.barplot(df.columns, df.iloc[i], color='mediumseagreen')
        plt.title('{} per OOI ({})'.format(df.index[i], specification), fontsize = 16, pad = 20, weight = 'bold')
        plt.text(1.1,1.1, trialname, transform=plt.gca().transAxes)
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
    plt.text(1.3,1.1, trialname, transform=plt.gca().transAxes)
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