import streamlit as st
from langchain import hub
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.llms.openai import OpenAI
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain_core.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
import os

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

    # 제목
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
        st.session_state.messages = [] # 대화 이력을 저장할 리스트 초기화

    # 사용자 입력 처리
    if user_input := st.chat_input("질문을 입력하세요."):
        # 사용자가 입력을 시작하면, info_placeholder를 삭제하거나 숨깁니다.
        info_placeholder.empty()  # 이제 subheader와 caption이 사라집니다.

        # 단계 1: 문서 로드(Load Documents)
        # 문서를 로드하고, 청크로 나누고, 인덱싱합니다.

        loader = TextLoader("data/SYU_GPT data.txt")
        # loader = DirectoryLoader(".", glob="data/SYU_GPT/*.txt", show_progress=True)
        # loader = PyPDFLoader("data/SYU_GPT 데이터 문서.pdf")
        docs = loader.load()

        # 단계 2: 문서 분할(Split Documents)
        text_splitter = CharacterTextSplitter(
            chunk_size=5000, chunk_overlap=500, separator="\n"
        )

        splits = text_splitter.split_documents(docs)

        # 단계 3: 임베딩 & 벡터스토어 생성(Create Vectorstore)
        # 벡터스토어를 생성합니다.
        vectorstore = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())

        # 단계 4: 검색(Search)
        # 뉴스에 포함되어 있는 정보를 검색하고 생성합니다.
        retriever = vectorstore.as_retriever()

        # 단계 5: 프롬프트 생성(Create Prompt)
        # 프롬프트를 생성합니다.
        prompt = hub.pull("rlm/rag-prompt")

        # 단계 6: 언어모델 생성(Create LLM)
        # 모델(LLM) 을 생성합니다.
        llm = ChatOpenAI(model_name="gpt-4-turbo-preview", temperature=0)

        def format_docs(docs):
            # 검색한 문서 결과를 하나의 문단으로 합쳐줍니다.
            return "\n\n".join(doc.page_content for doc in docs)

        model = llm

        google_search = GoogleSerperAPIWrapper()
        tools = [
            Tool(
                name="SYU-GPT",
                func=google_search.run,
                description="Chatbot For Sahmyook University",
                verbose=True
            )
        ]

        search_agent = create_react_agent(model, tools, prompt)
        agent_executor = AgentExecutor(
            agent=search_agent,
            tools=tools,
            verbose=True,
            return_intermediate_steps=True,
        )

        # 단계 7: 체인 생성(Create Chain)
        rag_chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
        )

        # 단계 8: 체인 실행(Run Chain)
        # 문서에 대한 질의를 입력하고, 답변을 출력합니다.
        question = user_input

        with st.spinner("답변을 생성하는 중입니다..."):
            response = rag_chain.invoke(question)

        # 대화에 추가
        with st.chat_message("user", avatar="🧃"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("SYU-GPT", avatar="photo/Logo.png"):
            st.markdown(response)
        st.session_state.messages.append({"role": "SYU-GPT", "content": response})

        st.caption(" ")
        st.caption(" ")
        st.page_link("main.py", label="처음으로 돌아가기", help="처음 화면으로 이동합니다")

# 앱 실행
run_app()
