import pandas as pd
import plotly.express as px

# CSV 파일 불러오기
df = pd.read_csv("dioxide-dioxide (1).csv")  # ← 파일명을 실제로 존재하는 파일명으로 바꿔주세요

# 날짜 → 연도 추출
df['Year'] = pd.to_datetime(df['dt']).dt.year

# 연도 필터링: 1950~2015년
df_filtered = df[(df['Year'] >= 1950) & (df['Year'] <= 2015)]

# 연도별 평균 온도 계산
yearly_avg = df_filtered.groupby('Year')['LandAverageTemperature'].mean().reset_index()

# Plotly 그래프 그리기
fig = px.line(
    yearly_avg,
    x='Year',
    y='LandAverageTemperature',
    title='🌡️ 연도별 평균 기온 추이 (1950–2015)',
    labels={'LandAverageTemperature': '평균 기온 (℃)', 'Year': '연도'},
    markers=True
)

fig.show()
