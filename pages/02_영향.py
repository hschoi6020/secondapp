import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import io

# 페이지 설정
st.set_page_config(
    page_title="지구 평균 기온 상승의 기후변화 및 생태계 영향",
    page_icon="🌍",
    layout="wide"
)

# 제목 및 헤더
st.title("🌍 지구 평균 기온 상승의 기후변화 및 생태계 영향")
st.markdown("### 🚗 자동차 CO2 배출량이 미치는 복합적 환경 영향 분석")
st.markdown("---")

# 사이드바
st.sidebar.header("🔧 분석 설정")
temperature_scenario = st.sidebar.selectbox(
    "기온 상승 시나리오",
    ["현재 추세", "1.5°C 제한", "2°C 제한", "3°C 상승"],
    index=0
)
show_predictions = st.sidebar.checkbox("2030년 예측 표시", value=True)
impact_severity = st.sidebar.slider("영향 강도 조정", 0.5, 2.0, 1.0, 0.1)

# 데이터 생성 함수
@st.cache_data
def load_comprehensive_data():
    # 기존 CO2 데이터
    csv_data = """Category;1990;1991;1992;1993;1994;1995;1996;1997;1998;1999;2000;2001;2002;2003;2004;2005;2006;2007;2008;2009;2010;2011;2012;2013;2014;2015;2016
Cars;5.947;6.020;6.228;6.498;6.688;6.978;7.127;7.146;7.244;7.534;7.720;7.671;7.840;8.278;8.650;8.813;8.927;8.837;9.086;9.059;9.104;9.114;9.450;9.384;9.144;9.532;10.123"""
    
    df = pd.read_csv(io.StringIO(csv_data), sep=';')
    cars_row = df[df['Category'] == 'Cars'].iloc[0]
    years = [col for col in df.columns if col != 'Category']
    car_emissions = [float(cars_row[year]) for year in years]
    
    np.random.seed(42)
    
    # 기온 데이터 생성
    base_temp = 14.0
    temp_increase = [(emission - car_emissions[0]) * 0.15 * impact_severity for emission in car_emissions]
    temp_noise = np.random.normal(0, 0.08, len(car_emissions))
    temperatures = [base_temp + increase + n for increase, n in zip(temp_increase, temp_noise)]
    
    # 기후변화 지표 생성
    extreme_weather_events = []
    sea_level_rise = []
    glacier_loss = []
    
    for i, temp in enumerate(temperatures):
        temp_anomaly = temp - base_temp
        
        # 극한 기후 사건 (기온 상승에 따라 지수적 증가)
        base_events = 12
        extreme_events = base_events + (temp_anomaly ** 2) * 15 + np.random.normal(0, 2)
        extreme_weather_events.append(max(base_events, extreme_events))
        
        # 해수면 상승 (mm/년)
        base_sea_level = 1.5
        sea_rise = base_sea_level + temp_anomaly * 0.8 + np.random.normal(0, 0.1)
        sea_level_rise.append(max(0, sea_rise))
        
        # 빙하 손실 (% 감소)
        base_loss = 0.5
        glacier_loss_rate = base_loss + temp_anomaly * 1.2 + np.random.normal(0, 0.15)
        glacier_loss.append(max(0, glacier_loss_rate))
    
    # 생태계 영향 지표 생성
    biodiversity_loss = []
    coral_bleaching = []
    forest_fire_area = []
    species_migration = []
    
    for i, temp in enumerate(temperatures):
        temp_anomaly = temp - base_temp
        
        # 생물다양성 손실 (% 감소)
        base_biodiversity = 2.0
        bio_loss = base_biodiversity + temp_anomaly * 3.5 + np.random.normal(0, 0.3)
        biodiversity_loss.append(max(0, bio_loss))
        
        # 산호초 백화 현상 (% 영향)
        base_coral = 5.0
        coral_impact = base_coral + (temp_anomaly ** 1.5) * 25 + np.random.normal(0, 2)
        coral_bleaching.append(max(0, min(100, coral_impact)))
        
        # 산불 면적 (천 헥타르)
        base_fire = 500
        fire_area = base_fire + temp_anomaly * 800 + np.random.normal(0, 100)
        forest_fire_area.append(max(base_fire, fire_area))
        
        # 종 이동 거리 (km)
        base_migration = 50
        migration_distance = base_migration + temp_anomaly * 120 + np.random.normal(0, 15)
        species_migration.append(max(0, migration_distance))
    
    # 데이터프레임 생성
    result_df = pd.DataFrame({
        'Year': [int(year) for year in years],
        'Car_CO2_Emissions': car_emissions,
        'Average_Temperature': temperatures,
        'Extreme_Weather_Events': extreme_weather_events,
        'Sea_Level_Rise': sea_level_rise,
        'Glacier_Loss': glacier_loss,
        'Biodiversity_Loss': biodiversity_loss,
        'Coral_Bleaching': coral_bleaching,
        'Forest_Fire_Area': forest_fire_area,
        'Species_Migration': species_migration
    })
    
    return result_df

