import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import koreanize_matplotlib  # 클라우드 환경에서 한글 깨짐을 완벽하게 해결합니다.
import os

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="Smart Scatter Explorer", layout="wide")
st.title("📊 Smart Scatter Explorer")
st.markdown("데이터의 상관관계를 분석하고 시점화하는 도구입니다.")

# 2. 데이터 불러오기 함수
file_name = '6주차_실습4.csv'

@st.cache_data
def load_data(file_path):
    if os.path.exists(file_path):
        try:
            # 한글 인코딩 대응 (Windows용 cp949 우선 시도)
            data = pd.read_csv(file_path, encoding='cp949')
        except:
            data = pd.read_csv(file_path, encoding='utf-8-sig')
        return data
    else:
        st.error(f"'{file_path}' 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
        return None

df = load_data(file_name)

if df is not None:
    # 데이터 미리보기 (접이식 메뉴)
    with st.expander("📂 데이터 미리보기"):
        st.dataframe(df.head())

    # 3. 사이드바 설정
    st.sidebar.header("그래프 설정")
    
    all_columns = df.columns.tolist()
    
    # [수정 사항 1] X, Y축 선택 항목에서 '학생ID'와 '전공' 제외
    excluded_cols = ['학생ID', '전공']
    plot_options = [col for col in all_columns if col not in excluded_cols]
    
    # 선택 상자 구성 (기본값 설정 포함)
    x_axis = st.sidebar.selectbox("X축 선택 (독립 변수)", plot_options, index=0)
    y_axis = st.sidebar.selectbox("Y축 선택 (종속 변수)", plot_options, index=min(1, len(plot_options)-1))
    
    # 색상(범례)은 구분을 위해 모든 컬럼에서 선택 가능하도록 구성
    hue_axis = st.sidebar.selectbox("색상(범례) 선택 (선택 사항)", [None] + all_columns)

    # [수정 사항 2] 추세선 표시 여부 체크박스
    show_trendline = st.sidebar.checkbox("추세선 표시", value=True)

    # 4. 산점도 시각화
    st.subheader(f"📍 {x_axis}와(과) {y_axis}의 관계 (Scatter Plot)")
    
    # Matplotlib의 Unicode 마이너스 기호 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False
    
    try:
        if show_trendline:
            # 추세선 포함 (regplot 또는 lmplot)
            if hue_axis:
                # 범례가 있는 경우 lmplot (그룹별 추세선)
                g = sns.lmplot(data=df, x=x_axis, y=y_axis, hue=hue_axis, height=6, aspect=1.5)
                plt.title(f"{x_axis}와(과) {y_axis}의 관계 (Scatter Plot)")
                st.pyplot(g.fig)
            else:
                # 범례가 없는 경우 regplot (단일 추세선)
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.regplot(data=df, x=x_axis, y=y_axis, ax=ax, 
                            scatter_kws={'alpha':0.6, 's':80}, 
                            line_kws={'color':'red', 'lw':2})
                ax.set_title(f"{x_axis}와(과) {y_axis}의 관계 (Scatter Plot)")
                st.pyplot(fig)
        else:
            # 추세선 없이 단순 산점도 (scatterplot)
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.scatterplot(data=df, x=x_axis, y=y_axis, hue=hue_axis, ax=ax, s=100, alpha=0.8)
            ax.set_title(f"{x_axis}와(과) {y_axis}의 관계 (Scatter Plot)")
            st.pyplot(fig)
            
    except Exception as e:
        st.error(f"그래프 생성 중 오류가 발생했습니다: {e}")

    # 5. 상관분석 결과 요약
    if df[x_axis].dtype in ['int64', 'float64'] and df[y_axis].dtype in ['int64', 'float64']:
        correlation = df[x_axis].corr(df[y_axis])
        st.divider()
        st.info(f"💡 **분석 결과:** {x_axis}와(과) {y_axis}의 상관계수는 **{correlation:.2f}**입니다.")
    else:
        st.warning("선택한 변수가 수치형 데이터가 아니어서 상관계수를 계산할 수 없습니다.")

else:
    st.info("CSV 파일을 업로드하거나 파일명을 확인해 주세요.")
