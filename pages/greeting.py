import streamlit as st

if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1

st.set_page_config(
    page_title="인사말",
    page_icon="😃",
    #page_icon="photo/Logo.png",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
    }
)

# 사이드바
st.sidebar.title("목록")
st.sidebar.write('-' * 50)
st.sidebar.page_link("main.py", label="홈", help="홈 화면으로 이동합니다")
st.sidebar.page_link("pages/greeting.py", label="인사말")
st.sidebar.page_link("pages/guide.py", label="사용 가이드")

st.subheader(':) 안녕하세요! 삼육대학교 전용 인공지능 SYU-GPT 입니다. 👋', divider='blue')
st.caption('여기서는 삼육대학교의 다양한 정보들을 질문할 수 있습니다.')
st.caption('모든 질문에 항상 완벽하게 답하는 것은 아니나, 학습된 정보 내에서 최선의 답변을 생성합니다.')
st.caption('삼육대학교에 대해 궁금한 점이 생기면 언제든 와서 질문해주세요!')
st.caption('SYU-GPT는 항상 여러분을 기다리고 있습니다 😉')
st.caption(' ')
st.caption(' ')
st.caption(' ')
st.caption('마지막 업데이트 : 2024년 3월 22일')