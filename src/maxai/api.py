
from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from .models import QuantileCashForecaster, traffic_lights
import os

app = FastAPI(title="maxAI — Finance API")

class ForecastReq(BaseModel):
    history: list
    horizonDays: int = 35
    startCash: float = 0.0
    modelPath: str = "artifacts/cash"

@app.post("/maxai/forecast/cash")
def forecast_cash(req: ForecastReq):
    df = pd.DataFrame(req.history)
    df['date'] = pd.to_datetime(df['date'])
    m = QuantileCashForecaster.load(req.modelPath)
    pred = m.forecast(df, horizon=req.horizonDays)
    plan = traffic_lights(pred, start_cash=req.startCash)
    return {'predictions': pred.to_dict(orient='records'),
            'plan': plan.to_dict(orient='records')}

def main():
    import uvicorn, os
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