# 데이터 로드
df = load_comprehensive_data()

# 상관계수 계산
temp_correlation = df['Car_CO2_Emissions'].corr(df['Average_Temperature'])
climate_correlations = {
    'Extreme_Weather': df['Average_Temperature'].corr(df['Extreme_Weather_Events']),
    'Sea_Level': df['Average_Temperature'].corr(df['Sea_Level_Rise']),
    'Glacier_Loss': df['Average_Temperature'].corr(df['Glacier_Loss'])
}
ecosystem_correlations = {
    'Biodiversity': df['Average_Temperature'].corr(df['Biodiversity_Loss']),
    'Coral_Bleaching': df['Average_Temperature'].corr(df['Coral_Bleaching']),
    'Forest_Fire': df['Average_Temperature'].corr(df['Forest_Fire_Area']),
    'Species_Migration': df['Average_Temperature'].corr(df['Species_Migration'])
}

# 메인 대시보드 레이아웃
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.metric(
        "🌡️ 평균 기온 상승", 
        f"{df['Average_Temperature'].iloc[-1] - df['Average_Temperature'].iloc[0]:.1f}°C",
        f"{temp_correlation:.3f} (CO2 상관관계)"
    )

with col2:
    st.metric(
        "🚗 CO2 배출량 증가", 
        f"{df['Car_CO2_Emissions'].iloc[-1] - df['Car_CO2_Emissions'].iloc[0]:.1f}M톤",
        f"{(df['Car_CO2_Emissions'].iloc[-1] / df['Car_CO2_Emissions'].iloc[0] - 1) * 100:.1f}%"
    )

with col3:
    st.metric(
        "⚠️ 극한 기후 사건", 
        f"{df['Extreme_Weather_Events'].iloc[-1]:.0f}건",
        f"{df['Extreme_Weather_Events'].iloc[-1] - df['Extreme_Weather_Events'].iloc[0]:.0f}건 증가"
    )

st.markdown("---")

# 기후변화 영향 분석
st.subheader("🌊 기후변화 영향 분석")

col4, col5 = st.columns([2, 1])

with col4:
    # 기후변화 지표 시각화
    fig_climate = make_subplots(
        rows=2, cols=2,
        subplot_titles=('극한 기후 사건 (연간 발생 건수)', '해수면 상승 (mm/년)', 
                       '빙하 손실 (% 감소)', '평균 기온 변화 (°C)'),
        vertical_spacing=0.1,
        horizontal_spacing=0.1
    )
    
    # 극한 기후 사건
    fig_climate.add_trace(
        go.Scatter(x=df['Year'], y=df['Extreme_Weather_Events'], 
                  mode='lines+markers', name='극한 기후 사건',
                  line=dict(color='red', width=2)),
        row=1, col=1
    )
    
    # 해수면 상승
    fig_climate.add_trace(
        go.Scatter(x=df['Year'], y=df['Sea_Level_Rise'], 
                  mode='lines+markers', name='해수면 상승',
                  line=dict(color='blue', width=2)),
        row=1, col=2
    )
    
    # 빙하 손실
    fig_climate.add_trace(
        go.Scatter(x=df['Year'], y=df['Glacier_Loss'], 
                  mode='lines+markers', name='빙하 손실',
                  line=dict(color='lightblue', width=2)),
        row=2, col=1
    )
    
    # 평균 기온
    fig_climate.add_trace(
        go.Scatter(x=df['Year'], y=df['Average_Temperature'], 
                  mode='lines+markers', name='평균 기온',
                  line=dict(color='orange', width=2)),
        row=2, col=2
    )
    
    fig_climate.update_layout(
        height=500,
        title_text="기후변화 주요 지표 변화 추이",
        showlegend=False
    )
    
    st.plotly_chart(fig_climate, use_container_width=True)

