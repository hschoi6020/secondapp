import pandas as pd
import plotly.express as px

# CSV 파일 로드
df = pd.read_csv("dioxide.csv")  # ← 여기에 파일 경로 입력

# 날짜에서 연도 추출
df['Year'] = pd.to_datetime(df['dt']).dt.year

# 연도별 평균 온도 계산
yearly_avg = df.groupby('Year')['LandAverageTemperature'].mean().reset_index()

# Plotly 그래프 그리기
fig = px.line(
    yearly_avg,
    x='Year',
    y='LandAverageTemperature',
    title='🌡️ 연도별 평균 기온 추이',
    labels={'LandAverageTemperature': '평균 기온 (℃)', 'Year': '연도'},
    markers=True
)

fig.show()
