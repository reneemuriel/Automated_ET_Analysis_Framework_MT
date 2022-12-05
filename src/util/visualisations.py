'''
Contains all visualisations of the framework.
'''

# ignore warnings
import warnings
warnings.filterwarnings('ignore')

# load packages
from cmath import pi
from matplotlib.image import FigureImage
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import re
import numpy as np

# make figures not pop up
matplotlib.use('Agg') 

### GENERAL METRICS
#region

# barplots for all metrics (apart from relative fix / sac duration)
def vis_gen_metrics_barplots(df, outputpath, filename, specification):
    # df: general metrics df
    # outputpath: output directory where file is exported to
    # specification: whole trial or specific action

    # drop fixation/saccade duration
    df_barplots = df.drop('Relative Fixation/Saccade Duration [%]', axis = 1)

    # iterates through general metrics dfs to create barplots for each metric
    for col in range(len(df_barplots.columns)):   
        savepath = outputpath / '{}_barplot_{}'.format(df_barplots.columns[col], specification)
        sns.set_theme(style='whitegrid')
        barplot = sns.barplot(x=df_barplots.index.values[:-1], y=df_barplots.iloc[:-1,col], color='mediumseagreen')
        x_labels = df_barplots.index.values[:-1]
        barplot.set_xticklabels(x_labels, rotation = 90)
        plt.title('{} ({})'.format(df_barplots.columns[col], specification), fontsize = 16, pad = 20, weight = 'bold')
        plt.text(1.1,1.1, filename, transform=plt.gca().transAxes)
        plt.ylabel(df_barplots.columns[col],  labelpad=20)
        fig = barplot.get_figure()
        fig.savefig(savepath, bbox_inches='tight', dpi=300)
        plt.clf()

# boxplots for all metrics (distributions per participant, group, all groups)
def vis_gen_metrics_boxplots_group(nested_list, outputpath, filename, specification, metric, x_labels):
    # nested_list: df of nested lists that contain values of level below in order to get box plot (e.g. boxplots of all groups needs values of each participant to calculate box plot)
    # outputpath: output directory where file is exported to
    # specification: whole trial or specific action
    savepath=outputpath /'{}_boxplot_{}'.format(metric, specification)
    sns.set_theme(style='whitegrid')
    boxplot = sns.boxplot(data=nested_list, color='mediumseagreen')
    boxplot.set_xticklabels(x_labels, rotation = 90) # changed this
    plt.title('{} ({})'.format(metric, specification), fontsize = 16, pad = 20, weight = 'bold')
    plt.text(1.1,1.1, filename, transform=plt.gca().transAxes)
    plt.ylabel(metric,  labelpad=20)               
    fig = boxplot.get_figure()
    fig.savefig(savepath, bbox_inches='tight', dpi=300)
    plt.clf()

