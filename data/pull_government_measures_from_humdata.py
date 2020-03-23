import os
from hdx.hdx_configuration import Configuration
from hdx.data.dataset import Dataset

FILE_PATH = "data/government_measures/"


Configuration.create(hdx_site='prod', user_agent='COVID19', hdx_read_only=True)
dataset = Dataset.read_from_hdx('acaps-covid19-government-measures-dataset')
resources = dataset.get_resources()

file_name = f"{resources[0]['name']}.XLSX"
if os.path.isfile(FILE_PATH + file_name):
    os.remove(FILE_PATH + file_name)

url, path = resources[0].download(FILE_PATH)
os.rename(FILE_PATH + file_name,  FILE_PATH + r'covid19-government-measures-dataset.xlsx')
