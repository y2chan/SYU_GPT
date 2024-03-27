import google.generativeai as genai
import streamlit as st

st.set_page_config(
    page_title="SYU-GPT",
    page_icon="😃",
    #page_icon="photo/Logo.png",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
    }
)

#st.image("photo/image.png")
st.title('SYU-GPT', anchor=False)

# 먼저, subheader와 caption을 포함하는 부분을 st.empty()를 사용하여 빈 홀더로 만듭니다.
info_placeholder = st.empty()

# 이제 info_placeholder를 사용하여 subheader와 caption을 표시합니다.
with info_placeholder.container():
    st.subheader('삼육대학교 검색 엔진')
    st.caption('여러분이 검색하고 싶은 학교 정보를 검색하세요!')
    st.caption('매일 데이터를 업데이트 중입니다.')
    st.caption('삼육대학교 재학생이라면 사용해보세요! 😊')
    st.caption(' ')

# 사이드바
st.sidebar.title("목록")
st.sidebar.write('-' * 50)
st.sidebar.page_link("testmain.py", label="홈", help="홈 화면으로 이동합니다")
st.sidebar.page_link("pages/greeting.py", label="인사말")
st.sidebar.page_link("pages/guide.py", label="사용 가이드")

@st.cache_resource
def load_model():
    model = genai.GenerativeModel('gemini-pro')
    print("model loaded...")
    return model

model = load_model()

if "chat_session" not in st.session_state:
    st.session_state["chat_session"] = model.start_chat(history=[])

for content in st.session_state.chat_session.history:
    with st.chat_message("ai", avatar="🤖" if content.role == "model" else "🧃"):
        st.markdown(content.parts[0].text)

if prompt := st.chat_input("질문을 입력하세요."):
    # 사용자가 입력을 시작하면, info_placeholder를 삭제하거나 숨깁니다.
    info_placeholder.empty()  # 이제 subheader와 caption이 사라집니다.

    # 채팅 메시지 처리 로직
    with st.chat_message("user", avatar="🧃"):
        st.markdown(prompt)
    with st.chat_message("ai", avatar="🤖"):
        message_placeholder = st.empty() # DeltaGenerator 반환
        full_response = ""
        with st.spinner("질문을 처리하는 중입니다..."):
            response = st.session_state.chat_session.send_message(prompt, stream=True)
            for chunk in response:
                full_response += chunk.text
                message_placeholder.markdown(full_response)