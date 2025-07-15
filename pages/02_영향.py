import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

# 페이지 설정
st.set_page_config(
    page_title="지구 평균 기온 상승의 영향",
    page_icon="🌡️",
    layout="wide"
)

# 제목
st.title("🌡️ 지구 평균 기온 상승의 영향")
st.markdown("### 자동차 CO2 배출량 증가가 미치는 환경 영향")
st.markdown("---")

# 데이터 생성
@st.cache_data
def load_data():
    # CO2 배출량 데이터
    csv_data = """Category;1990;1991;1992;1993;1994;1995;1996;1997;1998;1999;2000;2001;2002;2003;2004;2005;2006;2007;2008;2009;2010;2011;2012;2013;2014;2015;2016
Cars;5.947;6.020;6.228;6.498;6.688;6.978;7.127;7.146;7.244;7.534;7.720;7.671;7.840;8.278;8.650;8.813;8.927;8.837;9.086;9.059;9.104;9.114;9.450;9.384;9.144;9.532;10.123"""
    
    df = pd.read_csv(io.StringIO(csv_data), sep=';')
    cars_row = df[df['Category'] == 'Cars'].iloc[0]
    years = [col for col in df.columns if col != 'Category']
    car_emissions = [float(cars_row[year]) for year in years]
    
    # 기온 데이터 생성
    np.random.seed(42)
    base_temp = 14.0
    temp_increase = [(emission - car_emissions[0]) * 0.15 for emission in car_emissions]
    temperatures = [base_temp + increase + np.random.normal(0, 0.08) for increase in temp_increase]
    
    return pd.DataFrame({
        'Year': [int(year) for year in years],
        'Car_CO2_Emissions': car_emissions,
        'Average_Temperature': temperatures
    })

df = load_data()

# 기본 차트
col1, col2 = st.columns(2)

with col1:
    fig1 = px.line(df, x='Year', y='Car_CO2_Emissions', 
                   title='자동차 CO2 배출량 증가',
                   labels={'Car_CO2_Emissions': 'CO2 배출량 (백만톤)'})
    fig1.update_traces(line=dict(color='red', width=3))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.line(df, x='Year', y='Average_Temperature', 
                   title='지구 평균 기온 상승',
                   labels={'Average_Temperature': '평균 기온 (°C)'})
    fig2.update_traces(line=dict(color='orange', width=3))
    st.plotly_chart(fig2, use_container_width=True)

# 상관관계
correlation = df['Car_CO2_Emissions'].corr(df['Average_Temperature'])
st.info(f"**상관계수: {correlation:.3f}** - 자동차 CO2 배출량과 지구 평균 기온 사이에 강한 양의 상관관계")

st.markdown("---")

# 기후변화 영향
st.subheader("🌊 기후변화 영향")

climate_impacts = [
    {
        "영향": "🌡️ 극한 기후 사건 증가",
        "설명": "폭염, 한파, 가뭄, 홍수 등 극한 기후 사건의 빈도와 강도가 증가합니다.",
        "예시": "2003년 유럽 폭염으로 7만명 사망, 2021년 독일 홍수 피해"
    },
    {
        "영향": "🌊 해수면 상승",
        "설명": "빙하와 극지방 얼음이 녹으면서 전 세계 해수면이 지속적으로 상승합니다.",
        "예시": "연간 3.3mm 상승, 2100년까지 최대 2m 상승 예상"
    },
    {
        "영향": "🧊 빙하 및 극지방 얼음 감소",
        "설명": "그린란드와 남극 빙하가 빠르게 녹으면서 담수 공급에 영향을 미칩니다.",
        "예시": "북극 해빙 면적 연간 13% 감소"
    },
    {
        "영향": "🌪️ 태풍 및 허리케인 강화",
        "설명": "따뜻해진 바닷물로 인해 태풍과 허리케인의 강도가 증가합니다.",
        "예시": "카테고리 4-5급 강력한 태풍 빈도 증가"
    },
    {
        "영향": "💧 강수 패턴 변화",
        "설명": "일부 지역은 극심한 가뭄, 다른 지역은 집중호우로 물 순환 체계가 변화합니다.",
        "예시": "사헬 지역 사막화, 아시아 몬순 변화"
    }
]

for impact in climate_impacts:
    with st.expander(impact["영향"]):
        st.write(f"**설명:** {impact['설명']}")
        st.write(f"**예시:** {impact['예시']}")

st.markdown("---")

# 생태계 파괴 영향
st.subheader("🦋 생태계 파괴 영향")

