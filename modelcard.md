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
  metrics:
- "wql"
- "mase"
- "rmse"
  inference: "python_function"
  model-index:
- name: "maxAI-cash-quantile"
  results:
  - task: "time-series-forecasting"
    dataset: "tenant_csv_samples"
    metrics: { wql_p50: "see-modelcard", mase: "see-modelcard" }

---

# Model Card — maxAI Finance (Cashflow Forecaster)

**Short description**  
maxAI Finance is an open-source probabilistic cashflow forecasting and anomaly-detection suite for Kilimax ERP finance modules. It provides daily net-cash forecasts (inflow − outflow) as three quantiles (P10, P50, P90) and surfaces risk signals and anomalies to help finance teams make proactive decisions.

---

## 1. Intended use

**Primary use-cases**

- Short- to medium-term (daily/weekly) cashflow forecasting for SMEs and ERP users.
- Producing conservative (P10), median (P50) and optimistic (P90) daily net-cash scenarios.
- Driving actionable outputs: traffic-light risk signals, suggested bridge sizes, and anomaly alerts.

**Target users**

- Finance managers, accountants, CFOs, and ops leads.
- Developers integrating forecasting into ERP dashboards or chat assistants.

**Not intended for**

- Regulatory or statutory financial reporting without human review.
- High-frequency trading or sub-daily treasury operations.
- Decisions requiring legal, tax, or regulatory adjudication.

---

## 2. Non-technical summary

Think of maxAI as a **weather forecast for your cash**:

1. We look at past days of money in and out (history).
2. We learn patterns (paydays, supplier spikes, seasonality).
3. We forecast three scenarios: conservative, most-likely, optimistic.
4. We simulate your bank balance using the conservative path to show risk days.
5. We flag unusual days for investigation.

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

**Synthetic / demo data**

- The repo includes a labeled synthetic data generator for testing. Do not mix synthetic and production data in evaluation.

**Privacy**

- Only numeric amounts and dates are required. Do not include personal identifiers or PII in training data.

---

## 4. Model architecture & training

**Core approach**

- Three `GradientBoostingRegressor` models (scikit-learn) trained with quantile (pinball) loss to produce P10, P50, P90 forecasts.
- Anomaly detector: `IsolationForest` or robust detector run on engineered daily features.

**Design rationale**

- Quantile GBDT gives probabilistic outputs, CPU inference, and interpretable feature importance.
- Simplicity + interpretability enables rapid deployment into ERP stacks.

**Training regime**

- Global training across tenants with tenant/location normalization where available.
- Rolling-origin backtests (e.g., every 14 days).
- Hyperparameter tuning via time-series-aware CV.
- Early stopping and small tree depth to reduce overfitting.

---

## 5. Evaluation & metrics

**Primary metrics**

- Weighted Quantile Loss (WQL) at P10/P50/P90.
- Mean Absolute Scaled Error (MASE).
- Root Mean Squared Error (RMSE).
- Business KPIs where applicable (e.g., worst-case deficit, days below zero).

**Backtesting**

- Use rolling-origin backtests across multiple tenants and seasonal splits.
- Report per-segment metrics (high-volume vs long-tail series).

**Example reporting template**

- Provide WQL, MASE, and RMSE per segment and horizon (7, 14, 28 days).
- Include simulation of business impact (e.g., bridge size to avoid P10 negative days).

---

## 6. Output format & interpretation

**Primary outputs (API)**

- `predictions`: array of `{ date, net_p10, net_p50, net_p90 }`
- `plan`: `predictions` plus `traffic` computed by simulating P10 cumulatively against `startCash`.

**How to read**

- Use **P10** for risk planning and buffer sizing.
- Use **P50** for operational planning.
- Use **P90** for optimistic scenarios.

**Actionable fields**

- `earliest_red_date`: earliest date P10 cumulative balance ≤ 0.
- `worst_case_shortfall`: `max(0, -min_cumulative_p10)` — amount to bridge risk.
- `anomalies`: list of flagged dates with reason codes.

---

## 7. Failure modes & limitations

**Cold-start**

- Best with ≥ 40–90 days of history. Short histories fall back to baseline heuristics.

**Non-stationarity**

- New business models, product launches, or payment-term changes will reduce accuracy until retrained.

**Exogenous shocks**

- Macroeconomic events or outages (e.g., payment network downtime) must be encoded as features to be captured.

**Bias & fairness**

- Monitor for systematic under/over-forecasting by region or tenant; audit regularly.

**Explainability**

- Feature importance and simple attributions are provided. Complex causal claims are out of scope.

---

## 8. Security, privacy & governance

**Tenant isolation**

- Keep tenant raw data isolated. If training globally, use tenant embeddings and avoid exposing raw rows across tenants.

**PII**

- Do not include customer identifiers or personal data.

**Auditability**

- Log every forecast with model version, feature snapshot, and inputs.

**Access control**

- Restrict model artifacts and HF tokens to secure storage (secret manager).

---

## 9. Deployment & monitoring

**Deployment patterns**

- Edge/on-prem: export ONNX for inference in offline clients.
- Batch: nightly batch forecasts persisted to a forecast table.
- API: FastAPI endpoint for on-demand scenarios.

**Monitoring**

- Track WQL, MASE, PSI for features, and business KPIs.
- Trigger retrains when drift or KPI degradation crosses thresholds.

**Model registry**

- Store artifacts, metrics, and evaluation reports for each version.

---

## 10. Reproducibility & running the model

**Quick commands**

```bash
maxai-train-cash --cash path/to/cash_daily.csv --model artifacts/cash
maxai-forecast-cash --cash path/to/cash_daily.csv --model artifacts/cash --horizon 35 --start-cash 1000000 --out predictions.csv
```

**API call**
`POST /maxai/forecast/cash`:

```json
{
  "history": [{"date":"2025-08-01","inflow":200000,"outflow":150000}, ...],
  "horizonDays": 35,
  "startCash": 1000000,
  "modelPath": "artifacts/cash"
}
```

**Environment**

- Python >= 3.10
- pandas, numpy, scikit-learn, joblib, fastapi, gradio

**Notebooks**

- Include backtesting and evaluation notebooks: `notebooks/02_evaluation.ipynb`

---

## 11. Maintenance & governance

**Retrain cadence**

- Weekly to monthly depending on drift and business change rate.

**Human-in-the-loop**

- Require human approval for any payment-scheduling action. AI suggestions are advisory.

**Issue & updates**

- Report security/data issues via repo issue tracker.
- Maintain change log and release notes per model version.

---

## 12. Citation & contact

Please cite:

```
Ombura, Felix et al. "maxAI: Intermittent Cashflow Forecasting & Anomaly Detection", 2025.
```

Contact: `support@your-org.example` or GitHub `@your-org/maxai`

---

## 13. Limitations & concluding note

This model is a **decision-support tool**. Use it to reduce surprises and focus finance effort. Always combine model outputs with business rules and human judgment.