# piechart for relative fix / sac duration
def vis_gen_metrics_piechart(df, outputpath, filename, specification):
    # df: general metrics df
    # outputpath: output directory where file is exported to
    # specification: whole trial or specific action

    savepath=outputpath /'{}_piecharts_{}'.format('Relative Fixation Saccade Duration [%]', specification)

    # extract numbers out of the string saved in df
    perc_fixation_list = []
    perc_saccade_list = []
    for row in range(len(df)-1):
        perc_string = df['Relative Fixation/Saccade Duration [%]'][row] # extract numbers from string
        temp = re.findall(r'\d+', perc_string)
        perc_list = list(map(int, temp))
        perc_fixation_list.append(perc_list[0]) # extract fix percentage
        perc_saccade_list.append(perc_list[1])  # extract saccade percentage

    # different figure grid for different amount of trials/participants/groups  
    number_figs = len(perc_fixation_list)
    if number_figs % 3 == 0:
        figure_rows = number_figs / 3
    else:
        figure_rows = number_figs / 3 + 1

    # plot pie charts

    # if more than 2 pie charts are plotted
    if len(perc_fixation_list) >2 :    
        figure_rows = int(figure_rows)
        fig, axes = plt.subplots(figure_rows, 3, sharex=True, figsize=(10,5))
        fig.suptitle('Relative Fixation/Saccade Duration [%]', fontweight = 'bold')
        clrs = sns.color_palette('pastel')[0:len(perc_fixation_list)]
        lbls = ['Fixation', 'Saccade']

    # in case of only 1 sample + 1 mean -> only 2 plots on one row
    else:
        figure_rows = 1
        fig, axes = plt.subplots(figure_rows, 2, sharex=True, figsize=(10,5))
        fig.suptitle('Relative Fixation/Saccade Duration [%]', fontweight = 'bold')
        clrs = sns.color_palette('pastel')[0:len(perc_fixation_list)]
        lbls = ['Fixation', 'Saccade']

    # if only one row of pie charts (=< 3 plots)
    if figure_rows == 1:
        for fig_number in range(len(perc_fixation_list)):
            piedata = [perc_fixation_list[fig_number], perc_saccade_list[fig_number]] 
            axes[fig_number].set_title(df.index[fig_number])
            axes[fig_number].pie(piedata, colors = clrs, autopct='%.0f%%' )
        axes[0].legend(lbls, bbox_to_anchor=(0, 0.5))
        plt.text(1.1,1.1, filename, transform=plt.gca().transAxes)
        plt.savefig(savepath, bbox_inches = 'tight', dpi = 300)
        plt.clf()

    # if multiple rows of pie charts (> 3 plots)
    else:
        fig_number = 0
        for fig_row in range(figure_rows): 
            for fig_col in range(3): 
                    piedata = [perc_fixation_list[fig_number], perc_saccade_list[fig_number]] 
                    axes[fig_row, fig_col].set_title(df.index[fig_number], y=-0.1) # plot title below subplots
                    axes[fig_row, fig_col].pie(piedata, colors = clrs, autopct='%.0f%%' )
                    fig_number = fig_number + 1
                    if fig_number == number_figs:
                        break
            else:
                continue
            break

        fig.legend(lbls, bbox_to_anchor=(0.95, 1.05), loc = 'upper right') 
        fig.text(1,1, s=filename)

        # remove empty grid
        for ax in axes.flat[number_figs:]:
            ax.remove()    

        # save  
        plt.tight_layout()
        plt.savefig(savepath, bbox_inches = 'tight', dpi = 300)
        plt.clf()
    
# boxplots for visualisation of single trials per participant 
def vis_gen_metrics_boxplots_trials(sac_dur_list, fix_dur_list, outputpath, filename, specification, x_labels):

    # sac_dur_list: list of saccade durations of one participant
    # fix_dur_list: list of fixation durations of one participant
    # outputpath: output directory where file is exported to
    # specification: whole trial or specific action

    #boxplots: saccade duration
    savepath=outputpath /'Average Saccade Duration [ms]_boxplot_{}'.format(specification)
    sns.set_theme(style='whitegrid')
    boxplot = sns.boxplot(data=sac_dur_list, color='mediumseagreen')
    boxplot.set_xticklabels(x_labels, rotation = 90)
    plt.title('Average Saccade Duration ({})'.format(specification), fontsize = 16, pad = 20, weight = 'bold')
    plt.text(1.1,1.1, filename, transform=plt.gca().transAxes)
    plt.ylabel('Average Saccade Duration [ms]',  labelpad=20) 
    fig = boxplot.get_figure()
    fig.savefig(savepath, bbox_inches='tight', dpi=300)
    plt.clf()

    # boxplots: fixation duration
    savepath=outputpath /'Average Fixation Duration [ms]_boxplot_{}'.format(specification)
    boxplot = sns.boxplot(data=fix_dur_list, color='mediumseagreen')
    boxplot.set_xticklabels(x_labels, rotation = 90)
    plt.title('Average Fixation Duration ({})'.format(specification), fontsize = 16, pad = 20, weight = 'bold')
    plt.text(1.1,1.1, filename, transform=plt.gca().transAxes)
    plt.ylabel('Average Fixation Duration [ms]',  labelpad=20) 
    fig = boxplot.get_figure()
    fig.savefig(savepath, bbox_inches='tight', dpi=300)
    plt.clf()

