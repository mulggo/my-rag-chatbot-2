# 🤖 건설공사 AI 에이전트 아키텍처

## 시스템 개요
기존 RAG 챗봇을 지능형 에이전트로 업그레이드하여 자율적 판단과 다중 도구 활용이 가능한 시스템 구축

## 에이전트 구성 요소

### 1. 중앙 에이전트 (Agent Orchestrator)
- **역할**: 사용자 의도 파악 및 적절한 도구 선택
- **기능**: 
  - 질문 분석 및 분류
  - 도구 선택 및 실행 순서 결정
  - 결과 통합 및 최종 답변 생성

### 2. 도구 모음 (Tool Kit)

#### 🔍 Knowledge Base Tool
- **기능**: 기존 RAG 검색
- **사용 시기**: 건설 표준품셈 관련 질문

#### 🧮 Calculator Tool  
- **기능**: 수학적 계산 (인력 계산, 비용 산정 등)
- **사용 시기**: 수량 계산, 비율 계산 필요시

#### 📊 Data Analysis Tool
- **기능**: 업로드된 파일 분석 (Excel, CSV 등)
- **사용 시기**: 데이터 분석 요청시

#### 🔧 Construction Calculator Tool
- **기능**: 건설 전용 계산 (콘크리트량, 철근량 등)
- **사용 시기**: 건설 공사량 산정 필요시

#### 📋 Report Generator Tool
- **기능**: 분석 결과를 보고서 형태로 생성
- **사용 시기**: 종합적인 분석 결과 제시 필요시

### 3. 메모리 시스템
- **대화 기록**: 이전 대화 맥락 유지
- **작업 기록**: 수행한 계산이나 분석 결과 저장
- **학습 기록**: 사용자 선호도 및 패턴 학습

## 에이전트 워크플로우

```
사용자 질문 입력
    ↓
의도 분석 (Agent Orchestrator)
    ↓
도구 선택 및 실행 계획 수립
    ↓
도구 실행 (순차적 또는 병렬)
    ↓
결과 통합 및 검증
    ↓
최종 답변 생성 및 후속 제안
```

## 예시 시나리오

### 시나리오 1: 복합 질문
**질문**: "80mm 감압밸브 100개 설치에 필요한 총 인력과 예상 비용은?"

**에이전트 실행 과정**:
1. KB Tool: 80mm 감압밸브 단위 인력 검색 (6.224인, 1.297인)
2. Calculator Tool: 100개 × 단위 인력 계산
3. Construction Calculator: 인건비 계산 (지역별 노임단가 적용)
4. Report Generator: 종합 보고서 생성

### 시나리오 2: 데이터 분석
**질문**: "이 Excel 파일의 공사비 데이터를 분석해서 최적화 방안을 제시해줘"

**에이전트 실행 과정**:
1. Data Analysis Tool: Excel 파일 분석
2. KB Tool: 관련 표준품셈 정보 검색
3. Calculator Tool: 최적화 계산
4. Report Generator: 분석 보고서 및 개선안 제시

## 기술 스택

### 에이전트 프레임워크
- **LangChain Agents**: 도구 선택 및 실행
- **AWS Bedrock Agents**: 클라우드 네이티브 에이전트
- **Custom Agent Logic**: 건설 도메인 특화 로직

### 도구 구현
- **Function Calling**: Claude 3.7 Sonnet의 함수 호출 기능
- **Tool Integration**: 각 도구를 독립적 모듈로 구현
- **Error Handling**: 도구 실행 실패시 대안 제시

## 구현 단계

### Phase 4.1: 기본 에이전트 구조
- [ ] Agent Orchestrator 구현
- [ ] 기존 KB를 Tool로 래핑
- [ ] Calculator Tool 추가

### Phase 4.2: 고급 도구 추가
- [ ] Data Analysis Tool 구현
- [ ] Construction Calculator Tool 개발
- [ ] Report Generator 구현

### Phase 4.3: 메모리 및 학습
- [ ] 대화 메모리 시스템
- [ ] 사용자 선호도 학습
- [ ] 성능 최적화

### Phase 4.4: UI/UX 개선
- [ ] 에이전트 사고 과정 시각화
- [ ] 도구 실행 상태 표시
- [ ] 인터랙티브 보고서 생성
