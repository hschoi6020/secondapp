# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CSV Plotly 시각화", layout="wide")
st.title("CSV 데이터 Plotly 시각화 대시보드")

# 1. CSV 업로더
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")
if not uploaded_file:
    st.info("좌측 사이드바에서 CSV 파일을 업로드해주세요.")
    st.stop()

# 2. 데이터 로드
df = pd.read_csv(uploaded_file)
st.subheader("원본 데이터 미리보기")
st.dataframe(df.head(), use_container_width=True)

# 3. 컬럼 리스트 추출
cols = df.columns.tolist()

# 4. 사용자 인터랙션
st.sidebar.header("시각화 설정")
x_axis = st.sidebar.selectbox("X 축", cols, index=0)
y_axis = st.sidebar.selectbox("Y 축", cols, index=1 if len(cols) > 1 else 0)
chart_type = st.sidebar.selectbox(
    "차트 유형 선택",
    ["선형 차트 (Line)", "산점도 (Scatter)", "막대 차트 (Bar)", "히스토그램 (Histogram)"]
)

# 5. 날짜 타입 자동 변환 옵션
is_date = False
if st.sidebar.checkbox("X 축을 날짜로 변환", value=False):
    try:
        df[x_axis] = pd.to_datetime(df[x_axis])
        is_date = True
    except Exception as e:
        st.sidebar.error(f"날짜 변환 실패: {e}")


df_filtered = df.copy()
if is_date or pd.api.types.is_numeric_dtype(df[x_axis]):
    if is_date:
        df_filtered["__year__"] = df_filtered[x_axis].dt.year
        mask = (df_filtered["__year__"] >= 1990) & (df_filtered["__year__"] <= 2015)
        df_filtered = df_filtered.loc[mask].drop(columns="__year__")
    else:
        mask = (df_filtered[x_axis] >= 1990) & (df_filtered[x_axis] <= 2015)
        df_filtered = df_filtered.loc[mask]


# 7. 필터된 데이터 미리보기
st.subheader("1950–2015 범위 데이터 미리보기")
st.dataframe(df_filtered.head(), use_container_width=True)

# 8. Plotly 차트 생성
if chart_type == "선형 차트 (Line)":
    fig = px.line(
        df_filtered,
        x=x_axis,
        y=y_axis,
        title=f"{y_axis} vs {x_axis} (1950–2015)",
        markers=True
    )
elif chart_type == "산점도 (Scatter)":
    fig = px.scatter(
        df_filtered,
        x=x_axis,
        y=y_axis,
        title=f"{y_axis} vs {x_axis} (1950–2015)",
        trendline="ols"
    )
elif chart_type == "막대 차트 (Bar)":
    fig = px.bar(
        df_filtered,
        x=x_axis,
        y=y_axis,
        title=f"{y_axis} by {x_axis} (1950–2015)"
    )
else:  # 히스토그램
    fig = px.histogram(
        df_filtered,
        x=x_axis,
        nbins=30,
        title=f"{x_axis} 분포 (1950–2015)"
    )

# 9. Plot 렌더링
st.plotly_chart(fig, use_container_width=True)
