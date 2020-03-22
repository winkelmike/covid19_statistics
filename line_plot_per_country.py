import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from utils import etl_chain

CSV_PATH_COUNTRIES = "data/country_specific/"
IMAGE_PATH = "visualizations/static_plots_per_country/"
csv_file_path_list = glob.glob(CSV_PATH_COUNTRIES + '*.csv')


def extract_relevant_csv_for_static_vis():
    all_files = glob.glob(CSV_PATH_COUNTRIES + '*.csv')
    return [pd.read_csv(df_name, parse_dates=['date'], index_col='date') for df_name in all_files]


def transform_df_for_static_vis(df_list):
    return {
        country_df['country'].iloc[0].replace(',', ''): country_df[country_df.confirmed != 0].drop(['country'], axis=1)
        for country_df in df_list
    }


def load_country_observations_vis(df_dict_all):
    return {render_country_observation_vis(name, df) for name, df in df_dict_all.items()}


def render_country_observation_vis(country_name, country_df):
    dates = country_df.index[::7]
    labels = dates.strftime('%b %d')
    cols_plot = ['confirmed', 'deaths', 'recovered']
    sns.set_style("whitegrid")

    country_df[cols_plot].plot.area(alpha=0.5, figsize=(11, 9), stacked=False)
    plt.title(f"Covid-19 observations in {country_name} over time")
    plt.xlabel('Day')
    plt.xticks(dates, labels, rotation=60)
    plt.ylabel('Observations')

    file_path_name = f"{IMAGE_PATH}observations_in_{country_name.replace(' ', '_')}.jpg"
    if os.path.isfile(file_path_name):
        os.remove(file_path_name)
    try:
        plt.savefig(file_path_name)
    except Exception as inst:
        print(f"ERROR: '{inst.args[0]}' on the visualization: {country_name}")
    plt.close()


def load_country_subplots_vis(df_dict_all):
    return {render_country_subplots_vis(name, df) for name, df in df_dict_all.items()}


def render_country_subplots_vis(country_name, country_df):
    cols_plot = ['confirmed', 'deaths', 'recovered']
    figure = plt.figure()
    gs = figure.add_gridspec(7, 6)
    plt.rc('font', size=8)

    f_ax_all = figure.add_subplot(gs[:, :])
    f_ax_all.set_title("Covid-19 observations in " + country_name + " over time")
    f_ax_all.spines['right'].set_color('none')
    f_ax_all.spines['top'].set_color('none')
    f_ax_all.spines['bottom'].set_color('none')
    f_ax_all.spines['left'].set_color('none')
    f_ax_all.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)
    f_ax_all.set_xlabel('common xlabel')
    f_ax_all.set_ylabel('common ylabel')

    f_ax1 = figure.add_subplot(gs[1:, :4])
    f_ax1.set_title('all items')
    f_ax1.spines['right'].set_color('none')
    f_ax1.spines['top'].set_color('none')
    f_ax1.spines['bottom'].set_color('none')
    country_df[cols_plot].plot.area(alpha=0.5, stacked=False, ax=plt.gca())
    f_ax1.xaxis.set_visible(False)

    f_ax2 = figure.add_subplot(gs[2:3, 4:])
    f_ax2.set_title('confirmed')
    f_ax2.xaxis.set_visible(False)
    country_df['confirmed'].plot.area(alpha=0.5, ax=plt.gca(), color='#1F77B4')

    f_ax3 = figure.add_subplot(gs[4:5, 4:])
    f_ax3.set_title('deaths')
    f_ax3.xaxis.set_visible(False)
    country_df['deaths'].plot.area(alpha=0.5, ax=plt.gca(), color='#FF7F0E')

    f_ax4 = figure.add_subplot(gs[5:, 4:])
    f_ax4.set_title('recovered')
    f_ax4.xaxis.set_visible(False)
    country_df['recovered'].plot.area(alpha=0.5, figsize=(5, 5), ax=plt.gca(), color='#2CA02C')

    file_path_name = f"{IMAGE_PATH}observations_in_{country_name.replace(' ', '_')}.jpg"
    if os.path.isfile(file_path_name):
        os.remove(file_path_name)
    try:
        plt.savefig(file_path_name)
    except Exception as inst:
        print(f"ERROR: '{inst.args[0]}' on the visualization: {country_name}")
    plt.close()


