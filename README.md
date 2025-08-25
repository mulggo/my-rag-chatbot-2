# 멀티모달 RAG 챗봇 with AWS Bedrock

AWS Bedrock과 Knowledge Base를 활용한 멀티모달 RAG(Retrieval-Augmented Generation) 챗봇 프로젝트입니다. 텍스트, 이미지, PDF 등 다양한 형태의 문서를 처리하고, Streamlit으로 구현된 웹 UI를 통해 사용자와 상호작용합니다.

## 프로젝트 목표

이 프로젝트는 다음과 같은 목표를 달성하기 위해 설계되었습니다:

1. **멀티모달 문서 처리**: 다양한 형태의 문서(텍스트, 이미지, PDF)를 하나의 시스템에서 처리
2. **효율적인 검색**: AWS Bedrock Knowledge Base를 활용한 의미 기반 문서 검색
3. **고품질 응답 생성**: Foundation Model을 활용한 정확하고 맥락적인 답변 제공
4. **사용자 친화적 인터페이스**: 직관적이고 반응형 웹 UI 제공

## 핵심 기능

### 🔍 문서 처리 및 검색
- 텍스트 파일 (.txt, .md) 처리
- PDF 문서 텍스트 추출 및 처리
- 이미지 파일 OCR 처리
- 벡터 임베딩을 통한 의미 기반 검색
- S3를 데이터 소스로 하는 Knowledge Base 구성
- OpenSearch Serverless를 벡터 데이터베이스로 활용
- Rerank 모델을 통한 검색 결과 정확도 향상

### 🤖 AI 기반 응답 생성
- AWS Bedrock RetrieveAndGenerate API 활용
- 검색된 문서를 기반으로 한 맥락적 답변 생성
- 답변 소스 추적 및 표시

### 💬 대화형 인터페이스
- Streamlit 기반 웹 UI
- 실시간 채팅 인터페이스
- 대화 히스토리 관리
- 파일 업로드 기능

## 시스템 아키텍처

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Streamlit UI  │───▶│  Document        │───▶│   Amazon S3         │
│                 │    │  Processor       │    │   (Document Store)  │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
         │                                               │
         ▼                                               ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Chat Handler  │───▶│  Bedrock Client  │───▶│  Knowledge Base     │
│                 │    │                  │    │  (Vector Search)    │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
                                │                         │
                                ▼                         ▼
                       ┌──────────────────┐    ┌─────────────────────┐
                       │  Foundation      │    │  OpenSearch         │
                       │  Model           │    │  Serverless         │
                       └──────────────────┘    └─────────────────────┘
```

## 기술 스택

### Backend
- **Python 3.9+**: 메인 개발 언어
- **AWS Bedrock**: Foundation Model (Claude 3.7 Sonnet) 및 Knowledge Base
- **Amazon OpenSearch Serverless**: 벡터 데이터베이스
- **AWS S3**: 문서 저장소
- **Rerank Model**: Cohere Rerank v3 (검색 결과 정확도 향상)
- **Embedding Model**: Amazon Titan Text Embeddings v2
- **boto3**: AWS SDK

### Frontend
- **Streamlit**: 웹 UI 프레임워크
- **Streamlit Chat**: 채팅 인터페이스 컴포넌트

### 문서 처리
- **PyPDF2/pdfplumber**: PDF 텍스트 추출
- **Pillow**: 이미지 처리
- **pytesseract**: OCR (선택사항)

## 프로젝트 구조

```
my-rag-chatbot-2/
├── README.md                    # 프로젝트 문서 (현재 파일)
├── requirements.txt             # Python 의존성
├── .env.example                # 환경 변수 템플릿
├── .gitignore                  # Git 무시 파일
│
├── app.py                      # Streamlit 메인 애플리케이션
│
├── src/                        # 소스 코드
│   ├── __init__.py
│   ├── bedrock_client.py       # AWS Bedrock 클라이언트
│   ├── knowledge_base.py       # Knowledge Base 관리
│   ├── document_processor.py   # 문서 처리 유틸리티
│   ├── chat_handler.py         # 채팅 로직 처리
│   └── utils.py               # 공통 유틸리티
│
├── config/                     # 설정 파일
│   └── settings.py            # 애플리케이션 설정
│
├── data/                       # 데이터 디렉토리
│   ├── uploads/               # 업로드된 파일 임시 저장
│   └── samples/               # 샘플 문서
│
└── tests/                      # 테스트 코드
    ├── __init__.py
    ├── test_bedrock_client.py
    ├── test_document_processor.py
    └── test_chat_handler.py