with col5:
    st.markdown("### 📊 기후변화 상관관계")
    
    for indicator, corr in climate_correlations.items():
        if corr > 0.7:
            status = "🔴 강한 상관관계"
        elif corr > 0.4:
            status = "🟡 중간 상관관계"
        else:
            status = "🟢 약한 상관관계"
        
        st.metric(indicator.replace('_', ' '), f"{corr:.3f}", status)
    
    st.markdown("### 🌍 주요 영향")
    st.markdown("""
    - **극한 기후**: 폭염, 홍수, 가뭄 빈도 증가
    - **해수면**: 연간 상승률 지속적 증가
    - **빙하**: 전 세계 빙하 면적 감소
    - **기온**: 지속적인 상승 트렌드
    """)

st.markdown("---")

# 생태계 영향 분석
st.subheader("🦋 생태계 파괴 영향 분석")

col6, col7 = st.columns([2, 1])

with col6:
    # 생태계 지표 시각화
    fig_eco = make_subplots(
        rows=2, cols=2,
        subplot_titles=('생물다양성 손실 (%)', '산호초 백화 현상 (%)', 
                       '산불 면적 (천 헥타르)', '종 이동 거리 (km)'),
        vertical_spacing=0.1,
        horizontal_spacing=0.1
    )
    
    # 생물다양성 손실
    fig_eco.add_trace(
        go.Scatter(x=df['Year'], y=df['Biodiversity_Loss'], 
                  mode='lines+markers', name='생물다양성 손실',
                  line=dict(color='darkgreen', width=2)),
        row=1, col=1
    )
    
    # 산호초 백화
    fig_eco.add_trace(
        go.Scatter(x=df['Year'], y=df['Coral_Bleaching'], 
                  mode='lines+markers', name='산호초 백화',
                  line=dict(color='coral', width=2)),
        row=1, col=2
    )
    
    # 산불 면적
    fig_eco.add_trace(
        go.Scatter(x=df['Year'], y=df['Forest_Fire_Area'], 
                  mode='lines+markers', name='산불 면적',
                  line=dict(color='orangered', width=2)),
        row=2, col=1
    )
    
    # 종 이동
    fig_eco.add_trace(
        go.Scatter(x=df['Year'], y=df['Species_Migration'], 
                  mode='lines+markers', name='종 이동',
                  line=dict(color='purple', width=2)),
        row=2, col=2
    )
    
    fig_eco.update_layout(
        height=500,
        title_text="생태계 파괴 주요 지표 변화 추이",
        showlegend=False
    )
    
    st.plotly_chart(fig_eco, use_container_width=True)

with col7:
    st.markdown("### 🌿 생태계 상관관계")
    
    for indicator, corr in ecosystem_correlations.items():
        if corr > 0.7:
            status = "🔴 강한 상관관계"
        elif corr > 0.4:
            status = "🟡 중간 상관관계"
        else:
            status = "🟢 약한 상관관계"
        
        st.metric(indicator.replace('_', ' '), f"{corr:.3f}", status)
    
    st.markdown("### 🦋 생태계 위기")
    st.markdown("""
    - **생물다양성**: 멸종 위기 종 증가
    - **산호초**: 백화 현상 심화
    - **산불**: 대형 산불 빈발
    - **서식지**: 종의 서식지 이동
    """)

# 통합 영향 분석
st.markdown("---")
st.subheader("🔄 통합 영향 분석")

col8, col9 = st.columns([3, 1])

with col8:
    # 통합 상관관계 히트맵
    correlation_matrix = df[['Average_Temperature', 'Extreme_Weather_Events', 'Sea_Level_Rise', 
                            'Glacier_Loss', 'Biodiversity_Loss', 'Coral_Bleaching', 
                            'Forest_Fire_Area', 'Species_Migration']].corr()
    
    fig_heatmap = px.imshow(
        correlation_matrix,
        title="환경 지표 간 상관관계 히트맵",
        color_continuous_scale='RdYlBu_r',
        aspect="auto"
    )
    
    fig_heatmap.update_layout(height=400)
    st.plotly_chart(fig_heatmap, use_container_width=True)

