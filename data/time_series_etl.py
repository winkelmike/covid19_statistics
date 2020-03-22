import pandas as pd
from utils import etl_chain
from data.data_utils import get_country_name_from_df
from data.enrich_data import match_continent_to_df
FILE_PATH_SPECIFIC = "data/country_specific/"
FILE_PATH_ALL_DATA = "data/all_countries/"


def extract_covid_ts():
    """
    Load all JHU time series CSV's into local DataFrames
    :return: dict of DataFrames
    """
    confirmed_df = pd.read_csv(r'source_data/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid'
                               r'-Confirmed.csv')
    deaths_df = pd.read_csv(r'source_data/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')
    recovered_df = pd.read_csv(r'source_data/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid'
                               r'-Recovered.csv')
    return {'confirmed': confirmed_df, 'deaths': deaths_df, 'recovered': recovered_df}


def transform_covid_ts(df_dict):
    """
    Reshape all DataFrames to observations per date and country
    Concatenate all DataFrames on date/country to a single DataFrame
    :param df_dict: dict of DataFrames
    :return: single reshaped DataFrame
    """
    df_list = []
    for key in df_dict:
        df = df_dict[key]
        prepared_df = df \
            .rename(columns={'Country/Region': 'country'}) \
            .drop(['Lat', 'Long'], axis=1) \
            .groupby(['country']).sum()\
            .reset_index() \
            .melt(id_vars='country', var_name='date', value_name=key)\
            .set_index(['country', 'date'])\
            .rename(index={'Taiwan*': 'Taiwan'})
        enriched_prepared_df = enrich_covid_ts_dataframe(prepared_df)
        df_list.append(enriched_prepared_df)
    result_df = pd.concat(df_list, axis=1, join='inner')
    return result_df


def transform_covid_ts_per_country(long_df):
    """
    Split source DataFrame into several smaller ones grouped by country
    :param long_df: DataFrame of all countries and date
    :return: list of several DataFrames by country
    """
    country_df_list = []
    for country, df_country in long_df.groupby('country'):
        enriched_prepared_df = enrich_covid_ts_dataframe(df_country)
        country_df_list.append(enriched_prepared_df)
    return country_df_list


def enrich_covid_ts_dataframe(df):
    return etl_chain(df, match_continent_to_df)


def load_covid_ts_all_countries(df):
    """
    Output DataFrame to covid_observations_ts.csv
    :param df: DataFrame with observations per date and country
    """
    file_name = "covid_observations_all.csv"
    df.to_csv(FILE_PATH_ALL_DATA + file_name)


def load_covid_ts_per_country(df_list):
    """
    Output DataFrames per country to covid_observations_ts_<country name>.csv
    :param df_list: Dict per country of DataFrames over date
    """
    for df in df_list:
        country_name = get_country_name_from_df(df)
        file_name = f"covid_observations_in_{country_name}.csv"
        df.to_csv(FILE_PATH_SPECIFIC + file_name)


if __name__ == "__main__":
    raw_data = extract_covid_ts()

    # observations for all countries and date
    etl_chain(raw_data, transform_covid_ts, load_covid_ts_all_countries)

    # observations per country
    etl_chain(raw_data, transform_covid_ts, transform_covid_ts_per_country, load_covid_ts_per_country)
