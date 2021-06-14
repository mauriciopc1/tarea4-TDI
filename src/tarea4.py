import xml.etree.ElementTree as ET
import requests
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
import os

directory = os.path.dirname(os.path.abspath(__file__))
api_credentials = os.path.join(
    directory, 'tarea4-tdi-316808-bd39d54c91d0.json')


country_list = [
    "AND",
    "JAM",
    "CHL",
    "ESP",
    "ARG",
    "FRA",
]


def xml_to_pd(country_list):
    df_cols = [
        'COUNTRY',
        'GHO',
        'SEX',
        'YEAR',
        'GHECAUSES',
        'AGEGROUP',
        'Display',
        'Numeric',
        'Low',
        'High'
    ]
    df_rows = []
    for country in country_list:
        url = f'http://tarea-4.2021-1.tallerdeintegracion.cl/gho_{country}.xml'
        r = requests.get(url)
        tree = ET.fromstring(r.content)
        for fact in tree.findall('Fact'):
            data = [fact.find(col).text if fact.find(
                col) is not None else None for col in df_cols]
            df_rows.append({df_cols[i]: data[i]
                           for i, _ in enumerate(df_cols)})
    out_df = pd.DataFrame(df_rows, columns=df_cols)
    return out_df


gc = gspread.service_account(filename=api_credentials)
sh = gc.open_by_key('1yccee3i81FCF1U4GHS0GswEzllfp0KH_epzRxS4A9qc')

worksheet = sh.get_worksheet(0)
df = xml_to_pd(country_list)
set_with_dataframe(worksheet, df)
