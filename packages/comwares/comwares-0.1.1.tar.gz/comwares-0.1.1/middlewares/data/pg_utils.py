import datetime
import time
import pandas as pd
from typing import Iterable


def reformat_df(df: pd.DataFrame):
    for k in df.columns:
        if '_time' in k:
            df[k] = pd.to_datetime(df[k])
    df['review_time'] = int(datetime.datetime.utcnow().timestamp())
    return df


def get_df_from_cursor(cursor: Iterable, processing_func=None, verbose=False):
    processed_data = []
    for d in cursor:
        if processing_func:
            d = processing_func(d)
        if isinstance(d, list):
            processed_data += d
        else:
            processed_data.append(d)
    if verbose:
        print(f'[{datetime.datetime.now()}] Number of data in batch: {len(processed_data)}')
    df = pd.DataFrame(data=processed_data)
    df = reformat_df(df)
    return df


def clean_pg_table(pg_engine, dump_tbl, clean_tbl, partition_by, order_by, recreate=False):
    t1 = time.time()
    if recreate:
        sql = f'''
            drop table if exists {clean_tbl};
            create table {clean_tbl} as (
                select *
                from (
                    select *, rank() over (partition by {partition_by} order by {order_by} desc) as rk
                    from {dump_tbl}
                ) as t
                where rk = 1
            )
        '''
    else:
        sql = f'''
            delete from {clean_tbl} where 1 = 1;
            insert into {clean_tbl}
            select *
            from (
                select *, rank() over (partition by {partition_by} order by {order_by} desc) as rk
                from {dump_tbl}
            ) as t
            where rk = 1
        '''
    pg_engine.execute(sql)
    t2 = time.time()
    print(f'[{datetime.datetime.now()}] Table {clean_tbl} has been updated, time used = {round(t2 - t1, 3)} seconds.')
