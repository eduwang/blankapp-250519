import streamlit as st
import pandas as pd
import datetime
import calendar

st.set_page_config(page_title="출석부", layout="wide")

# 1. 가상의 학생 이름 25명 생성
students = [f"학생{i+1}" for i in range(25)]

# 2. 현재 연도 기준, 월 선택
year = datetime.date.today().year
month = st.selectbox("출석을 기록할 월을 선택하세요", list(range(1, 13)), index=datetime.date.today().month - 1)

# 3. 평일만 추출한 날짜 리스트 만들기
_, num_days = calendar.monthrange(year, month)
dates = [
    datetime.date(year, month, day)
    for day in range(1, num_days + 1)
    if datetime.date(year, month, day).weekday() < 5
]
date_strs = [date.strftime("%m/%d") for date in dates]

# 4. 출석부 데이터 초기화
if "attendance" not in st.session_state or st.session_state.selected_month != month:
    st.session_state.attendance = pd.DataFrame(False, index=students, columns=date_strs)
    st.session_state.selected_month = month

st.title("📘 학생 출석부")

# 5. 출석부 표 형태로 출력 (학생: 행, 날짜: 열)
edited_df = st.data_editor(
    st.session_state.attendance.astype(int),
    num_rows="fixed",
    use_container_width=True,
    key="attendance_editor"
)

# 6. 업데이트 반영
# (True/False로 변환하여 session_state에 저장)
st.session_state.attendance = edited_df.astype(bool)

# 7. 다운로드 버튼
st.download_button(
    label="📥 출석부 CSV 다운로드",
    data=st.session_state.attendance.astype(int).to_csv().encode("utf-8-sig"),
    file_name=f"{year}_{month}_출석부.csv",
    mime="text/csv"
)
