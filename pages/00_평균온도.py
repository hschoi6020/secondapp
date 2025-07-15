import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="로컬 CSV Plotly 시각화", layout="wide")
st.title("로컬 CSV 파일 Plotly 시각화 대시보드")

# 1. 로컬 파일 경로 지정
CSV_PATH = "dioxide.csv"  # 또는 "dioxide - dioxide (1).csv"

# 2. 데이터 로드
@st.cache_data
def load_data(path):
    return pd.read_csv(path)

df = load_data(CSV_PATH)

# 3. 데이터 미리보기
st.subheader("데이터 미리보기")
st.dataframe(df.head(), use_container_width=True)

# 4. 컬럼 리스트 추출
cols = df.columns.tolist()

# 5. 사이드바 설정
st.sidebar.header("시각화 설정")
x_axis = st.sidebar.selectbox("X 축", cols, index=0)
y_axis = st.sidebar.selectbox("Y 축", cols, index=1 if len(cols) > 1 else 0)
chart_type = st.sidebar.selectbox(
    "차트 유형 선택",
    ["선형 차트 (Line)", "산점도 (Scatter)", "막대 차트 (Bar)", "히스토그램 (Histogram)"]
)

# 6. 날짜 타입 자동 변환 옵션
if st.sidebar.checkbox("X 축을 날짜로 변환", value=False):
    try:
        df[x_axis] = pd.to_datetime(df[x_axis])
    except Exception as e:
        st.sidebar.error(f"날짜 변환 실패: {e}")

# 7. Plotly 차트 생성
if chart_type == "선형 차트 (Line)":
    fig = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}", markers=True)
elif chart_type == "산점도 (Scatter)":
    fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}", trendline="ols")
elif chart_type == "막대 차트 (Bar)":
    fig = px.bar(df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
else:
    fig = px.histogram(df, x=x_axis, nbins=30, title=f"{x_axis} 분포")

# 8. 차트 렌더링
st.plotly_chart(fig, use_container_width=True)
