import streamlit as st
import pandas as pd
import numpy as np

# 타이틀 설정
st.title('💧 우리 동네 물: 수질 변화 한눈에')
st.markdown("---")

# 공촌천, 장수천 관측소별 위도/경도 데이터
# 'river_coords' 딕셔너리에 각 강별 좌표 데이터를 저장합니다.
river_coords = {
    '공촌천': pd.DataFrame({
        'lat': [37.5255], 
        'lon': [126.6575],
        'name': ['공촌천'] 
    }),
    '장수천': pd.DataFrame({
        'lat': [37.4529], 
        'lon': [126.7025],
        'name': ['장수천']
    })
}

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


# 강 선택 기능으로 변경
st.sidebar.header('강 선택')
selected_river_name = st.sidebar.selectbox(
    '강을 선택하세요:',
    df['강'].unique()
)

# 지도 표시 기능만 남기기
if selected_river_name in river_coords:
    st.subheader(f'🗺️ {selected_river_name} 주요 관측소 위치')
    st.map(river_coords[selected_river_name])
else:
    st.subheader("🗺️ 강 위치")
    st.write("지도 데이터가 없어 위치를 표시할 수 없습니다.")
