
from __future__ import annotations
import pandas as pd

def read_cash_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=['date'])
    for col in ['inflow','outflow']:
        if col not in df.columns:
            raise ValueError(f'Missing required column: {col}')
    df = df.sort_values('date').reset_index(drop=True)
    df['net'] = df['inflow'] - df['outflow']
    return df

def to_records(df: pd.DataFrame):
    return df.to_dict(orient='records')
