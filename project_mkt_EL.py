#%%
import pandas as pd
import requests
import pandas_gbq
from google.oauth2 import service_account
from datetime import datetime, timedelta

#%%
def get_data(start_date, end_date, path_file):
    """
    Descarga datos de una API basada en el rango de fechas proporcionado y los guarda en un archivo CSV.
    
    :param start_date: Fecha de inicio en formato 'MM/DD/YYYY'.
    :param end_date: Fecha de fin en formato 'MM/DD/YYYY'.
    :param path_file: Ruta del archivo donde se almacenarán los datos.
    """
    url = f'https://my.api.mockaroo.com/project_elt_mkt.json?start_date={start_date}&end_date={end_date}'
    headers = {'X-API-Key': 'f4ab4d20'}
    r = requests.get(url, headers=headers)
    
    with open(path_file, 'wb') as f:
        f.write(r.content)
    
    print(f'{path_file} created')

def load_to_bigquery(path_file, source):
    """
    Carga los datos desde un archivo CSV a una tabla en Google BigQuery.
    
    :param path_file: Ruta del archivo CSV con los datos.
    :param source: Fuente de los datos, que se añadirá como columna en BigQuery.
    """
    credentials = service_account.Credentials.from_service_account_file(
        'credentials/project-mkt-elt-434619-68f27428e6ad.json',
    )
    
    df = pd.read_csv(path_file)
    df = df.assign(source=source)
    df.Date = pd.to_datetime(df.Date)
    
    pandas_gbq.to_gbq(
        df, f'broce_mkt.{source}_raw', 
        project_id='project-mkt-elt-434619', 
        if_exists='append',
        credentials=credentials
    )

def create_rango_fechas():
    """
    Genera un rango de fechas para cada mes de los años 2022, 2023 y 2024.
    
    :return: Lista de listas con pares de fechas [inicio, final] para cada mes.
    """
    anios = [2022, 2023, 2024]
    meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    range_dates = []
    
    for anio in anios:
        for mes in meses:
            inicio = (datetime(anio, mes, 1)).strftime('%m/%d/%Y').lstrip('0').replace('/0', '/')
            if mes == 12:
                final = (datetime(anio, mes, 31)).strftime('%m/%d/%Y').lstrip('0').replace('/0', '/')
            else:
                final = (datetime(anio, mes+1, 1) - timedelta(days=1)).strftime('%m/%d/%Y').lstrip('0').replace('/0', '/')
            range_dates.append([inicio, final])
    
    return range_dates

#%%
source = 'google_ads'
start_date = '1/1/2021'
end_date = '1/31/2021'

path_file = f'data/campaign_{source}_{start_date.replace("/", "-")}_{end_date.replace("/", "-")}.csv'
get_data(start_date, end_date, path_file)
load_to_bigquery(path_file, source)

#%%
sources = ['google_ads', 'youtube_ads', 'instagram_ads', 'twitter_ads', 'facebook_ads', 'email']
rango_date = create_rango_fechas()[:-9]

for source in sources:
    for rango in rango_date:
        start_date = rango[0]
        end_date = rango[1]
        path_file = f'data/campaign_{source}_{start_date.replace("/", "-")}_{end_date.replace("/", "-")}.csv'
        get_data(start_date, end_date, path_file)
        load_to_bigquery(path_file, source)

# %%