# for csv_file_path in csv_file_path_list:
#     if csv_file_path == 'data\\covid_observations_all.csv':
#         continue
#
#     country_df = pd.read_csv(csv_file_path, parse_dates=['date'], index_col='date')
#     country_name = country_df['country'].iloc[0].replace(',', '')
#     country_df.drop(['country'], axis=1)
#     country_df = country_df[country_df.confirmed != 0]
#
#
#     dates = country_df.index[::7]
#     labels = dates.strftime('%b %d')
#
#     cols_plot = ['confirmed', 'deaths', 'recovered']
#     # sns.set_style("whitegrid")
#     # plt.title("Covid-19 observations in " + country_name + " over time")
#     # plt.xlabel('Day')
#     # plt.xticks(dates, labels, rotation=60)
#     # plt.ylabel('Observations')
#     figure = plt.figure()
#     gs = figure.add_gridspec(7, 6)
#     plt.rc('font', size=8)
#
#     f_ax_all = figure.add_subplot(gs[:, :])
#     f_ax_all.set_title("Covid-19 observations in " + country_name + " over time")
#     f_ax_all.spines['right'].set_color('none')
#     f_ax_all.spines['top'].set_color('none')
#     f_ax_all.spines['bottom'].set_color('none')
#     f_ax_all.spines['left'].set_color('none')
#     f_ax_all.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)
#     f_ax_all.set_xlabel('common xlabel')
#     f_ax_all.set_ylabel('common ylabel')
#
#
#     f_ax1 = figure.add_subplot(gs[1:, :4])
#     f_ax1.set_title('all items')
#
#     f_ax1.spines['right'].set_color('none')
#     f_ax1.spines['top'].set_color('none')
#     f_ax1.spines['bottom'].set_color('none')
#     country_df[cols_plot].plot.area(alpha=0.5, stacked=False, ax=plt.gca())
#     f_ax1.xaxis.set_visible(False)
#
#
#     f_ax2 = figure.add_subplot(gs[2:3, 4:])
#     f_ax2.set_title('confirmed')
#     f_ax2.xaxis.set_visible(False)
#     country_df['confirmed'].plot.area(alpha=0.5, ax=plt.gca(), color='#1F77B4')
#
#     f_ax3 = figure.add_subplot(gs[4:5, 4:])
#     f_ax3.set_title('deaths')
#     f_ax3.xaxis.set_visible(False)
#     country_df['deaths'].plot.area(alpha=0.5, ax=plt.gca(), color='#FF7F0E')
#
#     f_ax4 = figure.add_subplot(gs[5:, 4:])
#     f_ax4.set_title('recovered')
#     f_ax4.xaxis.set_visible(False)
#     country_df['recovered'].plot.area(alpha=0.5, figsize=(5, 5), ax=plt.gca(), color='#2CA02C')
#
#     # f_ax3 = figure.add_subplot(gs[:, :-1])
#     # f_ax3.set_title('deceased')
#     #
#     # f_ax4 = figure.add_subplot(gs[:, :-1])
#     # f_ax4.set_title('recovered')
#     #
#     # ax = plt.subplot2grid((2, 2), (0, 0))
#     #
#     # f, axes = plt.subplots(2, 2, figsize=(7, 7), sharex=True)
#     #
#      # all three together in area
#
#
#     # country_df['confirmed'].plot.area(alpha=0.5, figsize=(11, 9), stacked=False, color='blue', ax=axes[0, 1])
#     # country_df['deaths'].plot.area(alpha=0.5, figsize=(11, 9), stacked=False, color='red', ax=axes[1, 0])
#     # country_df['recovered'].plot.area(alpha=0.5, figsize=(11, 9), stacked=False, color='green', ax=axes[1, 1])
#
#
#     plt.show()
#     input('x')
#
#
#
#     image_name = "observations_in_" + country_name.replace(' ', '_') + '.jpg'
#     file_path_name = IMAGE_PATH + "" + image_name
#
#     print('working on: ' + country_name)
#     if os.path.isfile(file_path_name):
#         os.remove(file_path_name)
#
#
#     try:
#         plt.savefig(file_path_name)
#     except Exception as inst:
#         print(inst.args[0])
#         print('ERROR on: ' + country_name)
#
#     plt.close()



if __name__ == "__main__":
    countries_df_list = extract_relevant_csv_for_static_vis()
    etl_chain(countries_df_list,
              transform_df_for_static_vis,
              load_country_observations_vis,
              render_country_observation_vis)
