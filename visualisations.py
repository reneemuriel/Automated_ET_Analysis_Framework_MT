# load packages
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

 

        