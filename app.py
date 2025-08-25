import streamlit as st
import boto3
import os
import time
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

# 전역 변수 (노트북 3번 참고)
KB_ID = os.getenv('BEDROCK_KNOWLEDGE_BASE_ID')
MODEL_ID = os.getenv('BEDROCK_MODEL_ID')
RERANK_MODEL_ID = os.getenv('BEDROCK_RERANK_MODEL_ID')
REGION = os.getenv('AWS_REGION')
S3_BUCKET = os.getenv('S3_BUCKET_NAME')

# 청크 설정 (test_chunk와 동일)
SOURCE_CHUNKS = 50  # 초기 검색 청크 수
RERANK_CHUNKS = 5   # 최종 선택 청크 수

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# AWS 계정 ID 가져오기 (동적)
@st.cache_data
def get_account_id():
    try:
        sts_client = boto3.client('sts', region_name=REGION)
        return sts_client.get_caller_identity()['Account']
    except Exception as e:
        st.error(f"AWS 계정 ID 조회 실패: {e}")
        return None

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

    # 계정 ID 가져오기
    account_id = get_account_id()
    if not account_id:
        return {
            'answer': "AWS 계정 ID를 가져올 수 없습니다.",
            'citations': [],
            'success': False
        }

    try:
        # 환경 변수 및 ARN 디버깅
        print(f"🔧 [DEBUG] 환경 변수 및 ARN 생성:")
        print(f"   MODEL_ID 원본: '{MODEL_ID}'")
        print(f"   MODEL_ID 길이: {len(MODEL_ID)}")
        print(f"   REGION: '{REGION}'")
        print(f"   Account ID: {account_id}")
        
        # MODEL_ID에서 중복된 'us.' 제거 (만약 있다면)
        clean_model_id = MODEL_ID
        if MODEL_ID.count('us.') > 1:  # 'us.'가 2번 이상 나타나면
            # 첫 번째 'us.' 제거
            clean_model_id = MODEL_ID.replace('us.', '', 1)
            print(f"⚠️ 중복된 'us.' 제거: {MODEL_ID} → {clean_model_id}")
        
        # ARN 생성 - clean_model_id 사용
        model_arn = f'arn:aws:bedrock:{REGION}:{account_id}:inference-profile/{clean_model_id}'
        rerank_arn = f'arn:aws:bedrock:{REGION}::foundation-model/{RERANK_MODEL_ID}'
        
        print(f"🤖 최종 Model ARN: {model_arn}")
        print(f"🔄 Rerank ARN: {rerank_arn}")
        
        # AWS 문서 확인: us.anthropic.claude-3-7-sonnet-20250219-v1:0 이 올바른 형식
        expected_model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
        if clean_model_id != expected_model_id:
            print(f"⚠️ 모델 ID 불일치:")
            print(f"   현재: {clean_model_id}")
            print(f"   예상: {expected_model_id}")
        
        request_params = {
            'input': {'text': query},
            'retrieveAndGenerateConfiguration': {
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': KB_ID,
                    'modelArn': model_arn,
                    'retrievalConfiguration': {
                        'vectorSearchConfiguration': {
                            'numberOfResults': SOURCE_CHUNKS,  # 50개 청크
                            'overrideSearchType': 'HYBRID',
                            'rerankingConfiguration': {
                                'type': 'BEDROCK_RERANKING_MODEL',
                                'bedrockRerankingConfiguration': {
                                    'modelConfiguration': {
                                        'modelArn': rerank_arn
                                    },
                                    'numberOfRerankedResults': RERANK_CHUNKS  # 5개로 축소
                                }
                            }
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
            }
        }

        # 세션 ID 관리
        if 'bedrock_session_id' in st.session_state:
            request_params['sessionId'] = st.session_state.bedrock_session_id

        response = client.retrieve_and_generate(**request_params)

        # 세션 ID 저장
        if 'sessionId' in response:
            st.session_state.bedrock_session_id = response['sessionId']

        # 실제 사용된 청크 수 확인
        actual_chunks_used = len(response.get('citations', []))
        actual_references_count = 0
        if 'citations' in response:
            for citation in response['citations']:
                if 'retrievedReferences' in citation:
                    actual_references_count += len(citation['retrievedReferences'])
        
        print(f"📊 [VERIFICATION] 실제 KB 응답 분석:")
        print(f"   요청한 초기 청크: {SOURCE_CHUNKS}개")
        print(f"   요청한 최종 청크: {RERANK_CHUNKS}개") 
        print(f"   실제 반환된 citations: {actual_chunks_used}개")
        print(f"   실제 반환된 references: {actual_references_count}개")

        return {
            'answer': response['output']['text'],
            'citations': response.get('citations', []),
            'success': True,
            'actual_chunks_used': actual_chunks_used,
            'actual_references_count': actual_references_count
        }

    except Exception as e:
        error_message = str(e)
        print(f"❌ 오류 발생: {error_message}")
        
        # 세션 관련 오류 처리
        if "Session with Id" in error_message and "is not valid" in error_message:
            if 'bedrock_session_id' in st.session_state:
                del st.session_state.bedrock_session_id
            
            try:
                if 'sessionId' in request_params:
                    del request_params['sessionId']
                
                response = client.retrieve_and_generate(**request_params)
                
                if 'sessionId' in response:
                    st.session_state.bedrock_session_id = response['sessionId']
                
                st.info("🔄 채팅 세션이 갱신되었습니다.")
                
                return {
                    'answer': response['output']['text'],
                    'citations': response.get('citations', []),
                    'success': True
                }
                
            except Exception as retry_error:
                return {
                    'answer': f"세션 갱신 후에도 오류가 발생했습니다: {str(retry_error)}",
                    'citations': [],
                    'success': False
                }
        
        return {
            'answer': f"오류가 발생했습니다: {error_message}",
            'citations': [],
            'success': False
        }

def setup_sidebar():
    """사이드바 설정"""
    with st.sidebar:
        st.title("🤖 RAG 챗봇 설정")

        # 환경 상태 표시
        st.subheader("📊 시스템 상태")
        
        account_id = get_account_id()

        if KB_ID:
            st.success(f"✅ Knowledge Base: {KB_ID}")
        else:
            st.error("❌ Knowledge Base ID 없음")

        if MODEL_ID:
            st.success(f"✅ Model: {MODEL_ID}")
        else:
            st.error("❌ Model ID 없음")

        if RERANK_MODEL_ID:
            st.success(f"✅ Rerank: {RERANK_MODEL_ID}")
        else:
            st.error("❌ Rerank Model ID 없음")

        if REGION:
            st.success(f"✅ Region: {REGION}")
        else:
            st.error("❌ AWS Region 없음")
            
        if account_id:
            st.success(f"✅ Account: {account_id}")
        else:
            st.error("❌ AWS Account ID 없음")

        st.divider()

        # 청크 설정 표시 (고정값)
        st.subheader("🔍 검색 설정")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📄 초기 검색 청크", f"{SOURCE_CHUNKS}개")
        with col2:
            st.metric("🎯 최종 선별 청크", f"{RERANK_CHUNKS}개")
        
        st.info("💡 test_chunk와 동일한 설정: 50개 초기 검색 → 5개 최종 선별")
        
        st.divider()

        # 응답 생성 설정
        st.subheader("⚙️ 응답 생성 설정")

        temperature = st.slider(
            "🌡️ 응답 창의성 (Temperature)",
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.1,
            help="낮을수록 일관된 답변, 높을수록 창의적 답변"
        )

        max_tokens = st.slider(
            "📝 최대 응답 길이 (Tokens)",
            min_value=256,
            max_value=4096,
            value=2048,
            step=256,
            help="응답의 최대 길이를 제한합니다"
        )

        st.divider()

        # 세션 관리
        st.subheader("💬 세션 관리")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🗑️ 채팅 초기화", use_container_width=True):
                st.session_state.messages = []
                st.session_state.session_id = str(uuid.uuid4())
                if 'bedrock_session_id' in st.session_state:
                    del st.session_state.bedrock_session_id
                st.rerun()

        with col2:
            if st.button("🔄 새 세션", use_container_width=True):
                st.session_state.session_id = str(uuid.uuid4())
                if 'bedrock_session_id' in st.session_state:
                    del st.session_state.bedrock_session_id
                st.success("새 세션이 시작되었습니다!")

        # 현재 세션 ID 표시
        st.caption(f"Streamlit 세션: {st.session_state.session_id[:8]}...")
        if 'bedrock_session_id' in st.session_state:
            st.caption(f"Bedrock 세션: {st.session_state.bedrock_session_id[:8]}...")
        else:
            st.caption("Bedrock 세션: 없음 (첫 질문 시 생성)")

        return {
            'temperature': temperature,
            'max_tokens': max_tokens
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
                                        st.markdown(f"{content[:300]}...")

                                    st.markdown("---")

def main_chat_interface(config):
    """메인 채팅 인터페이스"""
    st.title("🤖 멀티모달 RAG 챗봇")
    st.markdown("**건설공사 표준품셈 문서 기반 RAG 챗봇**")
    st.markdown("**Rerank 기반 고품질 답변 제공** | Claude 3.7 Sonnet + Cohere Rerank v3-5")

    # 실제 설정값 표시
    with st.container():
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📄 초기 검색 청크", f"{SOURCE_CHUNKS}개")
        
        with col2:
            st.metric("🎯 최종 선별 청크", f"{RERANK_CHUNKS}개")
        
        with col3:
            st.metric("🔎 검색 타입", "HYBRID")
        
        with col4:
            st.metric("🌡️ Temperature", f"{config['temperature']:.1f}")
        
        st.markdown("---")

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
                                            st.markdown(f"{content[:300]}...")

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

# 메인 실행 함수
def main():
    """메인 애플리케이션 실행"""
    # 사이드바 설정
    config = setup_sidebar()

    # 메인 채팅 인터페이스
    main_chat_interface(config)

if __name__ == "__main__":
    main()
