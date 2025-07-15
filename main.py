import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🚗 연도별 자동차 데이터 시각화")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file:
    # 데이터 읽기
    df = pd.read_csv(uploaded_file)

    # 연도 컬럼 추정: 'year', 'model_year' 등 포함된 열 찾기
    year_cols = [col for col in df.columns if 'year' in col.lower()]

    if not year_cols:
        st.error("⚠️ 'year'가 포함된 연도 관련 열을 찾을 수 없습니다.")
    else:
        year_col = st.selectbox("연도 컬럼을 선택하세요", year_cols)

        # 연도별 개수 집계
        year_count = df[year_col].value_counts().sort_index().reset_index()
        year_count.columns = ['Year', 'Count']

        # Plotly 그래프
        fig = px.bar(year_count, x='Year', y='Count',
                     labels={'Year': '연도', 'Count': '자동차 수'},
                     title='연도별 자동차 등록 수')

        st.plotly_chart(fig)
