import pymongo
import sqlalchemy
import datetime
import time
import pandas as pd
from bson import ObjectId


def process_key(key, **kwargs):
    k = str(key)
    pre_replace = {
        'VIP': 'Vip',
        'ID': 'Id',
    }
    if isinstance(kwargs.get('replace'), dict):
        pre_replace = {**pre_replace, **kwargs['replace']}
    for raw, clean in pre_replace.items():
        k = k.replace(raw, clean)
    processed_key = ''
    for letter in k:
        if letter.isupper():
            processed_key += '_' + letter.lower()
        else:
            processed_key += letter
    return processed_key


def process_value(value):
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, list):
        new_value = [str(elem) for elem in value]
        return new_value
    return value


def unnest_data(nested_data: dict, data: dict = None, path='', **kwargs):
    data = data or {}
    for k, v in nested_data.items():
        if 'password' in k or 'pwd' in k:
            continue
        new_key = path + process_key(k, **kwargs)
        if isinstance(v, dict):
            unnest_data(v, data, path=new_key + '_', **kwargs)
        else:
            data[new_key] = process_value(v)
    return data


def process_mongo_doc(doc):
    return unnest_data(doc)


def batch_data_to_dataframe(batch_data: list):
    df = pd.DataFrame(data=batch_data)
    df['review_time'] = datetime.datetime.utcnow()
    return df


def mongo_to_pg(mongo_col: pymongo.collection.Collection, mongo_query: dict, pg_engine: sqlalchemy.engine.Engine,
                pg_tbl_name: str, projection: dict = None, dump_mode='append', batch_size=2000, **kwargs):

    print(f'[{datetime.datetime.now()}] Start mongo2pg job: {mongo_col.full_name} -> {pg_engine.name}.{pg_tbl_name}...')
    t1 = time.time()
    results = []
    batch_data = []
    batch_id = 1
    print(f'[{datetime.datetime.now()}] Docs in results: {mongo_col.count_documents(mongo_query)}')
    projection = projection
    cursor = mongo_col.find(mongo_query, projection=projection)
    for idx, doc in enumerate(cursor):
        unnested_doc = unnest_data(doc, **kwargs)
        batch_data.append(unnested_doc)
        if (idx+1) % batch_size == 0:
            df = batch_data_to_dataframe(batch_data)
            df.to_sql(pg_tbl_name, con=pg_engine, index=False, if_exists=dump_mode)
            dump_mode = 'append'
            results += batch_data
            batch_data = []
            batch_id += 1
    if len(batch_data) > 0:
        df = batch_data_to_dataframe(batch_data)
        df.to_sql(pg_tbl_name, con=pg_engine, index=False, if_exists=dump_mode)
        results += batch_data
        batch_data = []

    t2 = time.time()
    print(f'[{datetime.datetime.now()}] Job finished, time use = {round(t2 - t1, 3)} sec')
    return results
