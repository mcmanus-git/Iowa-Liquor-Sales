from MyCreds.mycreds import IowaData
import pandas as pd
from sodapy import Socrata # < Unmaintained as of August 31, 2022, just in time for this project
import numpy as np
import h3
import requests
from geopy.geocoders import Nominatim
import pymssql

# Globals
geolocator = Nominatim(user_agent="my_user_agent")
KEY = IowaData.api_key
SECRET = IowaData.api_key_secret
TOKEN = IowaData.app_token
liquor_sales_data_id = "m3tr-qhgy"
LIMIT = 24_000_000


def get_unique_with_least_nulls(df):
    df['n_null'] = df.isnull().sum(axis=1)
    df = df.sort_values(['store_id', 'n_null'], ascending=False).groupby('store_id').last().reset_index()
    df.drop('n_null', axis=1, inplace=True)
    return df


def get_nominatim_lat_long(x):

    try:
        address = (x['address'] + ' ' + x['city'] + ', IA ' + x['zipcode']).replace('  ', ' ').strip()
        g = geolocator.geocode(address)
        if g:
            long, lat = g.longitude, g.latitude
        else:
            long, lat = np.nan, np.nan
    except:
        long, lat = np.nan, np.nan
        next

    return long, lat


def fill_missing_locs(df):
    missing = df[(~df['address'].isnull()) & (df['long'].isnull())]
    ll = missing.apply(lambda x: get_nominatim_lat_long(x), axis=1, result_type='expand')
    missing = missing.merge(ll, left_index=True, right_index=True).drop(['long', 'lat'], axis=1).rename({0: 'long', 1: 'lat'}, axis=1)

    df = df.merge(missing[['store_id', 'long', 'lat']], on='store_id', how='left')

    df['long_x'].fillna(df['long_y'], inplace=True)
    df['lat_x'].fillna(df['lat_y'], inplace=True)
    df.rename({'long_x': 'long', 'lat_x': 'lat'}, axis=1, inplace=True)
    df.drop(['long_y', 'lat_y'], axis=1, inplace=True)

    return df


def clean_locations(df, h3_resolution=8):
    coords_df = pd.DataFrame(df['geometry'].to_dict()).T
    coords_df['coordinates'] = np.where(coords_df['coordinates'].isnull(), pd.Series([[]]*len(coords_df)), coords_df['coordinates']) # fill na with empty list
    df = df.merge(pd.DataFrame(coords_df['coordinates'].to_list(), columns=['long', 'lat']), left_index=True, right_index=True)

    df['store_name'] = df['store_name'].str.replace('"', '').str.title().str.replace("'S", "'s")
    df['city'] = df['city'].str.title()
    df['address'] = df['address'].str.title()
    df['store_name'].replace("( #\d+ / .+| / .+| #\d+)", "", regex=True, inplace=True)
    df['zipcode'].replace(r"(-\d*)", "", regex=True, inplace=True)

    print('Removing Duplicates...')
    df = get_unique_with_least_nulls(df)

    print('Filling missing lat/long...')
    df = fill_missing_locs(df)

    def lat_long_to_h3(row):
        return h3.geo_to_h3(lat=row.lat,lng=row.long,resolution = h3_resolution)

    df['hex_id'] = df.apply(lat_long_to_h3, axis=1)
    df.drop('geometry', axis=1, inplace=True)

    return df


def get_store_info():

    query = f"select distinct(store) as store_id, name as store_name, address, city, zipcode," \
            f" county_number as county_id, store_location as geometry limit {LIMIT}"
    url = f"https://data.iowa.gov/resource/m3tr-qhgy.json?$$app_token={TOKEN}&$query={query}"
    print('Getting Request Response...')
    r = requests.get(url=url).json()
    df = pd.DataFrame(r)
    print('Cleaning Dataframe...')
    df = clean_locations(df)

    return df


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def load(df):
    server = IowaData.azure_server
    user = IowaData.azure_uid
    password = IowaData.azure_pwd

    write_data = list(map(tuple, df.fillna(0).values))
    insert_query = f"""INSERT INTO invoices.store({', '.join([*df.columns])}) VALUES ({', '.join(['%s' for col in df.columns])})"""
    insert_q, values_q = insert_query.split('VALUES') # get part with the query and the parameters
    insert_q += 'VALUES' # add values to make sql query correct after split

    with pymssql.connect(server, user, password, "iowa_liquor") as cnxn:
        with cnxn.cursor() as cur:
            for chunk_data in chunks(write_data, 1000):
                # chunk_data contains list of row parameters
                # we make it flat to use execute later instead execute_many
                flat_list = [item for sublist in chunk_data for item in sublist]
                # creating the query with multiple values insert
                chunk_query = insert_q + ','.join([values_q] * len(chunk_data))
                cur.execute(chunk_query, tuple(flat_list))
                cnxn.commit()


def main():
    store_map = get_store_info()
    print('Loading Data...')
    load(store_map)


if __name__ == '__main__':
    main()
