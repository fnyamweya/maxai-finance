
from __future__ import annotations
import gradio as gr, pandas as pd, matplotlib.pyplot as plt
from .models import QuantileCashForecaster, traffic_lights
from .io import read_cash_csv
import io

def run(cash_csv, horizon, start_cash, model_dir):
    df = read_cash_csv(cash_csv.name)
    model = QuantileCashForecaster.load(model_dir)
    pred = model.forecast(df, horizon=horizon)
    plan = traffic_lights(pred, start_cash=start_cash)
    # Build a quick plot
    fig = plt.figure()
    x = pd.to_datetime(pred['date'])
    plt.fill_between(x, pred['net_p10'], pred['net_p90'], alpha=0.2, label='P10-P90')
    plt.plot(x, pred['net_p50'], label='P50')
    plt.title('maxAI Cashflow Forecast (net)')
    plt.legend()
    return pred, plan, fig

def main():
    demo = gr.Interface(
        fn=run,
        inputs=[
            gr.File(label="cash_daily.csv"),
            gr.Slider(7, 56, value=35, step=1, label="Horizon (days)"),
            gr.Number(value=0, label="Starting Cash Balance"),
            gr.Textbox(value="artifacts/cash", label="Model Path")
        ],
        outputs=[gr.Dataframe(label="Predictions"), gr.Dataframe(label="Plan (Traffic Lights)"), gr.Plot(label="Chart")],
        title="maxAI — Finance (Cashflow)",
        description="Upload cash_daily.csv with columns: date,inflow,outflow. Model path must contain cash_model.joblib."
    )
    demo.launch()

if __name__ == "__main__":
    main()