# barplot for duration per action
def vis_gen_metrics_duration_per_action(df, outputpath, filename):
    # df: durations per action of a trial
    # outputpath: output directory where file is exported to
    savepath = outputpath / 'Duration per Action [ms]'
    sns.set_theme(style='whitegrid')
    barplot = sns.barplot(df.columns, df.iloc[-1], color='mediumseagreen')
    plt.title('Duration per Action [ms]', fontsize = 16, pad = 20, weight = 'bold')
    plt.text(1.1,1.1, filename, transform=plt.gca().transAxes)
    plt.ylabel('Duration per Action [ms]',  labelpad=20)
    barplot.set_xticklabels(labels = df.columns, rotation=90)
    fig = barplot.get_figure()
    fig.savefig(savepath, bbox_inches='tight', dpi=300)
    plt.clf()

#endregion
    
### OOI-BASED ANALYSIS
#region

# barplots and piecharts from trial level to all groups level of ooi-based analysis of metrics per OOI (as opposed to ooi-based per trial)
def vis_ooi_metrics(df, outputpath, filename, specification):
    # df: metrics per ooi df
    # outputpath: output directory where file is exported to
    # specification: whole trial or specific action
    
    # barplots for all metrics
    for i in range(len(df)):
        savepath=outputpath /'{} per OOI_barplot_{}'.format(df.index[i], specification)
        sns.set_theme(style='whitegrid')
        barplot = sns.barplot(df.columns, df.iloc[i], color='mediumseagreen')
        plt.title('{} per OOI ({})'.format(df.index[i], specification), fontsize = 16, pad = 20, weight = 'bold')
        plt.text(1.1,1.1, filename, transform=plt.gca().transAxes)
        plt.ylabel(df.index[i],  labelpad=20)
        fig = barplot.get_figure()
        fig.savefig(savepath, bbox_inches='tight', dpi=300)
        plt.clf()

    # additional piechart for Relative Dwell Time [%]:
    piedata = df.loc['Relative Dwell Time [%]'] 
    # only plot if greater than 0% 
    piedata = piedata[piedata!=0]
    # make pie chart
    savepath=outputpath /'{} per OOI_piechart_{}'.format('Relative Dwell Time [%]', specification)
    number_cols = len(piedata)
    clrs = sns.color_palette('pastel')[0:number_cols]
    lbls = piedata.index
    plt.pie(piedata, labels = lbls, colors = clrs, autopct='%.0f%%' )
    plt.text(1.3,1.1, filename, transform=plt.gca().transAxes)
    plt.title('Relative Dwell Time [%] per OOI ({})'.format(specification), fontsize = 16, pad = 20, weight = 'bold')
    plt.savefig(savepath, bbox_inches = 'tight', dpi = 300)
    plt.clf()