with col9:
    st.markdown("### 🎯 핵심 발견")
    
    # 가장 높은 상관관계 찾기
    temp_corr_values = [
        correlation_matrix.loc['Average_Temperature', col] 
        for col in correlation_matrix.columns 
        if col != 'Average_Temperature'
    ]
    max_corr_idx = np.argmax(temp_corr_values)
    max_corr_indicator = [col for col in correlation_matrix.columns if col != 'Average_Temperature'][max_corr_idx]
    
    st.success(f"**가장 강한 상관관계:**\n{max_corr_indicator.replace('_', ' ')}")
    st.info(f"상관계수: {max(temp_corr_values):.3f}")

# 시나리오 예측
if show_predictions:
    st.markdown("---")
    st.subheader("🔮 2030년 예측 시나리오")
    
    # 예측 데이터 생성
    future_emission = 12.5  # 예상 2030년 배출량
    future_temp = 14.0 + (future_emission - df['Car_CO2_Emissions'].iloc[0]) * 0.15 * impact_severity
    
    col10, col11, col12 = st.columns(3)
    
    with col10:
        st.markdown("#### 🌡️ 기후 예측")
        st.metric("예상 기온", f"{future_temp:.1f}°C")
        st.metric("극한 기후 사건", f"{12 + (future_temp - 14.0)**2 * 15:.0f}건")
        st.metric("해수면 상승", f"{1.5 + (future_temp - 14.0) * 0.8:.1f}mm/년")
    
    with col11:
        st.markdown("#### 🌊 환경 예측")
        st.metric("빙하 손실", f"{0.5 + (future_temp - 14.0) * 1.2:.1f}%")
        st.metric("생물다양성 손실", f"{2.0 + (future_temp - 14.0) * 3.5:.1f}%")
        st.metric("산호초 백화", f"{min(100, 5.0 + (future_temp - 14.0)**1.5 * 25):.0f}%")
    
    with col12:
        st.markdown("#### 🦋 생태계 예측")
        st.metric("산불 면적", f"{500 + (future_temp - 14.0) * 800:.0f}천ha")
        st.metric("종 이동 거리", f"{50 + (future_temp - 14.0) * 120:.0f}km")

# 데이터 테이블
st.markdown("---")
st.subheader("📋 통합 데이터")

# 주요 지표만 표시
display_columns = ['Year', 'Car_CO2_Emissions', 'Average_Temperature', 
                  'Extreme_Weather_Events', 'Biodiversity_Loss', 'Coral_Bleaching']
display_df = df[display_columns].copy()

st.dataframe(display_df.style.format({
    'Car_CO2_Emissions': '{:.2f}',
    'Average_Temperature': '{:.2f}',
    'Extreme_Weather_Events': '{:.0f}',
    'Biodiversity_Loss': '{:.1f}',
    'Coral_Bleaching': '{:.1f}'
}), use_container_width=True)

# 결론 및 행동 방안
st.markdown("---")
st.subheader("🎯 결론 및 대응 방안")

conclusion_col1, conclusion_col2, conclusion_col3 = st.columns(3)

with conclusion_col1:
    st.markdown("""
    ### 🚨 주요 발견
    - **연쇄 반응**: CO2 배출량 증가가 기후변화와 생태계 파괴의 연쇄 반응 촉발
    - **가속화**: 기온 상승에 따른 환경 영향이 지수적으로 증가
    - **불가역성**: 일부 생태계 변화는 되돌릴 수 없는 임계점 근접
    """)

with conclusion_col2:
    st.markdown("""
    ### 🌍 환경 영향
    - **기후 시스템**: 극한 기후 사건 빈발, 해수면 상승 가속화
    - **생태계**: 생물다양성 급격한 감소, 서식지 파괴
    - **인간 사회**: 식량 안보, 수자원, 거주 환경 위협
    """)

with conclusion_col3:
    st.markdown("""
    ### 🛡️ 대응 방안
    - **탄소 중립**: 2050년 탄소 중립 목표 달성
    - **친환경 교통**: 전기차, 대중교통 확대
    - **생태 보전**: 보호구역 확대, 복원 사업 추진
    """)

# 경고 메시지
st.markdown("---")
st.error("""
⚠️ **긴급 행동 필요**: 현재 추세가 지속될 경우 돌이킬 수 없는 환경 파괴가 발생할 수 있습니다. 
개인, 기업, 정부 차원의 즉각적인 대응이 필요합니다.
""")

# 푸터
st.markdown("---")
st.markdown("*이 분석은 교육 목적으로 제작되었으며, 실제 환경 데이터는 더 복잡한 상호작용을 포함합니다.*")
