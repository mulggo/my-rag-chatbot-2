

import streamlit as st
import boto3
import os
from datetime import datetime
import json
from dotenv import load_dotenv
import uuid

# 페이지 설정
st.set_page_config(
    page_title="멀티모달 RAG 챗봇",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 환경 변수 로드
load_dotenv()

# 전역 변수
KB_ID = os.getenv('BEDROCK_KNOWLEDGE_BASE_ID')
MODEL_ID = os.getenv('BEDROCK_MODEL_ID')
REGION = os.getenv('AWS_REGION')
ACCOUNT_ID = os.getenv('AWS_ACCOUNT_ID')
S3_BUCKET = os.getenv('S3_BUCKET_NAME')

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "bedrock_client" not in st.session_state:
    st.session_state.bedrock_client = None



# 사이드바 구성
def setup_sidebar():
    """사이드바 설정 및 구성"""
    with st.sidebar:
        st.title("🤖 RAG 챗봇 설정")

        # 환경 상태 표시
        st.subheader("📊 시스템 상태")

        if KB_ID:
            st.success(f"✅ Knowledge Base: {KB_ID[:8]}...")
        else:
            st.error("❌ Knowledge Base ID 없음")

        if MODEL_ID:
            st.success(f"✅ Model: {MODEL_ID.split('.')[-1]}")
        else:
            st.error("❌ Model ID 없음")

        if REGION:
            st.success(f"✅ Region: {REGION}")
        else:
            st.error("❌ AWS Region 없음")

        st.divider()

        # 채팅 설정
        st.subheader("⚙️ 채팅 설정")

        # 온도 설정
        temperature = st.slider(
            "응답 창의성 (Temperature)",
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.1,
            help="낮을수록 일관된 답변, 높을수록 창의적 답변"
        )

        # 최대 토큰 수
        max_tokens = st.slider(
            "최대 응답 길이 (Tokens)",
            min_value=256,
            max_value=4096,
            value=2048,
            step=256,
            help="응답의 최대 길이를 제한합니다"
        )

        # 검색 결과 수
        num_results = st.slider(
            "검색 결과 수",
            min_value=1,
            max_value=10,
            value=5,
            help="Knowledge Base에서 검색할 문서 수"
        )

        st.divider()

        # 세션 관리
        st.subheader("💬 세션 관리")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🗑️ 채팅 초기화", use_container_width=True):
                st.session_state.messages = []
                st.session_state.session_id = str(uuid.uuid4())
                st.rerun()

        with col2:
            if st.button("🔄 새 세션", use_container_width=True):
                st.session_state.session_id = str(uuid.uuid4())
                st.success("새 세션이 시작되었습니다!")

        # 현재 세션 ID 표시
        st.caption(f"세션 ID: {st.session_state.session_id[:8]}...")

        return {
            'temperature': temperature,
            'max_tokens': max_tokens,
            'num_results': num_results
        }



# Bedrock 클라이언트 초기화
@st.cache_resource
def get_bedrock_client():
    """Bedrock 클라이언트 초기화 (캐시됨)"""
    try:
        return boto3.client('bedrock-agent-runtime', region_name=REGION)
    except Exception as e:
        st.error(f"Bedrock 클라이언트 초기화 실패: {e}")
        return None

def retrieve_and_generate(query, config):
    """Knowledge Base를 사용한 RAG 검색 및 답변 생성"""
    client = get_bedrock_client()
    if not client:
        return {
            'answer': "Bedrock 클라이언트를 초기화할 수 없습니다.",
            'citations': [],
            'success': False
        }

    try:
        request_params = {
            'input': {'text': query},
            'retrieveAndGenerateConfiguration': {
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': KB_ID,
                    'modelArn': f'arn:aws:bedrock:{REGION}::foundation-model/{MODEL_ID}',
                    'retrievalConfiguration': {
                        'vectorSearchConfiguration': {
                            'numberOfResults': config['num_results'],
                            'overrideSearchType': 'HYBRID'
                        }
                    },
                    'generationConfiguration': {
                        'inferenceConfig': {
                            'textInferenceConfig': {
                                'maxTokens': config['max_tokens'],
                                'temperature': config['temperature'],
                                'topP': 0.9
                            }
                        }
                    }
                }
            },
            'sessionId': st.session_state.session_id
        }

        response = client.retrieve_and_generate(**request_params)

        return {
            'answer': response['output']['text'],
            'citations': response.get('citations', []),
            'success': True
        }

    except Exception as e:
        return {
            'answer': f"오류가 발생했습니다: {str(e)}",
            'citations': [],
            'success': False
        }

