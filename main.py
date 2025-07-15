import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# CSV 파일 불러오기
df = pd.read_csv('dioxide.csv', sep=';')

# Cars 데이터만 추출
cars = df[df['Category'] == 'Cars'].iloc[:, 1:]
years = cars.columns.astype(int)
emissions = cars.values.flatten()

# 스트림릿 타이틀
st.title('자동차 CO₂ 배출량 연도별 분석')
st.write("1990년부터 2016년까지의 자동차 CO₂ 배출량 데이터를 기반으로 시각화 및 분석을 수행합니다.")

# Plotly 라인 차트
fig = go.Figure()
fig.add_trace(go.Scatter(x=years, y=emissions, mode='lines+markers', name='Cars CO₂'))

fig.update_layout(
    title='자동차 CO₂ 배출량 추이',
    xaxis_title='연도',
    yaxis_title='배출량 (Mt)',
    template='plotly_white'
)

st.plotly_chart(fig, use_container_width=True)



# 추세 요약
st.subheader('추세 요약')
start = emissions[0]
end = emissions[-1]
change = end - start
percent_change = (change / start) * 100
annual_avg = change / (len(years) - 1)

st.write(f"처음 연도({years[0]})의 CO₂ 배출량은 **{start:.3f} Mt**, 마지막 연도({years[-1]})는 **{end:.3f} Mt**입니다.")
st.write(f"총 변화량은 **{change:.3f} Mt**, 변화율은 **{percent_change:.2f}%** 입니다.")
st.write(f"연평균 증가량은 **{annual_avg:.3f} Mt/year** 입니다.")
