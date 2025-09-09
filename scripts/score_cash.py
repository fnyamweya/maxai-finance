
import argparse
from maxai.cli import forecast_cash as _score

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--cash', required=True)
    ap.add_argument('--model', required=True)
    ap.add_argument('--horizon', type=int, default=35)
    ap.add_argument('--start-cash', type=float, default=0.0)
    ap.add_argument('--out', default='predictions.csv')
    args = ap.parse_args()
    _score.callback(cash=args.cash, model_dir=args.model, horizon=args.horizon, start_cash=args.start_cash, out_csv=args.out)
