
import argparse
from maxai.cli import train_cash as _train

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--cash', required=True)
    ap.add_argument('--model', required=True)
    args = ap.parse_args()
    _train.callback(cash=args.cash, model_dir=args.model)
