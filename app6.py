import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# 1. 페이지 설정
st.set_page_config(page_title="산점도 활용하기 프로그램", layout="wide")
st.title("📊 산점도 활용하기 프로그램")

# 2. 데이터 불러오기
file_name = '6주차_실습4.csv'


@st.cache_data
def load_data(file_path):
    if os.path.exists(file_path):
        try:
            data = pd.read_csv(file_path, encoding='cp949')
        except:
            data = pd.read_csv(file_path, encoding='utf-8-sig')
        return data
    else:
        st.error(f"'{file_path}' 파일을 찾을 수 없습니다.")
        return None


df = load_data(file_name)

if df is not None:
    # 3. 사이드바 - 변수 선택 및 옵션 설정
    st.sidebar.header("그래프 설정")

    all_columns = df.columns.tolist()

    # [수정 사항 1] X, Y축 선택 항목에서 '학생ID'와 '전공' 삭제
    excluded_cols = ['학생ID', '전공']
    plot_options = [col for col in all_columns if col not in excluded_cols]

    x_axis = st.sidebar.selectbox("X축 선택 (독립 변수)", plot_options, index=0)
    y_axis = st.sidebar.selectbox("Y축 선택 (종속 변수)", plot_options, index=min(1, len(plot_options) - 1))

    # 색상(범례)은 데이터 구분을 위해 전체 컬럼에서 선택 가능하도록 유지 (필요시 수정 가능)
    hue_axis = st.sidebar.selectbox("색상(범례) 선택 (선택 사항)", [None] + all_columns)

    # [수정 사항 2] 추세선 표시 여부 체크박스 추가
    show_trendline = st.sidebar.checkbox("추세선 표시", value=True)

    # 한글 폰트 설정 (Windows: Malgun Gothic, Mac: AppleGothic)
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False

    # 4. 그래프 그리기
    st.subheader(f"📍 {x_axis}와(과) {y_axis}의 관계 (Scatter Plot)")

    fig, ax = plt.subplots(figsize=(10, 6))

    try:
        if show_trendline:
            # 추세선을 포함하여 그리기
            if hue_axis:
                # 범례가 있을 경우 lmplot 사용 (FacetGrid 특성상 st.pyplot(g.fig)로 호출)
                g = sns.lmplot(data=df, x=x_axis, y=y_axis, hue=hue_axis, height=6, aspect=1.5)
                plt.title(f"{x_axis}와(과) {y_axis}의 관계 (Scatter Plot)")
                st.pyplot(g.fig)
            else:
                # 범례가 없을 경우 regplot 사용
                sns.regplot(data=df, x=x_axis, y=y_axis, ax=ax, scatter_kws={'alpha': 0.5}, line_kws={'color': 'red'})
                ax.set_title(f"{x_axis}와(과) {y_axis}의 관계 (Scatter Plot)")
                st.pyplot(fig)
        else:
            # 추세선 없이 단순 산점도만 그리기
            sns.scatterplot(data=df, x=x_axis, y=y_axis, hue=hue_axis, ax=ax, s=100, alpha=0.7)
            ax.set_title(f"{x_axis}와(과) {y_axis}의 관계 (Scatter Plot)")
            st.pyplot(fig)

    except Exception as e:
        st.error(f"그래프 생성 중 오류가 발생했습니다: {e}")

    # 5. 상관계수 수치 표시 (수치형 데이터인 경우만)
    if df[x_axis].dtype in ['int64', 'float64'] and df[y_axis].dtype in ['int64', 'float64']:
        corr = df[x_axis].corr(df[y_axis])
        st.info(f"💡 **{x_axis}**와(과) **{y_axis}**의 상관계수: **{corr:.2f}**")

else:
    st.info("데이터 파일을 로드할 수 없습니다. 파일명을 확인해 주세요.")