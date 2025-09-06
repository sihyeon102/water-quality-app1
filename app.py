import streamlit as st
import pandas as pd
import numpy as np

# 타이틀 설정
st.title('💧 우리 동네 물: 수질 변화 한눈에')
st.markdown("---")

# 공촌천, 장수천 관측소별 위도/경도 데이터
# 지도에 표시할 모든 하천의 위치를 하나의 데이터프레임으로 만듭니다.
all_river_coords = pd.DataFrame({
    'lat': [37.5255, 37.4529], 
    'lon': [126.6575, 126.7025],
    'name': ['공촌천', '장수천']
})

# GitHub Raw 데이터 URL
data_url = 'https://raw.githubusercontent.com/sihyeon102/water-quality-app1/main/%EB%8F%84%EC%8B%9C%EC%9D%98_%EC%88%98%EC%A7%88%ED%98%84%ED%99%A9_20250906112341.csv'

# 파일 업로드 (개발 환경에서는 로컬 파일을 사용)
try:
    df = pd.read_csv(data_url, encoding='cp949')
except Exception as e:
    st.error(f"데이터 파일을 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()


# 데이터 전처리
# 파일의 '구분(1)'은 강, '구분(4)'는 관측소로 가정합니다.
df = df.rename(columns={'구분(1)': '강', '구분(4)': '관측소'})

# 모든 하천의 위치를 표시하는 지도
st.subheader('🗺️ 공촌천과 장수천 위치')
st.map(all_river_coords)

# 선택 기능으로 변경
st.sidebar.header('데이터 조회')
selected_river_name = st.sidebar.selectbox(
    '정보를 보고 싶은 강을 선택하세요:',
    all_river_coords['name'].unique()
)

# 선택한 강의 데이터만 필터링
filtered_df = df[df['강'] == selected_river_name]
if not filtered_df.empty:
    st.markdown("---")
    st.subheader(f"📊 {selected_river_name} 수질 정보")

    # 최근 월 데이터 가져오기 (컬럼 이름에 따라 유동적으로 변경)
    latest_month = "2025.04"
    if latest_month not in filtered_df.columns:
        latest_month_column_names = [col for col in filtered_df.columns if col.startswith("2025")]
        if latest_month_column_names:
            latest_month = latest_month_column_names[-1]
    
    if latest_month in filtered_df.columns:
        try:
            latest_data = filtered_df[[latest_month]]
            # BOD, COD를 평균 내어 표시 (실제 데이터에 맞게 BOD, COD 컬럼을 명확히 지정해야 함)
            bod_data = latest_data.iloc[0, 0]
            cod_data = latest_data.iloc[0, 1]

            st.metric(label="생물학적 산소 요구량 (BOD)", value=f"{bod_data} mg/L")
            st.metric(label="화학적 산소 요구량 (COD)", value=f"{cod_data} mg/L")

        except Exception as e:
            st.error(f"데이터를 표시하는 중 오류가 발생했습니다. 데이터 파일의 열이름을 확인해주세요.")
            st.stop()
    else:
        st.write("선택한 강에 대한 최신 수질 데이터가 없습니다.")
