import streamlit as st
import pandas as pd
import altair as alt

# --- 페이지 설정 ---
# 페이지 제목, 아이콘, 레이아웃을 설정합니다. st.set_page_config는 스크립트에서 가장 먼저 실행되어야 합니다.
st.set_page_config(
    page_title="이산화탄소 농도 대시보드",
    page_icon="💨",
    layout="wide"
)

# --- 데이터 로딩 ---
# 스트림릿의 캐시 기능을 사용하여 데이터 로딩 속도를 향상시킵니다.
# 파일이 없거나 오류 발생 시 사용자에게 안내 메시지를 보여줍니다.
@st.cache_data
def load_data(file_path, separator):
    """지정된 경로와 구분자로 CSV 파일을 읽어 데이터프레임으로 반환합니다."""
    try:
        df = pd.read_csv(file_path, sep=separator)
        return df
    except FileNotFoundError:
        st.error(f"'{file_path}' 파일을 찾을 수 없습니다. `app.py`와 동일한 디렉토리에 파일이 있는지 확인하세요.")
        return None
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return None

# 데이터 로드 실행
# 업로드된 파일의 구분자가 ';'임을 감안하여 sep=';' 옵션을 사용합니다.
df = load_data('dioxide.csv', separator=';')


# --- 앱 UI 구성 ---
st.title("💨 이산화탄소 농도 데이터 분석")
st.markdown("---")


# 데이터가 성공적으로 로드된 경우에만 대시보드를 표시합니다.
if df is not None:
    
    # 데이터프레임의 열 이름을 확인하기 위해 컬럼명을 출력해봅니다. (디버깅용)
    # st.write(df.columns) 
    
    # 사용자가 직접 차트에 사용할 열을 선택할 수 있도록 합니다.
    # 이렇게 하면 어떤 CSV 파일이든 유연하게 대응할 수 있습니다.
    st.sidebar.header("⚙️ 차트 옵션")
    
    # ❗️ 사용자의 CSV 파일에 맞게 열 이름을 선택하도록 유도
    st.info("💡 `dioxide.csv` 파일의 실제 날짜 열과 수치 데이터 열을 아래에서 선택해주세요.")
    
    # 사용 가능한 열 목록 (숫자형 데이터와 나머지로 구분)
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    all_cols = df.columns.tolist()
    
    x_axis = st.sidebar.selectbox("📈 X축 선택 (시간 또는 카테고리)", options=all_cols, index=0)
    y_axis = st.sidebar.selectbox("📉 Y축 선택 (수치 데이터)", options=numeric_cols, index=0 if len(numeric_cols) > 0 else None)
    
    if y_axis:
        # --- 1. 메인 차트 (라인 차트) ---
        st.header("시간에 따른 농도 변화")
        
        # Altair를 사용한 인터랙티브 차트 생성
        chart = alt.Chart(df).mark_line(
            point=alt.OverlayMarkDef(color="red", size=20) # 점(포인트) 스타일 지정
        ).encode(
            x=alt.X(x_axis, title='시간'),
            y=alt.Y(y_axis, title='농도', scale=alt.Scale(zero=False)), # y축이 0부터 시작하지 않도록 설정
            tooltip=[x_axis, y_axis] # 마우스를 올렸을 때 표시될 정보
        ).interactive() # 사용자가 줌인/줌아웃, 이동 가능하도록 설정

        st.altair_chart(chart, use_container_width=True)
        st.markdown(f"**분석:** 위 그래프는 시간에 따른 **{y_axis}**의 변화를 보여줍니다. 전반적인 추세와 특정 시점의 값을 확인할 수 있습니다.")
        
        st.markdown("---")

        # --- 2. 추가 분석 (데이터 테이블 및 통계) ---
        col1, col2 = st.columns(2)

        with col1:
            st.header("📄 원본 데이터 보기")
            st.dataframe(df)

        with col2:
            st.header("📊 주요 통계치")
            # 선택된 수치 열에 대한 기술 통계량을 보여줍니다.
            st.write(df[[y_axis]].describe())
    else:
        st.warning("차트를 그릴 수 있는 수치 데이터 열이 없습니다. 파일을 확인해주세요.")

else:
    st.warning("데이터를 불러올 수 없어 대시보드를 표시할 수 없습니다.")


# --- 푸터 ---
st.markdown("---")
st.markdown("Made with ❤️ by Gemini")
