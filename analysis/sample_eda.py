import pandas as pd

sample_df = pd.read_csv('source_data/csse_covid_19_data/csse_covid_19_daily_reports/03-20-2020.csv')
print(sample_df.columns)
print(sample_df.describe())
print(sample_df.shape)
print(sample_df.info())
print(sample_df.head())