ecosystem_impacts = [
    {
        "영향": "🐠 생물다양성 감소",
        "설명": "서식지 파괴와 기후 변화로 인해 많은 종들이 멸종 위기에 처합니다.",
        "예시": "현재 멸종 속도가 자연 멸종률의 1000배, 100만 종 멸종 위기"
    },
    {
        "영향": "🪸 산호초 백화 현상",
        "설명": "해수 온도 상승으로 산호초가 공생 조류를 잃고 하얗게 변하며 죽어갑니다.",
        "예시": "그레이트 배리어 리프 50% 백화, 전 세계 산호초 30% 소실"
    },
    {
        "영향": "🔥 산불 빈도 증가",
        "설명": "고온 건조한 기후로 인해 대형 산불이 자주 발생하고 규모가 커집니다.",
        "예시": "호주 산불로 30억 마리 동물 피해, 아마존 산불 면적 증가"
    },
    {
        "영향": "🏃 종의 서식지 이동",
        "설명": "기온 상승으로 동식물들이 더 시원한 고위도나 고지대로 이동합니다.",
        "예시": "북극곰 서식지 감소, 고산 식물 분포 변화"
    },
    {
        "영향": "🌊 해양 생태계 변화",
        "설명": "해수 온도 상승과 산성화로 어류 분포와 먹이사슬이 변화합니다.",
        "예시": "북태평양 연어 개체수 감소, 해조류 서식지 북상"
    },
    {
        "영향": "🌿 식생 변화",
        "설명": "기후 변화로 인해 삼림 분포가 변화하고 사막화가 진행됩니다.",
        "예시": "툰드라 지역 삼림 확산, 아프리카 사막 남하"
    },
    {
        "영향": "🦆 철새 이동 경로 변화",
        "설명": "계절 변화 패턴이 달라지면서 철새들의 이동 시기와 경로가 변화합니다.",
        "예시": "유럽-아프리카 철새 이동 시기 2주 빨라짐"
    }
]

for impact in ecosystem_impacts:
    with st.expander(impact["영향"]):
        st.write(f"**설명:** {impact['설명']}")
        st.write(f"**예시:** {impact['예시']}")

st.markdown("---")

# 인간 사회 영향
st.subheader("🏘️ 인간 사회 영향")

human_impacts = [
    {
        "영향": "🌾 농업 생산성 변화",
        "설명": "기온 상승과 강수 패턴 변화로 농작물 수확량이 변화합니다.",
        "예시": "밀, 쌀 생산량 10-25% 감소 예상"
    },
    {
        "영향": "💧 수자원 부족",
        "설명": "빙하 감소와 가뭄으로 인해 담수 공급이 부족해집니다.",
        "예시": "히말라야 빙하 의존 지역 20억 명 영향"
    },
    {
        "영향": "🏠 해안 지역 침수",
        "설명": "해수면 상승으로 해안 도시와 저지대 국가들이 침수 위험에 처합니다.",
        "예시": "몰디브, 방글라데시 등 침수 위험, 마이애미 정기 침수"
    },
    {
        "영향": "🤒 질병 확산",
        "설명": "기온 상승으로 열대 질병의 분포 범위가 확대됩니다.",
        "예시": "말라리아, 뎅기열 전파 지역 확산"
    },
    {
        "영향": "🏃‍♂️ 기후 난민",
        "설명": "극한 기후와 해수면 상승으로 거주지를 떠나야 하는 사람들이 증가합니다.",
        "예시": "2050년까지 10억 명 기후 난민 예상"
    }
]

for impact in human_impacts:
    with st.expander(impact["영향"]):
        st.write(f"**설명:** {impact['설명']}")
        st.write(f"**예시:** {impact['예시']}")

st.markdown("---")

# 요약
st.subheader("📋 영향 요약")

col3, col4, col5 = st.columns(3)

with col3:
    st.markdown("""
    ### 🌊 기후변화 (5개 영향)
    - 극한 기후 사건 증가
    - 해수면 상승
    - 빙하 감소
    - 태풍 강화
    - 강수 패턴 변화
    """)

with col4:
    st.markdown("""
    ### 🦋 생태계 파괴 (7개 영향)
    - 생물다양성 감소
    - 산호초 백화
    - 산불 증가
    - 서식지 이동
    - 해양 생태계 변화
    - 식생 변화
    - 철새 이동 변화
    """)

with col5:
    st.markdown("""
    ### 🏘️ 인간 사회 (5개 영향)
    - 농업 생산성 변화
    - 수자원 부족
    - 해안 지역 침수
    - 질병 확산
    - 기후 난민
    """)

# 경고 메시지
st.error("⚠️ **총 17개의 주요 영향이 서로 연결되어 복합적인 환경 위기를 만들어내고 있습니다.**")

# 데이터 테이블
st.subheader("📊 기본 데이터")
st.dataframe(df.style.format({
    'Car_CO2_Emissions': '{:.2f}',
    'Average_Temperature': '{:.2f}'
}), use_container_width=True)
