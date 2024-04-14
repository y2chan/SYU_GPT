import os
import streamlit as st
from langchain import hub
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader, DirectoryLoader

# 환경 설정
def setup_environment():
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    os.environ["LANGCHAIN_API_KEY"] = "ls__202a1d46885b4cd085668e62959bd3fd"
    os.environ["LANGCHAIN_PROJECT"] = "SYU-GPT"
    os.environ["OPENAI_API_KEY"] = "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"
    os.environ["SERPER_API_KEY"] = "c8e06b2f9d85e759d3cbfecb409fdabfbff52780"

# 문서 처리 준비
def prepare_documents():
    if "retriever" not in st.session_state:
        # loader = TextLoader("data/SYU_GPT data.txt")
        loader = DirectoryLoader(".", glob="data/SYU_GPT/*.txt", show_progress=True)
        docs = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=5000, chunk_overlap=0, separator="\n")
        splits = text_splitter.split_documents(docs)
        vectorstore = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())
        st.session_state.retriever = vectorstore.as_retriever()

# 응답 생성
def generate_response(user_input):
    try:
        prompt = hub.pull("rlm/rag-prompt")
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        rag_chain = (
                {"context": st.session_state.retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
        )
        return rag_chain.invoke(user_input)
    except Exception as e:
        # 로그 또는 사용자 인터페이스에 보다 상세한 오류 메시지 출력
        st.error(f"API request failed: {str(e)}")
        return None


# 예외 처리를 강화하여 API 권한 문제에 대해 좀 더 상세한 정보를 제공
def main():
    setup_environment()
    try:
        prepare_documents()
        # 기타 코드 구현
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

    st.set_page_config(page_title="SYU-GPT", layout="wide", initial_sidebar_state="expanded", menu_items={'Get Help': 'https://www.extremelycoolapp.com/help', 'Report a bug': "https://www.extremelycoolapp.com/bug",})
    st.title('SYU-GPT', anchor=False)

    # 먼저, subheader와 caption을 포함하는 부분을 st.empty()를 사용하여 빈 홀더로 만듭니다.
    info_placeholder = st.empty()

    # 이제 info_placeholder를 사용하여 subheader와 caption을 표시합니다.
    with info_placeholder.container():
        st.subheader('삼육대학교 검색 엔진', anchor=False)
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
    st.sidebar.page_link("main.py", label="홈", help="홈 화면으로 이동합니다")
    st.sidebar.page_link("pages/greeting.py", label="인사말")
    st.sidebar.page_link("pages/guide.py", label="사용 가이드")
    st.sidebar.subheader("Other Web")
    st.sidebar.page_link("https://chat.openai.com/", label="ChatGPT", help="Chat GPT 사이트로 이동합니다")
    st.sidebar.page_link("https://gabean.kr/", label="GaBean", help="개발자의 또 다른 웹 사이트로 이동합니다")

    if "chat_session" not in st.session_state:
        st.session_state.messages = []

    if user_input := st.chat_input("질문을 입력하세요."):
        info_placeholder.empty()
        try:
            with st.spinner("답변을 생성하는 중입니다..."):
                response = generate_response(user_input)

            with st.chat_message("user", avatar="🧃"):
                st.markdown(user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("SYU-GPT", avatar="photo/Logo.png"):
                st.markdown(response)
            st.session_state.messages.append({"role": "SYU-GPT", "content": response})
        except Exception as e:
            st.error("에러가 발생했습니다: {}".format(e))

if __name__ == "__main__":
    main()