# boxplot for distributions per participant, group, all groups
def vis_ooi_boxplots(nested_list_series, outputpath, filename, specification, metric, x_labels):
    # nested_list: df of nested lists that contain values of level below in order to get box plot (e.g. boxplots of all groups needs values of each participant to calculate box plot)
    # outputpath: output directory where file is exported to
    # specification: whole trial or specific action
    savepath=outputpath /'{} per OOI_boxplot_{}'.format(metric, specification)
    sns.set_theme(style='whitegrid', palette='pastel')
    fig, axes = plt.subplots(1,len(nested_list_series), sharey=True)

    # iterate through all OOIs (nested series -> one series per OOI on respective level)
    for i in range (len(nested_list_series)):
        # make dataframe out of nested list
        df = pd.DataFrame(data=nested_list_series[i], index=x_labels)
        df = df.transpose()
        nested_list=nested_list_series[i]
        df_melted = df.melt()

        # make boxplot
        sns.boxplot(x='variable', y='value', hue='variable', data = df_melted, ax=axes[i]) # kind = 'count', labels=df.index,

        # remove redundant y labels and  x ticks
        axes[i].set_xticklabels('')
        axes[i].set_ylabel('')
        axes[i].get_legend().remove()
               
        # add title 
        axes[i].set_xlabel(nested_list_series.index[i])
        
    # plot all boxplots of all OOIs generated in loop
    axes[0].set_ylabel(metric, fontsize=16)
    axes[i].legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    plt.text(1.1,1.1, filename, transform=plt.gca().transAxes)
    fig.suptitle('{} ({})'.format(metric, specification), fontsize = 16, weight = 'bold')
    fig.savefig(savepath, bbox_inches='tight', dpi=300)
    plt.clf()

# visualisation of transition matrix
def vis_transition_matrix(transition_matrix, dict_ooi, outputpath, trialname, specification):
    # transition_matrix: TM from GTE calculation
    # dict_ooi: key to which number in TM corresponds to which OOI
    # outputpath: output directory where file is exported to
    # specification: whole trial or specific action

    # switch key and value in dict_ooi
    dict_ooi_switched = {y: x for x, y in dict_ooi.items()}
    df_tm = pd.DataFrame(transition_matrix)
    df_tm.columns = df_tm.columns.map(dict_ooi_switched)
    df_tm.index = df_tm.index.map(dict_ooi_switched)

    # generate TM
    savepath=outputpath /'Transition Matrix (GTE)_{}'.format(specification)    
    sns.color_palette('pastel')[0:len(df_tm)]
    sns.heatmap(df_tm, annot=True)
    sns.axes_style({'ytick.top': True})
    plt.tick_params(axis='both', which='major', labelsize=10, labelbottom = False, bottom=False, top = False, labeltop=True)
    plt.text(1.3,1.1, trialname, transform=plt.gca().transAxes)
    plt.title('Transition Matrix ({})'.format(specification), fontsize = 16, pad = 20, weight = 'bold')
    plt.savefig(savepath, bbox_inches = 'tight', dpi = 300)
    plt.clf()


# barplots from trial level to all groups level for ooi-based metrics per trial (as opposed to ooi-based metrics per OOI per trial)
def vis_ooigen_barplots(df, outputpath, filename, specification):
    # df: df containing all ooi-based metrics per trial
    # outputpath: output directory where file is exported to
    # specification: whole trial or specific action
    
    # iterate through all metrics in df
    for col in range(len(df.columns)):  
        savepath = outputpath / '{}_barplot_{}'.format(df.columns[col], specification)
        sns.set_theme(style='whitegrid')
        barplot = sns.barplot(x=df.index.values[:-1], y=df.iloc[:-1,col], color='mediumseagreen') # -1 becaues last row is standard deviation
        barplot.set_xticklabels(df.index[:-1], rotation = 90)
        barplot.set_yticklabels(df.columns[col])  
        plt.title('{} ({})'.format(df.columns[col], specification), fontsize = 16, pad = 20, weight = 'bold')
        plt.text(1.1,1.1, filename, transform=plt.gca().transAxes)
        fig = barplot.get_figure()
        fig.savefig(savepath, bbox_inches='tight', dpi=300)
        plt.clf()

#endregion

### K-COEFFICIENT
#region

