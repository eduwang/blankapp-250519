import streamlit as st
import openai

# 🔑 OpenAI API 키 불러오기
openai.api_key = st.secrets["openai"]["openai_api_key"]

# 🔁 대화 히스토리 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "당신은 친절하고 똑똑한 AI 비서입니다."}
    ]

st.title("💬 GPT 챗봇 (멀티턴)")

# ✅ 사용자 입력 받기
user_input = st.text_input("질문을 입력하세요", key="user_input")

# ✅ 메시지 처리
if user_input:
    # 사용자 메시지 저장
    st.session_state.messages.append({"role": "user", "content": user_input})

    # GPT 응답 생성
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # 또는 gpt-3.5-turbo
        messages=st.session_state.messages
    )

    bot_reply = response.choices[0].message.content

    # GPT 메시지 저장
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# ✅ 대화 출력
for msg in st.session_state.messages[1:]:  # system 메시지는 제외
    role = "👤 사용자" if msg["role"] == "user" else "🤖 GPT"
    st.markdown(f"**{role}:** {msg['content']}")