```

### 📁 디렉토리별 상세 설명

#### `src/` - 소스 코드
**메인 애플리케이션 코드가 들어가는 핵심 디렉토리**
- `bedrock_client.py`: AWS Bedrock API 호출, Foundation Model 통신 관리
- `knowledge_base.py`: Knowledge Base 검색, RetrieveAndGenerate API 호출
- `document_processor.py`: PDF, 이미지, 텍스트 파일 처리 및 전처리
- `chat_handler.py`: 채팅 세션 관리, 대화 히스토리, 응답 생성 로직
- `utils.py`: 공통 유틸리티 함수, 헬퍼 함수들

#### `config/` - 설정 관리
**애플리케이션 설정 및 상수 관리**
- `settings.py`: 앱 설정값, 기본값, 상수 정의

#### `data/` - 데이터 저장소
**파일 및 데이터 관리 디렉토리**
- `uploads/`: 사용자가 업로드한 파일들의 임시 저장 공간
- `samples/`: 테스트 및 데모용 샘플 문서들

#### `tests/` - 테스트 코드
**품질 보증을 위한 테스트 코드**
- 각 모듈별 단위 테스트 및 통합 테스트 파일들

### 🔄 데이터 흐름 예시
```
사용자 파일 업로드 
→ data/uploads/에 저장 
→ src/document_processor.py가 파일 처리 
→ S3에 업로드 및 Knowledge Base 동기화
→ 사용자 질문 입력
→ src/chat_handler.py가 요청 처리
→ src/bedrock_client.py가 RetrieveAndGenerate API 호출
→ 응답 생성 및 Streamlit UI에 표시
```

## 개발 단계

### Phase 1: 기본 설정 및 인프라
- [ ] AWS Bedrock Knowledge Base 생성
- [ ] S3 버킷 설정
- [ ] IAM 역할 및 정책 구성
- [ ] 개발 환경 설정

### Phase 2: 핵심 기능 구현
- [ ] Bedrock 클라이언트 구현
- [ ] 문서 처리 모듈 개발
- [ ] Knowledge Base 연동
- [ ] RetrieveAndGenerate API 통합

### Phase 3: UI 개발
- [ ] Streamlit 기본 레이아웃
- [ ] 채팅 인터페이스 구현
- [ ] 파일 업로드 기능
- [ ] 응답 표시 및 소스 추적

### Phase 4: 에이전트 적용
- [ ] 에러 처리 및 로깅
- [ ] 성능 최적화
- [ ] 테스트 코드 작성
- [ ] 문서화 완성

## 환경 설정 요구사항

### AWS 리소스
```bash
# 필요한 AWS 서비스
- AWS Bedrock (Foundation Models)
- AWS Bedrock Knowledge Base
- Amazon S3 (문서 저장)
- Amazon OpenSearch Serverless (벡터 DB)
```

### 환경 변수
```env
# .env 파일 예시
AWS_REGION=us-east-1
AWS_PROFILE=default

# Bedrock 설정
BEDROCK_KNOWLEDGE_BASE_ID=your-kb-id
BEDROCK_MODEL_ID=anthropic.claude-3-7-sonnet-20240620-v1:0
BEDROCK_EMBEDDING_MODEL_ID=amazon.titan-embed-text-v2:0
BEDROCK_RERANK_MODEL_ID=cohere.rerank-v3-5:0

# S3 설정
S3_BUCKET_NAME=your-document-bucket
S3_PREFIX=documents/

# 애플리케이션 설정
MAX_FILE_SIZE_MB=10
SUPPORTED_FILE_TYPES=pdf,txt,md,jpg,jpeg,png
```

### Python 의존성 (예상)
```txt
streamlit>=1.28.0
boto3>=1.34.0
python-dotenv>=1.0.0
PyPDF2>=3.0.0
Pillow>=10.0.0
streamlit-chat>=0.1.1
```

## 성공 지표

이 프로젝트의 성공은 다음 지표로 측정됩니다:

1. **기능적 완성도**: 모든 계획된 기능의 구현 완료
2. **사용자 경험**: 직관적이고 반응성 좋은 UI
3. **정확도**: 관련성 높은 문서 검색 및 정확한 답변 생성
4. **성능**: 합리적인 응답 시간 (< 10초)
5. **안정성**: 에러 처리 및 예외 상황 대응

## 다음 단계

1. **AWS 리소스 설정**: Bedrock Knowledge Base 및 S3 버킷 생성
2. **개발 환경 구축**: 가상환경 설정 및 의존성 설치
3. **프로토타입 개발**: 기본적인 문서 업로드 및 검색 기능 구현
4. **점진적 기능 추가**: 단계별로 기능을 추가하며 테스트

---

이 README는 프로젝트 개발 과정에서 지속적으로 업데이트될 예정입니다.
