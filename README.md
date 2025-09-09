---
language: "en"
license: "apache-2.0"
tags:
  - "time-series"
  - "forecasting"
  - "finance"
  - "quantile-regression"
  - "cashflow"
  - "anomaly-detection"
library_name: "scikit-learn"
datasets:
  - "custom/csv"
inference: "python_function"
---

# maxAI — Finance Intelligence (Cashflow + Anomaly)

**Tagline:** _See the money before it moves._  
**What:** Open‑source cashflow forecasting and anomaly radar for ERP finance modules.

## Features (v0.1)

- Daily/weekly **cashflow forecast** with **P10/P50/P90** bands (quantile GBDT).
- **Traffic‑light** early warnings (green/yellow/red) for cash tightness.
- **Anomaly scan** on daily net cash (Isolation Forest).
- **FastAPI** API and **Gradio Space** demo.
- Hugging Face packaging script & model card.

## Quickstart (local)

```bash
# 1) Install (uv/venv/pip)
pip install -e .

# 2) Generate synthetic finance data (optional)
python -m maxai.synthetic --out data/cash_daily.csv

# 3) Train
maxai-train-cash --cash data/cash_daily.csv --model artifacts/cash

# 4) Forecast 35 days ahead
maxai-forecast-cash --cash data/cash_daily.csv --model artifacts/cash --horizon 35 --start-cash 1000000 --out predictions.csv

# 5) Run API
maxai-api  # -> http://127.0.0.1:8000/docs

# 6) Gradio demo (local Space)
maxai-space-demo
```

### CSV schema: `cash_daily.csv`

- `date` (YYYY-MM-DD)
- `inflow` (float)
- `outflow` (float)

## Hugging Face — upload

```bash
pip install huggingface_hub

# Log in
huggingface-cli login

# Package model artifacts and push (creates repo if missing)
python scripts/pack_hf.py --model_dir artifacts/cash --repo maxai/maxai-finance-cash
```

> The Space app lives in `src/maxai/space_app.py` and can be deployed as a Hugging Face Space (Gradio) by pointing to this file.
