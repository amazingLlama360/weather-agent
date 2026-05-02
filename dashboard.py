import json

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


st.title("Camping Temperature Dashboard")


with open("memory.json", "r") as f:
    data = json.load(f)


history = data["temperature_history"]
df = pd.DataFrame(history)

df["time"] = pd.to_datetime(df["time"])
df["time"] = df["time"].dt.tz_convert("America/Los_Angeles")


latest_time = df["time"].max()
last_24h = df[df["time"] >= latest_time - pd.Timedelta(hours=24)]


max_temp = last_24h["temperature"].max()
max_row = last_24h[last_24h["temperature"] == max_temp]

min_temp = last_24h["temperature"].min()
min_row = last_24h[last_24h["temperature"] == min_temp]


fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=last_24h["time"],
        y=last_24h["temperature"],
        mode="lines",
        name="Temperature",
    )
)

fig.add_trace(
    go.Scatter(
        x=max_row["time"],
        y=max_row["temperature"],
        mode="markers",
        marker=dict(size=10),
        name="Max Temp",
    )
)

fig.add_trace(
    go.Scatter(
        x=min_row["time"],
        y=min_row["temperature"],
        mode="markers",
        marker=dict(size=10),
        name="Min Temp",
    )
)

fig.update_layout(
    title="Temperature Over the Last 24 Hours",
    xaxis_title="Time",
    yaxis_title="Temperature (°C)",
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Last 24 Hours of Data")
st.dataframe(last_24h)