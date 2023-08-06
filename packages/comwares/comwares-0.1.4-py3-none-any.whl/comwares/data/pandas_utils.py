import datetime
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

