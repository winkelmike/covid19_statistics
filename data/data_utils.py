import pandas as pd
import glob


def extract_data_csv_list(path):
    all_files = glob.glob(f"{path}*.csv")
    return [pd.read_csv(df_name, parse_dates=['date'], index_col='date') for df_name in all_files]


def get_country_name_from_df(df):
    if "country" in df.index.names:
        return df.index.get_level_values('country')[0].replace(',', '')
    else:
        return df['country'].iloc[0].replace(',', '')
