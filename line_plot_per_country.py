import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

CSV_PATH = "data/"
IMAGE_PATH = "visualizations/static_plots_per_country/"
csv_file_path_list = glob.glob(CSV_PATH + '*.csv')

for csv_file_path in csv_file_path_list:
    if csv_file_path == 'data\\covid_observations_all.csv':
        continue

    country_df = pd.read_csv(csv_file_path, parse_dates=['date'], index_col='date')
    country_name = country_df['country'].iloc[0].replace(',', '')
    country_df.drop(['country'], axis=1)
    country_df = country_df[country_df.confirmed != 0]

    dates = country_df.index[::7]
    labels = dates.strftime('%b %d')

    cols_plot = ['confirmed', 'deaths', 'recovered']
    sns.set_style("whitegrid")

    country_df[cols_plot].plot.area(alpha=0.5, figsize=(11, 9), stacked=False)
    plt.title("Covid-19 observations in " + country_name + " over time")
    plt.xlabel('Day')
    plt.xticks(dates, labels, rotation=60)
    plt.ylabel('Observations')

    image_name = "observations_in_" + country_name.replace(' ', '_') + '.jpg'
    file_path_name = IMAGE_PATH + "" + image_name

    print('working on: ' + country_name)
    if os.path.isfile(file_path_name):
        os.remove(file_path_name)
    try:
        plt.savefig(file_path_name)
    except Exception as inst:
        print(inst.args[0])
        print('ERROR on: ' + country_name)

    plt.close()
