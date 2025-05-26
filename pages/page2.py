import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# ✅ NanumGothic 폰트 불러오기 (.ttf 파일은 프로젝트 루트에 있어야 함)
font_path = "./fonts/Dongle-Bold.ttf"
font_prop = fm.FontProperties(fname=font_path)

st.set_page_config(page_title="학생 성적 분석 대시보드", layout="wide")
st.title("📊 학생 성적 및 출결 분석 대시보드")

# 파일 업로드
uploaded_file = st.file_uploader("학생 데이터 CSV 업로드", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # 평균 점수 추가
    df["평균점수"] = df[["수학", "영어", "과학"]].mean(axis=1)

    # 미리보기
    st.subheader("📄 데이터 미리보기")
    st.dataframe(df)

    # 요약 통계
    st.subheader("📈 요약 통계")
    st.write(df.describe())

    # 필터링
    st.subheader("🔍 조건 필터링")
    col1, col2 = st.columns(2)
    with col1:
        min_score = st.slider("최소 평균 점수", int(df['평균점수'].min()), int(df['평균점수'].max()), step=1)
    with col2:
        max_absent = st.slider("최대 결석 일수", int(df['결석일수'].min()), int(df['결석일수'].max()), step=1)

    filtered_df = df[(df['평균점수'] >= min_score) & (df['결석일수'] <= max_absent)]
    st.write(f"🔹 조건에 맞는 학생 수: {len(filtered_df)}명")
    st.dataframe(filtered_df)

    # 산점도
    st.subheader("📌 결석일수와 평균점수 간 관계")
    corr = df[['평균점수', '결석일수']].corr().iloc[0, 1]
    st.write(f"상관계수: `{corr:.2f}`")

    fig1, ax1 = plt.subplots()
    sns.scatterplot(data=df, x='결석일수', y='평균점수', ax=ax1)
    ax1.set_title("결석일수 vs 평균점수", fontproperties=font_prop)
    ax1.set_xlabel("결석일수", fontproperties=font_prop)
    ax1.set_ylabel("평균점수", fontproperties=font_prop)
    st.pyplot(fig1)

    # 막대 그래프
    st.subheader("📊 학생별 평균 점수 (막대 그래프)")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    sns.barplot(data=df, x='이름', y='평균점수', ax=ax2)
    ax2.set_title("학생별 평균 점수", fontproperties=font_prop)
    ax2.set_xlabel("이름", fontproperties=font_prop)
    ax2.set_ylabel("평균점수", fontproperties=font_prop)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, fontproperties=font_prop)
    st.pyplot(fig2)

    # 상자 그림
    st.subheader("📦 과목별 점수 분포 (상자 그림)")
    df_melted = df.melt(id_vars=['이름'], value_vars=['수학', '영어', '과학'],
                        var_name='과목', value_name='점수')
    fig3, ax3 = plt.subplots()
    sns.boxplot(data=df_melted, x='과목', y='점수', ax=ax3)
    ax3.set_title("과목별 점수 분포", fontproperties=font_prop)
    ax3.set_xlabel("과목", fontproperties=font_prop)
    ax3.set_ylabel("점수", fontproperties=font_prop)
    st.pyplot(fig3)

else:
    st.info("좌측에서 학생 데이터를 포함한 CSV 파일을 업로드하세요.")
