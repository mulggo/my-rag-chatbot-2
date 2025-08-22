# 검색 증강 생성(RAG)이란 무엇인가요?
[AWS 계정 생성](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html?pg=what_is_header)
검색 증강 생성이란 무엇인가요? 검색 증강 생성이 중요한 이유는 무엇인가요? 검색 증강 생성의 이점은 무엇인가요? 검색 증강 생성은 어떻게 작동하나요? 검색 증강 생성과 시맨틱 검색의 차이점은 무엇인가요? AWS는 검색 증강 생성 요구 사항을 어떻게 지원할 수 있나요?
## 검색 증강 생성이란 무엇인가요?
검색 증강 생성(RAG)은 대규모 언어 모델의 출력을 최적화하여 응답을 생성하기 전에 훈련 데이터 소스 외부의 신뢰할 수 있는 기술 자료를 참조하도록 하는 프로세스입니다. 대규모 언어 모델(LLM)은 방대한 양의 데이터를 기반으로 훈련되며 수십억 개의 파라미터를 사용하여 질문에 대한 답변, 언어 번역, 문장 완성 등의 작업에서 독창적인 결과를 생성합니다. RAG는 이미 강력한 LLM의 기능을 특정 도메인이나 조직의 내부 기술 자료로 확장하므로 모델을 다시 훈련할 필요가 없습니다. 이는 LLM 결과를 개선하여 다양한 상황에서 연관성, 정확성 및 유용성을 유지하기 위한 비용 효율적인 접근 방식입니다.
## 검색 증강 생성이 중요한 이유는 무엇인가요?
LLM은 지능형 [챗봇](https://aws.amazon.com/what-is/chatbot/) 및 기타 [자연어 처리(NLP)](https://aws.amazon.com/what-is/nlp/) 애플리케이션을 지원하는 핵심 [인공 지능(AI)](https://aws.amazon.com/what-is/artificial-intelligence/) 기술입니다. 신뢰할 수 있는 지식 소스를 상호 참조하여 다양한 상황에서 사용자 질문에 답변할 수 있는 봇을 만드는 것이 LLM의 목표입니다. 안타깝게도 LLM 기술의 특성상 LLM 응답에 대한 예측이 불가능합니다. 또한 LLM 훈련 데이터는 정적이며 보유한 지식은 일정 기간 동안만 유용합니다.
LLM의 알려진 문제점은 다음과 같습니다.
  * 답이 없을 때 허위 정보를 제공합니다.
  * 사용자가 구체적이고 최신의 응답을 기대할 때 오래되었거나 일반적인 정보를 제공합니다.
  * 신뢰할 수 없는 출처로부터 응답을 생성합니다.
  * 다양한 훈련 소스에서 동일한 용어를 사용하여 다른 내용을 설명하면서 용어 혼동으로 인해 응답이 부정확합니다.
[대형 언어 모델](https://aws.amazon.com/what-is/large-language-model/)은 현재 상황에 대한 최신 정보는 없지만 항상 절대적인 자신감을 가지고 모든 질문에 답변하는 열정적인 신입 사원으로 생각할 수 있습니다. 안타깝게도 이러한 태도는 사용자 신뢰에 부정적인 영향을 미칠 수 있으며 챗봇이 모방해서는 안 되는 것입니다.
RAG는 이러한 문제 중 일부를 해결하기 위한 접근 방식입니다. LLM을 리디렉션하여 신뢰할 수 있는 사전 결정된 지식 출처에서 관련 정보를 검색합니다. 조직은 생성된 텍스트 출력을 더 잘 제어할 수 있으며 사용자는 LLM이 응답을 생성하는 방식에 대한 인사이트를 얻을 수 있습니다.
## 검색 증강 생성의 이점은 무엇인가요?
RAG 기술은 조직의 [생성형 AI](https://aws.amazon.com/what-is/generative-ai/) 관련 작업에 있어 여러 가지 이점을 제공합니다.
### **비용 효율적인 구현**
챗봇 개발은 일반적으로 [파운데이션 모델](https://aws.amazon.com/what-is/foundation-models/)을 사용하여 시작됩니다. 파운데이션 모델(FM)은 광범위한 일반화 데이터와 레이블이 지정되지 않은 데이터에 대해 훈련된 API 액세스 가능 LLM입니다. 조직 또는 도메인별 정보를 위해 FM을 재교육하는 데 컴퓨팅 및 재정적 비용이 많이 소요됩니다. RAG를 통해 LLM에 새 데이터를 더 비용 효율적으로 도입할 수 있습니다. 그리고 생성형 인공 지능(생성형 AI) 기술을 보다 폭넓게 접근하고 사용할 수도 있습니다.
### **최신 정보**
LLM의 원본 훈련 데이터 소스가 요구 사항에 적합하더라도 연관성을 유지하기가 어렵습니다. 개발자는 RAG를 사용하여 생성형 모델에 최신 연구, 통계 또는 뉴스를 제공할 수 있습니다. RAG를 사용하여 LLM을 라이브 소셜 미디어 피드, 뉴스 사이트 또는 기타 자주 업데이트되는 정보 소스에 직접 연결할 수 있습니다. 그러면 LLM은 사용자에게 최신 정보를 제공할 수 있습니다.
### **사용자 신뢰 강화**
RAG은 LLM이 소스의 저작자 표시를 통해 정확한 정보를 제공할 수 있게 합니다. 출력에는 소스에 대한 인용 또는 참조가 포함될 수 있습니다. 추가 설명이나 세부 정보가 필요한 경우 사용자가 소스 문서를 직접 찾아볼 수도 있습니다. 이를 통해 생성형 AI 솔루션에 대한 신뢰와 확신을 높일 수 있습니다.
### **개발자 제어 강화**
개발자는 RAG를 사용하여 채팅 애플리케이션을 보다 효율적으로 테스트하고 개선할 수 있습니다. 변화하는 요구 사항 또는 부서 간 사용에 맞게 LLM의 정보 소스를 제어하고 변경할 수 있습니다. 또한 개발자는 민감한 정보 검색을 다양한 인증 수준으로 제한하여 LLM이 적절한 응답 생성을 유도할 수 있습니다. 또한 LLM이 특정 질문에 대해 잘못된 정보 소스를 참조하는 경우 문제를 해결하고 수정할 수도 있습니다. 조직은 더 광범위한 애플리케이션을 대상으로 생성형 AI 기술을 보다 자신 있게 구현할 수 있습니다.
## 검색 증강 생성은 어떻게 작동하나요?
RAG가 없는 경우 LLM은 사용자 입력을 바탕으로 훈련한 정보 또는 이미 알고 있는 정보를 기반으로 응답을 생성합니다. RAG에는 사용자 입력을 활용하여 먼저 새 데이터 소스에서 정보를 가져오는 정보 검색 구성 요소가 도입되었습니다. 사용자 쿼리와 관련 정보가 모두 LLM에 제공됩니다. LLM은 새로운 지식과 학습 데이터를 사용하여 더 나은 응답을 생성합니다. 프로세스의 개요를 아래에서 확인하세요.
### **외부 데이터 생성**
LLM의 원래 학습 데이터 세트 외부에 있는 새 데이터를 _외부 데이터_ 라고 합니다. API, 데이터베이스 또는 문서 리포지토리와 같은 여러 데이터 소스에서 가져올 수 있습니다. 데이터의 형식은 파일, 데이터베이스 레코드 또는 긴 형식의 텍스트와 같이 다양합니다. _임베딩 언어 모델_ 이라고 하는 또 다른 AI 기법은 데이터를 수치로 변환하고 벡터 데이터베이스에 저장합니다. 이 프로세스는 생성형 AI 모델이 이해할 수 있는 지식 라이브러리를 생성합니다.
### **관련 정보 검색**
연관성 검색을 수행하는 단계는 다음과 같습니다. 사용자 쿼리는 벡터 표현으로 변환되고 벡터 데이터베이스와 매칭됩니다. 예를 들어 조직의 인사 관련 질문에 답변할 수 있는 스마트 챗봇을 생각할 수 있습니다. 직원이 _“연차휴가는 얼마나 남았나요?“_ 라고 검색하면 시스템은 개별 직원의 과거 휴가 기록과 함께 연차 휴가 정책 문서를 검색합니다. 이러한 특정 문서는 직원이 입력한 내용과 관련이 높기에 반환됩니다. 수학적 벡터 계산 및 표현을 사용하여 연관성이 계산 및 설정됩니다.
### **LLM 프롬프트 확장**
다음으로 RAG 모델은 검색된 관련 데이터를 컨텍스트에 추가하여 사용자 입력(또는 프롬프트)을 보강합니다. 이 단계에서는 프롬프트 엔지니어링 기술을 사용하여 LLM과 효과적으로 통신합니다. 확장된 프롬프트를 사용하면 대규모 언어 모델이 사용자 쿼리에 대한 정확한 답변을 생성할 수 있습니다.
### **외부 데이터 업데이트**
만약에 외부 데이터가 시간이 경과된 데이터가 된다면 어떻게 될까요? 최신 정보 검색을 유지하기 위해 문서를 비동기적으로 업데이트하고 문서의 임베딩 표현을 업데이트합니다. 자동화된 실시간 프로세스 또는 주기적 배치 처리를 통해 이 작업을 수행할 수 있습니다. 변경 관리에 다양한 데이터 과학 접근 방식을 사용할 수 있기 때문에 데이터 분석에서 흔히 발생하는 과제이기도 합니다.
다음 다이어그램에서 LLM과 함께 RAG를 사용하는 개념적 흐름을 확인하세요.
![](https://docs.aws.amazon.com/images/sagemaker/latest/dg/images/jumpstart/jumpstart-fm-rag.jpg)  
## 검색 증강 생성과 시맨틱 검색의 차이점은 무엇인가요?
시맨틱 검색은 방대한 외부 지식 소스를 LLM 애플리케이션에 추가하려는 조직을 위해 RAG 결과를 개선해 줍니다. 오늘날의 기업들은 매뉴얼, FAQ, 연구 보고서, 고객 서비스 가이드, 인사 관리 문서 리포지토리 등 방대한 양의 정보를 다양한 시스템에 저장합니다. 컨텍스트 검색은 대규모로 실행하기 어려우며, 그로 인해 생성형 출력 품질이 떨어집니다.
시맨틱 검색 기술은 서로 다른 정보가 수록된 여러 대규모 데이터베이스를 스캔하고 데이터를 더 정확하게 검색할 수 있습니다. 예를 들어 질문을 관련 문서에 매핑하고 검색 결과 대신 특정 텍스트를 반환하여 _“작년에 기계 수리에 지출한 금액은 얼마입니까?”_ 와 같은 질문에 답할 수 있습니다. 그러면 개발자는 이 답변을 사용하여 LLM에 더 많은 컨텍스트를 제공할 수 있습니다.
RAG의 기존 또는 키워드 검색 솔루션은 지식 집약적 작업에 대해 제한된 결과를 제공합니다. 또한 개발자는 수동으로 데이터를 준비할 때 워드 임베딩, 문서 청킹 및 기타 복잡한 문제를 해결해야 합니다. 반대로 시맨틱 검색 기술은 모든 지식 기반 준비 작업을 수행하므로 개발자는 그럴 필요가 없습니다. 또한 관련된 시맨틱 구절과 토큰 단어를 연관성에 따라 정렬하여 RAG 페이로드의 품질을 극대화합니다.
## AWS는 검색 증강 생성 요구 사항을 어떻게 지원할 수 있나요?
[Amazon Bedrock](https://aws.amazon.com/bedrock/)은 개발을 간소화하고 프라이버시 및 보안을 유지 관리하는 동시에, 생성형 AI 애플리케이션을 구축할 수 있는 다양한 기능과 함께 고성능 기반 모델을 제공하는 완전관리형 서비스입니다. Amazon Bedrock의 지식 기반을 사용하면 클릭 몇 번으로 FM을 RAG용 데이터 소스에 연결할 수 있습니다. 벡터 변환, 검색 및 개선된 출력 생성이 모두 자동으로 처리됩니다.
자체 RAG를 관리하는 조직을 위한 [Amazon Kendra](https://aws.amazon.com/kendra/)는 기계 학습 기반의 매우 정확한 엔터프라이즈 검색 서비스입니다. Amazon Kendra의 정확도가 높은 시맨틱 랭커와 함께 RAG 워크플로의 엔터프라이즈 검색기로 사용할 수 있는 최적화된 Kendra [Retrive API](https://docs.aws.amazon.com/kendra/latest/APIReference/API_Retrieve.html)를 제공합니다. 예를 들어 검색 API를 사용하여 다음을 수행할 수 있습니다.
  * 각각 최대 200개의 토큰 단어로 구성된 시맨틱 구절을 연관성에 따라 정렬하여 최대 100개까지 검색합니다.
  * [Amazon Simple Storage Service](https://aws.amazon.com/s3/), SharePoint, Confluence 및 기타 웹 사이트와 같은 널리 사용되는 데이터 기술에 사전 구축된 커넥터를 사용합니다.
  * HTML, Word, PowerPoint, PDF, Excel, 텍스트 파일 등 다양한 문서 형식을 지원합니다.
  * 최종 사용자 권한에서 허용되는 문서를 기준으로 응답을 필터링합니다.
또한 Amazon은 더 많은 사용자 지정 생성형 AI 솔루션을 구축하려는 조직을 위한 옵션도 제공합니다. [Amazon SageMaker JumpStart](https://aws.amazon.com/sagemaker/jumpstart/)는 단 몇 번의 클릭만으로 배포할 수 있는 FM, 내장 알고리즘, 사전 구축된 ML 솔루션을 갖춘 ML 허브입니다. 기존 SageMaker 노트북 및 코드 예시를 참조하여 RAG 구현 속도를 높일 수 있습니다.
[지금 무료 계정을 생성하여](https://portal.aws.amazon.com/billing/signup) AWS에서 검색 증강 생성을 시작하세요.
## AWS에서의 다음 단계
### [제품 관련 추가 리소스 확인 가장 포괄적인 생성형 AI 서비스 세트로 보다 빠르게 혁신 ](/ai/generative-ai/services/)
### [무료 계정 가입 AWS 프리 티어에 즉시 액세스할 수 있습니다. 가입 ](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html)
### [콘솔에서 구축 시작 AWS Management Console에서 구축을 시작하세요. 로그인 ](https://console.aws.amazon.com)
[AWS 계정 생성](https://portal.aws.amazon.com/gp/aws/developer/registration/?nc2=h_su&src=header_signup)
## 알아보기
  * [AWS란 무엇인가요?](/what-is-aws/?nc1=f_cc)
  * [클라우드 컴퓨팅이란 무엇인가요?](/what-is-cloud-computing/?nc1=f_cc)
  * [생성형 AI란 무엇인가요?](/what-is/generative-ai/?nc1=f_cc)
  * [클라우드 컴퓨팅 개념 허브](/what-is/?nc1=f_cc)
  * [AWS 클라우드 보안](/security/?nc1=f_cc)
  * [새로운 소식](/new/?nc1=f_cc)
  * [블로그](/blogs/?nc1=f_cc)
  * [보도 자료](https://press.aboutamazon.com/press-releases/aws)
## 리소스
  * [시작하기](/getting-started/?nc1=f_cc)
  * [훈련](/training/?nc1=f_cc)
  * [AWS Solutions Library](/solutions/?nc1=f_cc)
  * [아키텍처 센터](/architecture/?nc1=f_cc)
  * [제품 및 기술 관련 FAQ](/faqs/?nc1=f_dr)
  * [애널리스트 보고서](/resources/analyst-reports/?nc1=f_cc)
  * [AWS 파트너](/partners/work-with-partners/?nc1=f_dr)
  * [AWS의 포용, 다양성, 평등](/diversity-inclusion/?nc1=f_cc)
## 개발자
  * [개발자 센터](/developer/?nc1=f_dr)
  * [SDK 및 도구](/developer/tools/?nc1=f_dr)
  * [AWS에서의 .NET](/developer/language/net/?nc1=f_dr)
  * [AWS에서의 Python](/developer/language/python/?nc1=f_dr)
  * [AWS에서의 Java](/developer/language/java/?nc1=f_dr)
  * [AWS 상의 PHP](/developer/language/php/?nc1=f_cc)
## 도움말
  * [AWS에 문의](/contact-us/?nc1=f_m)
  * [지원 티켓 제출](https://console.aws.amazon.com/support/home/?nc1=f_dr)
  * [AWS re:Post](https://repost.aws/?nc1=f_dr)
  * [지식 센터](https://repost.aws/knowledge-center/?nc1=f_dr)
  * [AWS Support 개요](/premiumsupport/?nc1=f_dr)
  * [전문가의 도움 받기](https://iq.aws.amazon.com/?utm=mkt.foot/?nc1=f_m)
  * [AWS 접근성](/accessibility/?nc1=f_cc)
  * [법적 고지](/legal/?nc1=f_cc)
English
맨 위로 이동
Amazon은 기회 균등을 보장하는 기업입니다(소수/여성/장애/재향 군인/성 정체성/성적 지향/나이).
[](https://twitter.com/awscloud) [ facebook ](https://www.facebook.com/amazonwebservices) [ linkedin ](https://www.linkedin.com/company/amazon-web-services/) [ instagram ](https://www.instagram.com/amazonwebservices/) [ twitch ](https://www.twitch.tv/aws) [ youtube ](https://www.youtube.com/user/AmazonWebServices/Cloud/) [ podcasts ](/podcasts/?nc1=f_cc) [ email ](https://pages.awscloud.com/communication-preferences?trk=homepage)
  * [개인정보 처리방침](/privacy/?nc1=f_pr)
  * [사이트 이용 약관](/terms/?nc1=f_pr)
  * 쿠키 기본 설정
© 2025, Amazon Web Services, Inc. 또는 자회사. All rights reserved.