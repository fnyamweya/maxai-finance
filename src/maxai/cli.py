
from __future__ import annotations
import click, pandas as pd, os, joblib
from .io import read_cash_csv
from .models import QuantileCashForecaster, traffic_lights

@click.group()
def cli():
    pass

@cli.command()
@click.option('--cash', required=True, help='Path to cash_daily.csv')
@click.option('--model', 'model_dir', required=True, help='Output dir for model artifacts')
def train_cash(cash, model_dir):
    df = read_cash_csv(cash)
    m = QuantileCashForecaster.train(df)
    os.makedirs(model_dir, exist_ok=True)
    m.save(model_dir)
    click.echo(f"Saved model to {model_dir}")

@cli.command()
@click.option('--cash', required=True)
@click.option('--model', 'model_dir', required=True)
@click.option('--horizon', type=int, default=35)
@click.option('--start-cash', type=float, default=0.0)
@click.option('--out', 'out_csv', default='predictions.csv')
def forecast_cash(cash, model_dir, horizon, start_cash, out_csv):
    df = read_cash_csv(cash)
    m = QuantileCashForecaster.load(model_dir)
    pred = m.forecast(df, horizon=horizon)
    plan = traffic_lights(pred, start_cash=start_cash)
    pred.to_csv(out_csv, index=False)
    plan.to_csv(out_csv.replace('.csv','_plan.csv'), index=False)
    click.echo(f"Wrote {out_csv} and {out_csv.replace('.csv','_plan.csv')}")

if __name__ == '__main__':
    cli()