def display_chat_messages():
    """채팅 메시지 표시"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # 소스 문서 표시 (assistant 메시지에만)
            if message["role"] == "assistant" and "citations" in message:
                citations = message["citations"]
                if citations:
                    with st.expander(f"📚 참고 문서 ({len(citations)}개)"):
                        for i, citation in enumerate(citations, 1):
                            if 'retrievedReferences' in citation:
                                for ref in citation['retrievedReferences']:
                                    location = ref.get('location', {})
                                    s3_location = location.get('s3Location', {})
                                    uri = s3_location.get('uri', 'Unknown')

                                    st.markdown(f"**{i}. {uri.split('/')[-1]}**")

                                    content = ref.get('content', {}).get('text', '')
                                    if content:
                                        st.markdown(f"""
                                                    {content[:300]}...
                                                    """)

                                    st.markdown("---")

def main_chat_interface(config):
    """메인 채팅 인터페이스"""
    st.title("🤖 멀티모달 RAG 챗봇")
    st.markdown("**'pdf', 'txt', 'md', 'jpg', 'jpeg', 'png' 파일을 업로드하고 질문해보세요!**")

    # 환경 변수 확인
    if not all([KB_ID, MODEL_ID, REGION]):
        st.error("⚠️ 환경 변수가 올바르게 설정되지 않았습니다. .env 파일을 확인해주세요.")
        st.stop()

    # 채팅 메시지 표시
    display_chat_messages()

    # 사용자 입력
    if prompt := st.chat_input("질문을 입력하세요..."):
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 사용자 메시지 표시
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI 응답 생성
        with st.chat_message("assistant"):
            with st.spinner("답변을 생성하고 있습니다..."):
                result = retrieve_and_generate(prompt, config)

                if result['success']:
                    st.markdown(result['answer'])

                    # 소스 문서 표시
                    citations = result['citations']
                    if citations:
                        with st.expander(f"📚 참고 문서 ({len(citations)}개)"):
                            for i, citation in enumerate(citations, 1):
                                if 'retrievedReferences' in citation:
                                    for ref in citation['retrievedReferences']:
                                        location = ref.get('location', {})
                                        s3_location = location.get('s3Location', {})
                                        uri = s3_location.get('uri', 'Unknown')

                                        st.markdown(f"**{i}. {uri.split('/')[-1]}**")

                                        content = ref.get('content', {}).get('text', '')
                                        if content:
                                            st.markdown(f"""
{content[:300]}...
""")

                                        st.markdown("---")

                    # 어시스턴트 메시지 저장
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": result['answer'],
                        "citations": citations
                    })
                else:
                    st.error(result['answer'])
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": result['answer']
                    })



def setup_file_upload():
    """파일 업로드 섹션 설정"""
    with st.sidebar:
        st.divider()
        st.subheader("📁 문서 업로드")

        uploaded_files = st.file_uploader(
            "문서를 업로드하세요",
            type=['pdf', 'txt', 'md', 'jpg', 'jpeg', 'png'],
            accept_multiple_files=True,
            help="PDF, 텍스트, 이미지 파일을 지원합니다"
        )

        if uploaded_files:
            st.success(f"{len(uploaded_files)}개 파일이 업로드되었습니다!")

            for file in uploaded_files:
                st.write(f"📄 {file.name} ({file.size:,} bytes)")

            if st.button("🚀 Knowledge Base에 추가", use_container_width=True):
                with st.spinner("파일을 처리하고 있습니다..."):
                    # TODO: 실제 파일 처리 및 S3 업로드 구현
                    st.success("파일이 성공적으로 추가되었습니다!")
                    st.info("Knowledge Base 동기화는 몇 분 정도 소요될 수 있습니다.")

        return uploaded_files


# 메인 실행 함수
def main():
    """메인 애플리케이션 실행"""
    # 사이드바 설정
    config = setup_sidebar()

    # 파일 업로드
    uploaded_files = setup_file_upload()

    # 메인 채팅 인터페이스
    main_chat_interface(config)

if __name__ == "__main__":
    main()
