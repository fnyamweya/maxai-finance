
# maxAI (Finance) — Product Document

## Elevator Pitch
maxAI turns your finance module into a forward‑looking CFO assistant. It forecasts cash, flags anomalies, and explains what to do next, in plain language.

## Users & Jobs‑To‑Be‑Done
- **Owner/CFO:** "Will we have enough cash next month?"
- **Accountant:** "What looks unusual before month‑end close?"
- **Ops Lead:** "When should we stagger supplier payments?"

## Functional Scope (v0.1)
1. **Cashflow Forecast** (daily/weekly, P10/P50/P90)  
2. **Traffic‑Light Alerts** (green/yellow/red weeks)  
3. **Anomaly Radar** (outliers in daily net cash)  
4. **API + Space UI** (integrate or try in minutes)

## Non‑Functional
- Open‑source (Apache‑2.0), reproducible, no PII.
- Tenant isolation by `tenant_id` at data source edge.
- Works offline with local CSV.

## KPIs
- Forecast WQL@P50 ≤ baseline (naïve).  
- Reduction in *surprise* negative balances.  
- Time saved at period‑end.

## Roadmap
- v0.2: AR/AP risk scorer, narrative financials.  
- v0.3: AP optimizer, FX scenario engine.  
- v1.0: Full governance, drift monitors, multilingual assistant.
