import pandas as pd
import plotly.express as px

# CSV 파일 로드
df = pd.read_csv("goog4_request&X-Goog-Date=20250715T005625Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=4b8b2d8ea55d798f9f6a49912c6857674cad98d9810d67e8975c49d11195873e84cb348a77e8e8d0fc1487efc74cbf6888ca67f24543dbb8d1f4d8e72665120443b7d7cbf0bc4cd4eddfe1015493e0e286d3bdc4357792c229151c6870f7a8a7bbadc9207e897eb53c05a8eafe02df992f20eb1a636a2445c2eef362070b404a971c3f149e3c3bcedc6da99f36104e16ecbde425ee2943abe2a53ae525841fd2b55cb18ba9be9fae431aac3ccfb54c0ae6fe999af8b02501b047ce7946bc25cf7c398631f1d9a7a8ce7c783a2ab04bb1319bb2d6c671643e9879b4c22c83e8d8b9e530af997f93fe8580ff86ed10511c6a09dd03cf66fcd80b4e275c534a5ffc.csv")  # ← 여기에 파일 경로 입력

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
