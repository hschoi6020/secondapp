import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🌡️ 연도별 평균 기온 추이 시각화")

# 파일 업로드 받기
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    # CSV 읽기
    df = pd.read_csv(uploaded_file)

    # 날짜 → 연도 변환
    df['Year'] = pd.to_datetime(df['dt']).dt.year

    # 연도별 평균 계산
    yearly_avg = df.groupby('Year')['LandAverageTemperature'].mean().reset_index()

    # Plotly 그래프
    fig = px.line(
        yearly_avg,
        x='Year',
        y='LandAverageTemperature',
        title='연도별 평균 기온 추이',
        labels={'LandAverageTemperature': '평균 기온 (℃)', 'Year': '연도'},
        markers=True
    )

    st.plotly_chart(fig)
