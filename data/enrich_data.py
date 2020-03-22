import pycountry_convert as pc
from data.data_utils import get_country_name_from_df
import numpy as np

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


def country_to_continent(country_name):
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
    except Exception as inst:
        if country_name in COUNTRY_CODE_ENRICHED.keys():
            country_alpha2 = COUNTRY_CODE_ENRICHED[country_name]
        else:
            print(f"ERROR: '{inst.args[0]}' on the country_name: {country_name}, returning NaN instead")
            return np.NaN

    # WORKAROUND for pycountry_convert renaming issue
    if country_alpha2 == "TL":
        country_alpha2 = "TP"
    elif country_alpha2 == "VA":
        country_alpha2 = "IT"

    country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    return country_continent_name


def match_continent_to_df(df):
    if "country" in df.index.names:
        df['continent'] = df.apply(lambda row: country_to_continent(row.name[0]), axis=1)
    else:
        df['continent'] = df.apply(lambda row: country_to_continent(row['country']), axis=1)
    return df
