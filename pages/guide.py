import streamlit as st

if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1

st.set_page_config(
    page_title="사용 가이드",
    # page_icon="😃",
    page_icon="photo/Logo.png",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
    }
)

# 사이드바
st.sidebar.image("photo/syugptLogo.png")
hide_img_fs = '''
    <style>
    button[title="View fullscreen"]{
        visibility: hidden;}
    </style>
    '''
st.sidebar.markdown(hide_img_fs, unsafe_allow_html=True)

st.sidebar.write('-' * 50)
st.sidebar.subheader("Menu")
st.sidebar.page_link("main.py", label="홈", help="홈 화면으로 이동합니다")
st.sidebar.page_link("pages/greeting.py", label="인사말")
st.sidebar.page_link("pages/guide.py", label="사용 가이드")
st.sidebar.subheader("Other Web")
st.sidebar.page_link("https://chat.openai.com/", label="ChatGPT", help="Chat GPT 사이트로 이동합니다")
st.sidebar.page_link("https://gabean.kr/", label="GaBean", help="개발자의 또 다른 웹 사이트로 이동합니다")

st.subheader('SYU-GPT는 이렇게 사용합니다', divider='blue')