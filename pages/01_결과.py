import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="CO₂ vs 온도", layout="wide")
st.title("자동차 CO₂ 배출량 증가에 따른 지구 평균 기온 변화")

# 1. 로컬 CSV 로드
@st.cache_data
def load_data(path):
    return pd.read_csv(path)

df = load_data("car_co2_temp.csv")

# 2. 연도 범위 선택
years = df["year"].unique()
start_year, end_year = st.sidebar.select_slider(
    "연도 범위 선택",
    options=sorted(years),
    value=(years.min(), years.max())
)

df = df[(df["year"] >= start_year) & (df["year"] <= end_year)]

# 3. 데이터 미리보기
st.subheader(f"{start_year}년 ~ {end_year}년 데이터")
st.dataframe(df, use_container_width=True)

# 4. Plotly 이중 축 차트 그리기
fig = make_subplots(specs=[[{"secondary_y": True}]])

# 자동차 CO₂ 배출량 (왼쪽 y축)
fig.add_trace(
    go.Scatter(
        x=df["year"],
        y=df["vehicle_co2"],
        name="자동차 CO₂ 배출량 (MtCO₂)",
        mode="lines+markers",
        line=dict(color="green"),
    ),
    secondary_y=False
)

# 지구 평균 기온 (오른쪽 y축)
fig.add_trace(
    go.Scatter(
        x=df["year"],
        y=df["avg_temp"],
        name="지구 평균 기온 (℃)",
        mode="lines+markers",
        line=dict(color="red"),
    ),
    secondary_y=True
)

# 레이아웃 설정
fig.update_layout(
    title_text="연도별 자동차 CO₂ 배출량 vs 지구 평균 기온 (이중 축)",
    legend=dict(orientation="h", y=-0.2),
    margin=dict(l=40, r=40, t=80, b=40)
)

fig.update_xaxes(title_text="연도")
fig.update_yaxes(title_text="자동차 CO₂ 배출량 (MtCO₂)", secondary_y=False)
fig.update_yaxes(title_text="지구 평균 기온 (℃)", secondary_y=True)

# 5. 차트 렌더링
st.plotly_chart(fig, use_container_width=True)
