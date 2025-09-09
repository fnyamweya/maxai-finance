
from __future__ import annotations
import numpy as np, pandas as pd, joblib, os
from sklearn.ensemble import GradientBoostingRegressor
from .features import build_features, build_Xy

QUANTILES = [0.1, 0.5, 0.9]

class QuantileCashForecaster:
    def __init__(self, models, feature_cols):
        self.models = models  # dict q -> model
        self.feature_cols = feature_cols

    @classmethod
    def train(cls, cash_df: pd.DataFrame, **gb_params):
        feat = build_features(cash_df)
        X, y, cols = build_Xy(feat)
        models = {}
        for q in QUANTILES:
            m = GradientBoostingRegressor(loss='quantile', alpha=q, n_estimators=400, max_depth=2,
                                          learning_rate=0.05, subsample=0.9, random_state=17)
            m.set_params(**{k:v for k,v in gb_params.items() if v is not None})
            m.fit(X, y)
            models[q] = m
        return cls(models, cols)

    def save(self, path: str):
        os.makedirs(path, exist_ok=True)
        joblib.dump({'models': self.models, 'feature_cols': self.feature_cols}, os.path.join(path, 'cash_model.joblib'))

    @classmethod
    def load(cls, path: str):
        obj = joblib.load(os.path.join(path, 'cash_model.joblib'))
        return cls(obj['models'], obj['feature_cols'])

    def _make_row(self, hist_df: pd.DataFrame, date: pd.Timestamp):
        feat = build_features(hist_df)
        # we only need last row features for prediction day
        x = feat.tail(1).drop(columns=['date','inflow','outflow','net']).values
        preds = {q: float(self.models[q].predict(x)[0]) for q in QUANTILES}
        return preds

    def forecast(self, cash_df: pd.DataFrame, horizon: int = 35):
        df = cash_df.sort_values('date').reset_index(drop=True).copy()
        preds = []
        last_date = df['date'].iloc[-1]
        for h in range(1, horizon+1):
            d = last_date + pd.Timedelta(days=h)
            # build features using history + previous predicted net (use p50 for recursion)
            row_pred = self._make_row(df, d) if len(df)>=40 else {0.1:0.0,0.5:0.0,0.9:0.0}
            # append pseudo-row with inflow/outflow derived from net p50 split (heuristic 60/40)
            net_p50 = row_pred[0.5]
            inflow_guess = max(0.0, 0.6*max(0.0, net_p50))
            outflow_guess = inflow_guess - net_p50
            df = pd.concat([df, pd.DataFrame([{'date': d, 'inflow': inflow_guess, 'outflow': outflow_guess}])], ignore_index=True)
            preds.append({'date': d.date().isoformat(), 'net_p10': row_pred[0.1], 'net_p50': net_p50, 'net_p90': row_pred[0.9]})
        return pd.DataFrame(preds)

def traffic_lights(pred_df: pd.DataFrame, start_cash: float, min_buffer: float = 0.0):
    bal = start_cash
    lights = []
    for _,r in pred_df.iterrows():
        # conservative: use p10 for net flow
        bal += r['net_p10']
        level = 'green' if bal > min_buffer else ('yellow' if bal > min_buffer*0.5 else 'red')
        lights.append(level)
    out = pred_df.copy()
    out['traffic'] = lights
    return out