# visualisation of k-coefficient per trial: line plot
def vis_kcoeff_lineplot_trial(df, outputpath, trialname, specification):
    # df: df with all k-coefficients and corresponding time point of fixation of one trial
    # outputpath: output directory where file is exported to
    # specification: whole trial or specific action
        savepath=outputpath /'K-Coefficient_{}'.format(specification)
        sns.set_theme(style='whitegrid')
        lineplot = sns.lineplot(df['start_time'], df['K-coefficient'], color='mediumseagreen')
        plt.title('K-Coefficient ({})'.format(specification), fontsize = 16, pad = 20, weight = 'bold')
        plt.text(1.1,1.1, trialname, transform=plt.gca().transAxes)
        plt.ylabel('K-Coefficient',  labelpad=20)
        plt.xlabel('Time [ms]',  labelpad=20)
        fig = lineplot.get_figure()
        fig.savefig(savepath, bbox_inches='tight', dpi=300)
        plt.clf()

# visualisation of k-coefficient line graph per participant -> overlay multiple trials
def vis_kcoeff_lineplot_pp(df_list, outputpath, trialname, legend_names, specification):
    # df_list: list of all dfs of one participant with all k-coefficients and corresponding time point of fixation of one trial
    # outputpath: output directory where file is exported to
    # specification: whole trial or specific action
    # legend_names: trial numbers

    # plot
    savepath = outputpath / 'K-Coefficients per time'
    sns.set_theme(style = 'whitegrid')
    clrs = sns.color_palette('pastel')[0:len(df_list)]
    
    # iterate through all trials per participant
    for l in range(len(df_list)):
        sns.lineplot(x=df_list[l]['start_time'], y=df_list[l]['K-coefficient'], color = clrs[l])

    plt.legend(legend_names)
    plt.title('K-Coefficient ({})'.format(specification), fontsize = 16, pad = 20, weight = 'bold')
    plt.text(1.1,1.1, trialname, transform=plt.gca().transAxes)
    plt.ylabel('K-Coefficient',  labelpad=20)
    plt.xlabel('Time [ms]',  labelpad=20)
    plt.savefig(savepath, bbox_inches='tight', dpi=300)
    plt.clf()

# barplot of mean k-coefficients per participant/group/allgroups and mark >2stdv mean with other color
def vis_kcoeff_barplot(df, outputpath, trialname, specification):
    # df: df with all k-coefficients per level
    # outputpath: output directory where file is exported to
    # specification: whole trial or specific action

    savepath = outputpath / 'K-Coefficients Summary'
    # slightly adapt df 
    df = df.transpose()

    #create a paired color palette
    sns.set_palette(sns.color_palette("Paired"))
    
    # create custom palette thatt separates ambient and focal view as well as inside and outside 2x stdevs
    custom_palette = {}
    for x in range(len(df)):
        if df[trialname][x] < 0:
            custom_palette[df.index[x]] = 'seagreen'
            if df['Outside 2x Stdev'][x] == 'Yes':
                custom_palette[df.index[x]] = 'springgreen'
        else:
            custom_palette[df.index[x]] = 'teal'
            if df['Outside 2x Stdev'][x] == 'Yes':
                custom_palette[df.index[x]] = 'cyan'
    
    # create customised legend (according to palette)
    color_list = ['seagreen','springgreen', 'teal', 'cyan' ]
    label_list = ['Ambient viewing / Not outside 2x stdev','Ambient viewing / Outside 2x stdev',  'Focal viewing / Not outside 2x stdev', 'Focal viewing / Outside 2x stdev']
    handlelist = [plt.plot([], marker='o', ls='', color = color)[0] for color in color_list]
    
    # create barplot with customised palette and legend from above
    barplot = sns.barplot(x=df.index, y=df[trialname], palette=custom_palette, dodge = False, data = df) 
    plt.title('K-Coefficient ({})'.format(specification), fontsize = 16, pad = 20, weight = 'bold')
    plt.text(1.1,1.1, trialname, transform=plt.gca().transAxes)
    plt.ylabel('K-Coefficient',  labelpad=20)
    barplot.set_xticklabels(labels = df.index, rotation=90)
    plt.legend(handlelist, label_list, bbox_to_anchor=(1, 1), loc="upper left")
    plt.savefig(savepath, bbox_inches='tight', dpi=300)
    plt.clf()

