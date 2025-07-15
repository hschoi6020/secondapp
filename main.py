import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 로드
df = pd.read_csv('dioxide.csv', sep=';')

# 'Cars' 데이터 추출
cars_data = df[df['Category'] == 'Cars'].iloc[:, 1:].T
cars_data.columns = ['CO2 Emissions']
cars_data.index = cars_data.index.astype(int)

# 타이틀과 설명
st.title('자동차 CO2 배출량 연도별 분석')
st.write("""
이 앱은 1990년부터 2016년까지의 자동차 CO2 배출량 변화를 시각화하고 간단한 분석을 제공합니다.
""")

# 라인 그래프 시각화
st.subheader('연도별 CO2 배출량 추이')
st.line_chart(cars_data)

# 기본 통계 정보
st.subheader('기본 통계')
st.write(cars_data.describe())

# 추세 분석
st.subheader('추세 요약')
start_emission = cars_data.iloc[0]['CO2 Emissions']
end_emission = cars_data.iloc[-1]['CO2 Emissions']
change
