import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# 환경 변수 로드
load_dotenv(find_dotenv())

# OpenAI 클라이언트 초기화
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# 메시지를 처리하고 응답을 반환하는 함수
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    chat_completion = openai_client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=temperature,
    )
    return chat_completion.choices[0].message.content

# 대화 내용을 화면에 출력하는 함수
def display_conversation():
    for role, text in st.session_state['conversation']:
        if role == "user":
            with st.chat_message(role, avatar="🧃"):
                st.markdown(text)
        else:
            with st.chat_message(role, avatar="🤖"):
                st.markdown(text)


# Streamlit 앱
def run_app():

    st.set_page_config(
        page_title="SYU-GPT",
        page_icon="photo/Logo.png",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
        }
    )

    #제목
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
    st.sidebar.page_link("testmain2.py", label="홈", help="홈 화면으로 이동합니다")
    st.sidebar.page_link("pages/greeting.py", label="인사말")
    st.sidebar.page_link("pages/guide.py", label="사용 가이드")
    st.sidebar.subheader("Other Web")
    st.sidebar.page_link("https://chat.openai.com/", label="ChatGPT", help="Chat GPT 웹 사이트로 이동합니다")
    st.sidebar.page_link("https://gabean.kr/", label="GaBean", help="개발자의 또 다른 웹 사이트로 이동합니다")


    if "chat_session" not in st.session_state:
        st.session_state["conversation"] = [] # 대화 이력을 저장할 리스트 초기화


    # 사용자 입력 처리
    if user_input := st.chat_input("질문을 입력하세요."):
        # 사용자가 입력을 시작하면, info_placeholder를 삭제하거나 숨깁니다.
        info_placeholder.empty()  # 이제 subheader와 caption이 사라집니다.

        if 'context' not in st.session_state:
            st.session_state['context'] = [{'role': 'system', 'content': """
        You are SYU-GPT, an automated chatbot designed to answer questions about 삼육대학교. \
        You provide information on various topics including departments, scholarships, \
        registrations, grades, graduation, course enrollment, shuttle buses, transportation, facility information, \
        academic schedules, academic notice, library services, campus buildings, certification documents, and the rear gate. \
        The database is organized with detailed information under each category. \
        Your responses should be accurate, informative, and delivered in a friendly conversational style. \
        Please ensure the information provided is up to date and relevant to the user's query. \
        """}]



        # 사용자의 메시지 추가
        st.session_state['context'].append({'role': 'user', 'content': user_input})

        with st.spinner("질문을 처리하는 중입니다..."):
            # OpenAI로부터 응답 받기
            response = get_completion_from_messages(st.session_state['context']) # 적절한 'messages' 인자를 전달

        # 대화에 추가
        st.session_state['context'].append({'role': 'assistant', 'content': response})
        st.session_state['conversation'].append(('user', user_input))
        st.session_state['conversation'].append(('SYU-GPT', response))

        # 대화 내용을 화면에 출력
        display_conversation()

        # 입력 필드 초기화
        st.session_state['user_input'] = ""

        st.caption(" ")
        st.caption(" ")
        st.page_link("testmain2.py", label="처음으로 돌아가기", help="처음 화면으로 이동합니다")

# 앱 실행
run_app()