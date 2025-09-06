import streamlit as st
import pandas as pd
import numpy as np

# 타이틀 설정
st.title('💧 우리 동네 물: 수질 변화 한눈에')
st.markdown("---")

# BOD와 COD 등급 기준 (환경부 하천 생활환경 기준 참고)
def get_water_quality_status(value, type):
    if type == 'BOD':
        if value <= 1.0:
            return '매우 좋음 (I등급)', 'blue'
        elif value <= 3.0:
            return '좋음 (II등급)', 'green'
        elif value <= 5.0:
            return '보통 (III등급)', 'orange'
        elif value <= 8.0:
            return '나쁨 (IV등급)', 'red'
        else:
            return '매우 나쁨 (V등급)', 'darkred'
    elif type == 'COD':
        if value <= 2.0:
            return '매우 좋음 (I등급)', 'blue'
        elif value <= 4.0:
            return '좋음 (II등급)', 'green'
        elif value <= 7.0:
            return '보통 (III등급)', 'orange'
        elif value <= 9.0:
            return '나쁨 (IV등급)', 'red'
        else:
            return '매우 나쁨 (V등급)', 'darkred'
    return '알 수 없음', 'gray'

# 한강, 공촌천, 장수천 관측소별 위도/경도 데이터
# 'river_coords' 딕셔너리에 각 강별 좌표 데이터를 저장합니다.
# 실제 좌표를 찾으시면 이 값을 수정해주세요.
river_coords = {
    '한강': pd.DataFrame({
        'lat': [37.5665, 37.5326, 37.5147],
        'lon': [126.9780, 126.9900, 127.0500],
        'name': ['한강대교', '잠실', '뚝섬']
    }),
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


# 파일 업로드 (개발 환경에서는 로컬 파일을 사용)
try:
    df = pd.read_csv('도시의_수질현황_20250906112341.csv', encoding='cp949')
except FileNotFoundError:
    st.error("데이터 파일 (도시의_수질현황_20250906112341.csv)을 찾을 수 없습니다. 파일을 업로드하거나 경로를 확인해주세요.")
    st.stop()
except UnicodeDecodeError:
    try:
        df = pd.read_csv('도시의_수질현황_20250906112341.csv', encoding='utf-8')
    except UnicodeDecodeError:
        st.error("파일 인코딩 오류가 발생했습니다. 'cp949' 또는 'utf-8' 인코딩으로 파일을 다시 확인해주세요.")
    st.stop()


# 데이터 전처리
# 파일의 '구분(1)'은 강, '구분(4)'는 관측소로 가정합니다.
df = df.rename(columns={'구분(1)': '강', '구분(4)': '관측소'})

# 수질 측정 데이터 추출 (날짜 형식으로 변환)
data_columns = df.columns[4:]
df_data = df[data_columns].transpose()
df_data.columns = df['관측소']
df_data.index = pd.to_datetime(df_data.index, format='%Y.%m')

# BOD 및 COD 데이터 추출 (예시)
# 실제 데이터의 컬럼 순서에 따라 조정이 필요합니다.
# 현재 데이터는 BOD, COD가 같은 날짜 컬럼에 섞여 있으므로, 가상의 데이터를 생성합니다.
# 실제 데이터를 분석하여 BOD, COD 컬럼을 명확히 구분해야 합니다.
# 여기서는 예시를 위해 BOD와 COD를 가상으로 분리합니다.
df_bod = df_data.iloc[::2]  # 홀수 행 데이터 (가정)
df_cod = df_data.iloc[1::2] # 짝수 행 데이터 (가정)


# 강 선택 기능으로 변경
st.sidebar.header('강 선택')
selected_river_name = st.sidebar.selectbox(
    '강을 선택하세요:',
    df['강'].unique()
)

# 선택된 강에 속한 모든 관측소의 데이터를 필터링
stations_in_river = df[df['강'] == selected_river_name]['관측소'].unique()
selected_data_bod = df_bod[stations_in_river]
selected_data_cod = df_cod[stations_in_river]

# 선택된 강 전체의 월별 BOD 및 COD 평균 계산
avg_data_bod = selected_data_bod.mean(axis=1)
avg_data_cod = selected_data_cod.mean(axis=1)

# 데이터 시각화
st.subheader(f"📊 {selected_river_name} 수질 변화 추이")
st.write("월별 BOD와 COD 변화를 시계열 그래프로 확인할 수 있습니다.")

chart_data = pd.DataFrame({
    'BOD': avg_data_bod,
    'COD': avg_data_cod,
})

# BOD, COD 그래프 표시
st.line_chart(chart_data)

st.markdown("---")
st.subheader("📌 BOD와 COD의 의미")
st.markdown("""
- **BOD (생물화학적 산소 요구량)**: 물속의 유기물을 미생물이 분해할 때 필요한 산소의 양. 수치가 높을수록 오염도가 높습니다.
- **COD (화학적 산소 요구량)**: 물속의 유기물과 무기물을 화학적으로 분해할 때 필요한 산소의 양. BOD보다 더 넓은 범위의 오염 물질을 측정합니다.
""")

st.markdown("---")
# river_coords 딕셔너리에 선택된 강이 있는지 확인
if selected_river_name in river_coords:
    st.subheader(f'🗺️ {selected_river_name} 주요 관측소 위치')
    st.write('지도에 표시된 위치는 예시이며, 실제 좌표로 수정할 수 있습니다.')
    st.map(river_coords[selected_river_name])
else:
    st.subheader("🗺️ 강 위치")
    st.write("강의 위치 데이터가 없어 지도 기능은 제공되지 않습니다.")

# BOD/COD 상태 표시 (선택된 강 전체의 최신 평균 데이터 기준)
latest_bod = avg_data_bod.iloc[-1] if not avg_data_bod.empty else 0
latest_cod = avg_data_cod.iloc[-1] if not avg_data_cod.empty else 0

bod_status, bod_color = get_water_quality_status(latest_bod, 'BOD')
cod_status, cod_color = get_water_quality_status(latest_cod, 'COD')

st.sidebar.markdown("---")
st.sidebar.subheader("⭐ 현재 수질 지표 (평균)")
st.sidebar.metric(label="BOD (mg/L)", value=f"{latest_bod:.2f}", delta_color="off")
st.sidebar.markdown(f"<div style='color:{bod_color}; font-size:1.2em;'>**BOD 상태:** {bod_status}</div>", unsafe_allow_html=True)

st.sidebar.metric(label="COD (mg/L)", value=f"{latest_cod:.2f}", delta_color="off")
st.sidebar.markdown(f"<div style='color:{cod_color}; font-size:1.2em;'>**COD 상태:** {cod_status}</div>", unsafe_allow_html=True)
