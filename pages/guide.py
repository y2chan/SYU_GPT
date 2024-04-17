import streamlit as st

st.set_page_config(
    page_title="사용 가이드",
    # page_icon="😃",
    page_icon="photo/Logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
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
st.sidebar.page_link("main.py", label="Home", help="홈 화면으로 이동합니다", icon="🏠")
st.sidebar.page_link("pages/greeting.py", label="Greeting", icon="✋")
st.sidebar.page_link("pages/guide.py", label="User's Guide", icon="❓")
st.sidebar.subheader("Other Web")
st.sidebar.page_link("https://www.syu.ac.kr/", label="Sahmyook University", help="삼육대학교 공식 사이트로 이동합니다")
st.sidebar.page_link("https://chat.openai.com/", label="ChatGPT", help="Chat GPT 사이트로 이동합니다")
st.sidebar.page_link("https://gabean.kr/", label="GaBean", help="개발자의 또 다른 웹 사이트로 이동합니다")

st.subheader('SYU-GPT는 이렇게 사용합니다', divider='blue', anchor=False)
st.caption('SYU-GPT가 대답할 수 있는 주제와 그에 대한 설명은 아래와 같습니다.')
st.caption('1. 학과')
st.caption('')
st.caption('2. 등록')
st.caption('')
st.caption('3. 성적')
st.caption('')
st.caption('4. 수강신청')
st.caption('')
st.caption('5. 졸업')
st.caption('')
st.caption('6. 학사일정')
st.caption('')
st.caption('7. 동아리')
st.caption('')
st.caption('8. 장학금')
st.caption('')
st.caption('9. 증명서')
st.caption('')
st.caption('10. 교통')
st.caption('')
st.caption('11. 셔틀버스')
st.caption('')
st.caption('12. 학교 건물')
st.caption('')
st.caption('13. 시설 정보')
st.caption('')
st.caption('14. 후문 정보')
st.caption('')
st.caption('15. 도서관')
st.caption('')
st.caption('16. 업무별 전화번호')
st.caption('')
st.caption('17. 관련 링크')
st.caption('')
st.caption('삼육대학교에 대해 궁금한 점이 생기면 언제든 와서 질문해주세요!')
st.caption('')
st.caption(' ')
st.caption(' ')
st.caption(' ')