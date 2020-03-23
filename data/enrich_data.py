import pycountry_convert as pc
import numpy as np
import pandas as pd
from utils import etl_chain

COUNTRY_CODE_ENRICHED = {
    "Bahamas, The": "BS",
    "Congo (Brazzaville)": "CG",
    "Congo (Kinshasa)": "CD",
    "Cote d'Ivoire": "CI",
    "Gambia, The": "GM",
    "Holy See": "VA",
    "Korea, South": "KR",
    "Kosovo": "XK",
    "US": "US"
}


def get_iso_and_continent_from_country_name(country_name):
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
    except Exception as inst:
        if country_name in COUNTRY_CODE_ENRICHED.keys():
            country_alpha2 = COUNTRY_CODE_ENRICHED[country_name]
        else:
            print(f"ERROR: '{inst.args[0]}' on the country_name: {country_name}, returning NaN instead")
            return pd.Series([np.NaN, np.NaN])

    # WORKAROUND for pycountry_convert renaming issue
    if country_alpha2 == "TL":
        country_alpha2 = "TP"
    elif country_alpha2 == "VA":
        country_alpha2 = "IT"

    country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    return pd.Series([country_alpha2, country_continent_name])


def match_iso_and_continent_to_df(df):
    if "country" in df.index.names:
        df[['country_code', 'continent']] = \
            df.apply(lambda row: get_iso_and_continent_from_country_name(row.name[0]), axis=1)
    else:
        df[['country_code', 'continent']] = \
            df.apply(lambda row: get_iso_and_continent_from_country_name(row['country']), axis=1)
    return df


def extract_government_measures():
    return pd.read_excel("data/government_measures/covid19-government-measures-dataset.xlsx", "Database")


def transform_government_measures(df):
    return df


def match_government_measures_to_df(df_in):
    df_government_measures = extract_government_measures()
    print(df_government_measures.head())
    input('x')
    df_government_measures_transformed = transform_government_measures(df_government_measures)
    df_in.merge(df_government_measures_transformed)
    return df_in


# TODO add policy events
# TODO add demographics per country
# TODO create alternative enrichment CSV to be joined to observations later
