
from __future__ import annotations
import pandas as pd, numpy as np

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy().sort_values('date').reset_index(drop=True)
    df['net'] = df['inflow'] - df['outflow']
    # temporal features
    df['dow'] = df['date'].dt.dayofweek
    df['dom'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['is_month_end'] = df['date'].dt.is_month_end.astype(int)
    # lags
    for L in [1,2,3,7,14,28]:
        df[f'lag_{L}'] = df['net'].shift(L)
    # rolling means/std
    for W in [7,14,28]:
        df[f'roll_mean_{W}'] = df['net'].shift(1).rolling(W, min_periods=3).mean()
        df[f'roll_std_{W}'] = df['net'].shift(1).rolling(W, min_periods=3).std()
    df = df.dropna().reset_index(drop=True)
    return df

def build_Xy(df: pd.DataFrame):
    y = df['net'].values
    drop_cols = ['date','inflow','outflow','net']
    X = df.drop(columns=[c for c in drop_cols if c in df.columns])
    return X, y, X.columns.tolist()
