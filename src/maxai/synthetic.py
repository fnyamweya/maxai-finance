
from __future__ import annotations
import pandas as pd, numpy as np
from dateutil.relativedelta import relativedelta
import argparse, random, datetime as dt

def gen_days(n=540, end=None, seed=17):
    random.seed(seed); np.random.seed(seed)
    if end is None:
        end = dt.date.today()
    start = end - dt.timedelta(days=n-1)
    return pd.date_range(start, end, freq='D')

def synthetic_cash(n=540, end=None, seed=17):
    days = gen_days(n, end, seed)
    t = np.arange(len(days))
    # Baseline inflow/outflow with weekly and monthly patterns
    inflow = 100000 + 30000*np.sin(2*np.pi*t/7) + 50000*np.sin(2*np.pi*t/30) + np.random.normal(0,20000,len(t))
    outflow = 80000 + 35000*np.sin(2*np.pi*(t+2)/7) + 40000*np.sin(2*np.pi*(t+5)/30) + np.random.normal(0,18000,len(t))
    # Payday spikes on day 25 approx
    day = pd.Series(days).dt.day.values
    payday = (day>=24)&(day<=26)
    outflow = outflow + payday*120000
    inflow = np.maximum(1000, inflow)
    outflow = np.maximum(1000, outflow)
    df = pd.DataFrame({'date': days, 'inflow': inflow, 'outflow': outflow})
    return df

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='data/cash_daily.csv')
    ap.add_argument('--days', type=int, default=540)
    args = ap.parse_args()
    df = synthetic_cash(n=args.days)
    os = args.out
    import os as _os
    _os.makedirs(_os.path.dirname(os), exist_ok=True)
    df.to_csv(os, index=False)
    print('Wrote', os)

if __name__ == '__main__':
    main()