# barplot of mean k-coefficients per participant/group/allgroups per action and mark >2stdv mean with other color
def vis_kcoeff_barplot_action(df, outputpath, trialname, specification):
    # df: df with all k-coefficients per action of respective level
    # outputpath: output directory where file is exported to
    # specification: whole trial or specific action
    
    savepath = outputpath / 'K-Coefficients Summary per action'
    # transpose df
    df = df.transpose()
    # delete nan rows
    df.dropna(inplace = True)

    # create custom palette thatt separates ambient and focal view as well as inside and outside 2x stdevs
    custom_palette = {}
    for x in range(len(df)):

        if df['Mean {}'.format(trialname)][x] < 0:
            custom_palette[df.index[x]] = 'seagreen'
            if df['Outside 2x Stdev'][x] == 'Yes': # 'Yes'
                custom_palette[df.index[x]] = 'springgreen'
        else:
            custom_palette[df.index[x]] = 'teal'
            if df['Outside 2x Stdev'][x] == 'Yes': # 'Yes'
                custom_palette[df.index[x]] = 'cyan'
    
    # create customised legend (according to palette)
    color_list = ['seagreen','springgreen', 'teal', 'cyan' ]
    label_list = ['Ambient viewing / Not outside 2x stdev','Ambient viewing / Outside 2x stdev',  'Focal viewing / Not outside 2x stdev', 'Focal viewing / Outside 2x stdev']
    handlelist = [plt.plot([], marker='o', ls='', color = color)[0] for color in color_list]

    # create barplot
    barplot = sns.barplot(x=df.index, y=df['Mean {}'.format(trialname)], palette=custom_palette, dodge = False, data = df)
    plt.title('K-Coefficient ({})'.format(specification), fontsize = 16, pad = 20, weight = 'bold')
    plt.text(1.1,1.1, trialname, transform=plt.gca().transAxes)
    plt.ylabel('K-Coefficient',  labelpad=20)
    barplot.set_xticklabels(labels = df.index, rotation=90)
    plt.legend(handlelist, label_list, bbox_to_anchor=(1, 1), loc="upper left")
    plt.savefig(savepath, bbox_inches='tight', dpi=300)
    plt.clf()

#endregion

### STATISTICS 
#region

# mark trials outside 2x 

# ooi gen barplots for 
def vis_stats_ooi_gen(df, outputpath, trialname, metric, specification):
    savepath = outputpath / '{}_barplot_Whole Trial.png'.format(metric) # overwrite the existing barplots

    # create custom palette (inside vs outside 2x stdevs)
    custom_palette = {}
    for x in range(len(df)):
        if df['Outside 2x Stdev'][x] == 'Yes':
                custom_palette[df.index[x]] = 'springgreen'
        else:
            custom_palette[df.index[x]] = 'seagreen'
    
    # create customised legend (according to palette)
    color_list = ['seagreen','springgreen' ]
    label_list = ['Not outside 2x stdev','Outside 2x stdev']
    handlelist = [plt.plot([], marker='o', ls='', color = color)[0] for color in color_list]
    
    # create barplot
    barplot = sns.barplot(x=df.index, y=df[metric], palette=custom_palette, dodge = False, data = df) 
    plt.title('{} ({})'.format(metric, specification), fontsize = 16, pad = 20, weight = 'bold')
    plt.text(1.5,1.1, trialname, transform=plt.gca().transAxes)
    plt.ylabel(metric,  labelpad=20)
    barplot.set_xticklabels(labels = df.index, rotation=90)
    plt.legend(handlelist, label_list, bbox_to_anchor=(1.2, 1), loc="upper left")
    plt.savefig(savepath, bbox_inches='tight', dpi=300)
    plt.clf()

#endregion

