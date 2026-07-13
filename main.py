import streamlit as st
import pandas as pd

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="서울-양평 도시 열섬현상 분석", layout="wide")
st.title("🏙️ 서울 vs 🌲 양평 기온 비교를 통한 도시 열섬현상 분석")
st.markdown("""
본 웹앱은 대도시(서울)와 외곽 농촌 지역(양평)의 기온 데이터를 비교하여 **도시 열섬현상(Urban Heat Island Effect)**을 시각적으로 확인하기 위해 제작되었습니다.
- **데이터 출처:** 기상청 공공데이터 (2025년 시간별 기온 데이터)
""")

# 2. 데이터 로드 함수 (성능 향상을 위한 캐싱 적용)
@st.cache_data
def load_data():
    # 파일 읽기 (요청하신 cp949 인코딩 적용)
    seoul = pd.read_csv("서울_기온.csv", encoding="cp949")
    yangpyeong = pd.read_csv("양평_기온.csv", encoding="cp949")
    
    # 일시 컬럼을 datetime 형식으로 변환
    seoul['일시'] = pd.to_datetime(seoul['일시'])
    yangpyeong['일시'] = pd.to_datetime(yangpyeong['일시'])
    
    # 분석에 필요한 월(Month), 시(Hour) 컬럼 생성
    seoul['월'] = seoul['일시'].dt.month
    seoul['시'] = seoul['일시'].dt.hour
    yangpyeong['월'] = yangpyeong['일시'].dt.month
    yangpyeong['시'] = yangpyeong['일시'].dt.hour
    
    # 필요한 컬럼만 추출 후 병합을 위해 이름 변경
    seoul_sub = seoul[['일시', '월', '시', '기온(°C)']].rename(columns={'기온(°C)': '서울_기온'})
    yang_sub = yangpyeong[['일시', '월', '시', '기온(°C)']].rename(columns={'기온(°C)': '양평_기온'})
    
    # 일시 기준으로 두 데이터 병합
    df = pd.merge(seoul_sub, yang_sub, on=['일시', '월', '시'], how='inner')
    
    # 두 지역의 기온 차이 계산 (서울 - 양평)
    df['기온차(서울-양평)'] = df['서울_기온'] - df['양평_기온']
    return df

try:
    df = load_data()
    
    # 데이터 요약 정보 사이드바 표시
    st.sidebar.header("📊 데이터 요약 (2025년)")
    st.sidebar.metric("서울 평균 기온", f"{df['서울_기온'].mean():.1f} °C")
    st.sidebar.metric("양평 평균 기온", f"{df['양평_기온'].mean():.1f} °C")
    st.sidebar.metric("평균 기온차 (서울-양평)", f"{df['기온차(서울-양평)'].mean():.1f} °C")

    # ----------------------------------------------------
    # ① 1년간 두 지역의 기온 변화 (선그래프)
    # ----------------------------------------------------
    st.subheader("① 1년간 두 지역의 기온 변화 (시간별)")
    
    # streamlit 내장 line_chart 사용을 위해 데이터 가공
    chart_df = df.set_index('일시')[['서울_기온', '양평_기온']]
    st.line_chart(chart_df, color=["#ff4b4b", "#0068c9"])
    
    # 하단 레이아웃을 좌우 2분할(Column)하여 막대그래프 배치
    col1, col2 = st.columns(2)
    
    with col1:
        # ----------------------------------------------------
        # ② 시각(0~23시)별 평균 기온차 (막대그래프)
        # ----------------------------------------------------
        st.subheader("② 시각별 평균 기온차 (서울-양평)")
        hour_diff = df.groupby('시')['기온차(서울-양평)'].mean()
        st.bar_chart(hour_diff, color="#ffaa00")
        st.caption("주로 야간과 새벽 시간에 서울의 기온이 양평보다 확연히 높은 도시 열섬현상이 관찰됩니다.")
        
    with col2:
        # ----------------------------------------------------
        # ③ 월(1~12월)별 평균 기온차 (막대그래프)
        # ----------------------------------------------------
        st.subheader("③ 월별 평균 기온차 (서울-양평)")
        month_diff = df.groupby('월')['기온차(서울-양평)'].mean()
        st.bar_chart(month_diff, color="#29b5e8")
        st.caption("계절별로 도시와 외곽 지역 간의 기온 차이가 어떻게 변화하는지 확인할 수 있습니다.")

except FileNotFoundError:
    st.error("❌ '서울_기온.csv' 또는 '양평_기온.csv' 파일을 찾을 수 없습니다. 웹앱 스크립트(`app.py`)와 같은 폴더에 위치시켜 주세요.")
