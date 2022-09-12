import pandas as pd
from MyCreds.mycreds import IowaData
import pymssql
import h3
from sodapy import Socrata # < Unmaintained as of August 31, 2022, just in time for this project
import numpy as np
from datetime import datetime, timedelta
from tqdm import tqdm

# Config Globals
KEY = IowaData.api_key
SECRET = IowaData.api_key_secret
TOKEN = IowaData.app_token
liquor_sales_data_id = "m3tr-qhgy"


def get_last_date_of_month(year, month):
    if month == 12:
        last_date = datetime(year, month, 31)
    else:
        last_date = datetime(year, month + 1, 1) + timedelta(days=-1)

    return last_date.strftime("%Y-%m-%d")


def log(run_start, time_range, successful=1, error='NaN'):
    run_time = datetime.now() - run_start
    with open('etl_log.csv', 'a') as f:
        f.write(f"{datetime.now()}, {run_time}, {time_range[0]}, {time_range[1]}, {successful}, {error}\n")


def clean_dataframe(df, h3_resolution=8):
    coords_df = pd.DataFrame(df['store_location'].to_dict()).T
    coords_df['coordinates'] = np.where(coords_df['coordinates'].isnull(), pd.Series([[]]*len(coords_df)),
                                        coords_df['coordinates']) # fill na with empty list

    df = df.merge(pd.DataFrame(coords_df['coordinates'].to_list(),
                               columns=['long', 'lat']),
                  left_index=True,
                  right_index=True)

    def lat_long_to_h3(row):
        return h3.geo_to_h3(lat=row.lat,lng=row.long,resolution = h3_resolution)

    df['hex_id'] = df.apply(lat_long_to_h3, axis=1)
    df['date'] = pd.to_datetime(df['date'])

    int_cols = ['store', 'county_number', 'category', 'vendor_no', 'itemno', 'pack', 'sale_bottles', ]
    float_cols = ['state_bottle_cost', 'state_bottle_retail', 'sale_dollars', 'sale_liters', 'sale_gallons']

    df[int_cols] = df[int_cols].astype('Int64')
    df[float_cols] = df[float_cols].astype(float)
    df.drop('store_location', axis=1, inplace=True)

    str_cols = list(df.select_dtypes(include='object'))
    df[str_cols] = df[str_cols].astype(str)

    return df


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def load(df):
    server = IowaData.azure_server
    user = IowaData.azure_uid
    password = IowaData.azure_pwd

    write_data = list(map(tuple, df.fillna(0).values))
    insert_query = f"""INSERT INTO invoices.temptable({', '.join([*df.columns])}) VALUES ({', '.join(['%s' for col in df.columns])})"""
    insert_q, values_q = insert_query.split('VALUES') # get part with the query and the parameters
    insert_q += 'VALUES' # add values to make sql query correct after split

    with pymssql.connect(server, user, password, "iowa_liquor") as cnxn:
        with cnxn.cursor() as cur:

            for chunk_data in chunks(write_data, 1000):
                # chunk_data contains list of row parameters
                flat_list = [item for sublist in chunk_data for item in sublist] # we make it flat to use execute later instead execute_many
                chunk_query = insert_q + ','.join([values_q] * len(chunk_data)) # creating the query with multiple values insert
                cur.execute(chunk_query, tuple(flat_list))
                cnxn.commit()



    # write_data = [str(rec) for rec in df.fillna(0).to_records(index=False)]
    # insert_query_part = f"INSERT INTO invoices.temptable({', '.join([*df.columns])})"
    #
    # for chunk in tqdm(chunks(write_data, 10000)):
    #     val_query_part = f"VALUES {', '.join(chunk)}"
    #     insert_chunk_query = insert_query_part + "\n" + val_query_part + ";"
    #     with pymssql.connect(server, user, password, "iowa_liquor") as cnxn:
    #         with cnxn.cursor() as cur:
    #             cur.execute(insert_chunk_query, write_data)
    #             cnxn.commit()


    # insert_query = f"""INSERT INTO invoices.temptable({', '.join([*df.columns])})
    # VALUES ({', '.join(['%s' for col in df.columns])})"""
    #
    # write_data = tuple(map(tuple, df.fillna(0).values))
    #
    # with pymssql.connect(server, user, password, "iowa_liquor") as cnxn:
    #     with cnxn.cursor() as cur:
    #         cur.executemany(insert_query, write_data)
    #         cnxn.commit()


def main():
    date_intervals = [
        [
            f"{datetime(y, m, 1):%Y-%m-%d}",
            f"{get_last_date_of_month(y, m)}"
        ]
        for y in range(2012, datetime.now().year + 1)
        for m in range(1, 13)
        if (y <= datetime.now().year and datetime.now().month > m)
    ]

    client = Socrata("data.iowa.gov", app_token=TOKEN)

    for interval in tqdm(date_intervals):
        run_start_time = datetime.now()
        try:
            date_between = f"(date between '{interval[0]}' and '{interval[1]}')"
            print(f"Retrieving: {interval}")
            results = client.get_all(liquor_sales_data_id, where=date_between)
            socrata_df = pd.DataFrame.from_records(results)
            socrata_df = clean_dataframe(socrata_df)
            print("Loading results...")
            load(socrata_df)
            log(run_start_time, interval)

        except Exception as e:
            log(run_start_time, interval, successful=0, error=e)


if __name__ == '__main__':
    main()
