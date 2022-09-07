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
    plt.title('Relative Dwelltime [%] per OOI ({})'.format(specification), fontsize = 16, pad = 20, weight = 'bold')
    plt.savefig(savepath, bbox_inches = 'tight', dpi = 300)

 

        