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
  - name: "custom/csv"
inference:
  type: "python_function"
  entry_point: "src/maxai/space_app.py"
model-index:
  - name: "maxAI-cash-quantile"
    results:
      - task:
          name: "time-series-forecasting"
          type: "regression"
        dataset:
          name: "tenant_csv_samples"
          type: "tabular"
        metrics:
          - name: "wql_p50"
            type: "wql"
            value: "see-modelcard"
          - name: "mase"
            type: "mase"
            value: "see-modelcard"
          - name: "rmse"
            type: "rmse"
            value: "see-modelcard"
---

# Model Card — maxAI Finance (Cashflow Forecaster)

**Short description**  
maxAI Finance is an open-source probabilistic cashflow forecasting and anomaly-detection suite for ERP finance modules. It provides daily net-cash forecasts (inflow − outflow) as three quantiles (P10, P50, P90) and surfaces risk signals and anomalies to help finance teams make proactive decisions.

---

## 1. Intended use

**Primary use-cases**

- Short- to medium-term (daily/weekly) cashflow forecasting for SMEs and ERP users.
- Producing conservative (P10), median (P50) and optimistic (P90) daily net-cash scenarios.
- Driving actionable outputs: traffic-light risk signals, suggested bridge sizes, and anomaly alerts.

**Target users**

- Finance managers, accountants, CFOs, ops leads, and developers integrating forecasting into ERP dashboards.

**Not intended for**

- Regulatory or statutory financial reporting without human review.
- High-frequency trading or sub-daily treasury operations.
- Decisions requiring legal, tax, or regulatory adjudication.

---

## 2. Non-technical summary

Think of maxAI as a **weather forecast for your cash**:

1. It looks at past days of money in and out (history).
2. It learns patterns (paydays, supplier spikes, seasonality).
3. It forecasts three scenarios: conservative (P10), most-likely (P50), optimistic (P90).
4. It simulates your bank balance using the conservative path to show risk days.
5. It flags unusual days for investigation.

Outputs are decision-support only; human approval is required for financial actions.

---

## 3. Data

**Required input (CSV)**

- `cash_daily.csv` with columns:
  - `date` (YYYY-MM-DD)
  - `inflow` (float)
  - `outflow` (float)

**Derived features**

- `net = inflow - outflow`
- calendar: day_of_week, day_of_month, month, is_month_end
- temporal: lags (1,2,3,7,14,28), rolling means/std (7,14,28)
- optional flags: payroll_day, holiday, scheduled_invoice_date

**Privacy**

- Only numeric amounts and dates are required; do not include personal identifiers or PII.

---

## 4. Model architecture & training

**Core approach**

- Three Gradient Boosting models trained with quantile (pinball) loss to produce P10, P50, P90 forecasts.
- Anomaly detector: IsolationForest over engineered daily features.

**Training**

- Rolling-origin backtests, tenant normalization when applicable, and time-series aware CV.

---

## 5. Outputs & interpretation

**Primary outputs (API)**

- `predictions`: array of `{ date, net_p10, net_p50, net_p90 }`
- `plan`: `predictions` plus `traffic` computed by simulating cumulative `net_p10` against `startCash`

**Actionable fields**

- `earliest_red_date`: earliest date P10 cumulative balance ≤ 0
- `worst_case_shortfall`: `max(0, -min_cumulative_p10)` — amount to bridge risk
- `anomalies`: list of flagged dates with reason codes

---

## 6. Evaluation & metrics

**Primary metrics**

- Weighted Quantile Loss (WQL) at P10/P50/P90
- Mean Absolute Scaled Error (MASE)
- Root Mean Squared Error (RMSE)

**Reporting**

- Provide per-segment and per-horizon values (e.g., 7/14/28 days). Include backtest and business-impact simulations.

---

## 7. Limitations & governance

- Cold-start: best with ≥ 40–90 days of history.
- Non-stationarity and exogenous shocks can reduce accuracy.
- Human-in-the-loop required for payment actions; log all forecasts with model version.

---

## 8. Contact & citation

If you use this model in production or research, please cite:

`Ombura, Felix et al. "maxAI: Intermittent Cashflow Forecasting & Anomaly Detection", 2025.`

Contact / maintainers: `felixombura@gmail.com`
