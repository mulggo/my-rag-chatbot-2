import boto3
from botocore.exceptions import ClientError

def create_knowledge_base_with_auto_vector_store(kb_name, role_arn, region='us-east-1'):
    """
    AWS Bedrock이 자동으로 OpenSearch Serverless 컬렉션과 인덱스를 생성하도록 하는 방식
    공식 문서의 "Quick create a new vector store" 옵션
    """
    bedrock_agent_client = boto3.client('bedrock-agent', region_name=region)
    
    try:
        response = bedrock_agent_client.create_knowledge_base(
            name=kb_name,
            description='Knowledge Base for RAG chatbot with auto-created vector store',
            roleArn=role_arn,
            knowledgeBaseConfiguration={
                'type': 'VECTOR',
                'vectorKnowledgeBaseConfiguration': {
                    'embeddingModelArn': f'arn:aws:bedrock:{region}::foundation-model/amazon.titan-embed-text-v2:0'
                }
            },
            storageConfiguration={
                'type': 'OPENSEARCH_SERVERLESS',
                'opensearchServerlessConfiguration': {
                    # collectionArn 완전히 제거 - AWS가 자동 생성
                    # vectorIndexName도 제거 - AWS가 자동 생성
                    # fieldMapping도 제거 - AWS가 기본값으로 자동 설정
                }
            }
        )
        
        kb_id = response['knowledgeBase']['knowledgeBaseId']
        kb_arn = response['knowledgeBase']['knowledgeBaseArn']
        
        print(f"✅ Knowledge Base 생성 완료!")
        print(f"Knowledge Base ID: {kb_id}")
        print(f"Knowledge Base ARN: {kb_arn}")
        print(f"✅ AWS Bedrock이 자동으로 OpenSearch Serverless 컬렉션과 인덱스를 생성합니다!")
        print(f"⏳ 컬렉션 생성에는 몇 분이 소요될 수 있습니다...")
        
        return kb_id, kb_arn
        
    except ClientError as e:
        print(f"❌ Knowledge Base 생성 오류: {e}")
        return None, None

def create_knowledge_base_with_custom_vector_store(kb_name, role_arn, collection_arn, region='us-east-1'):
    """
    기존 OpenSearch Serverless 컬렉션을 사용하는 방식 (고급 사용자용)
    """
    bedrock_agent_client = boto3.client('bedrock-agent', region_name=region)
    
    try:
        response = bedrock_agent_client.create_knowledge_base(
            name=kb_name,
            description='Knowledge Base for RAG chatbot with existing vector store',
            roleArn=role_arn,
            knowledgeBaseConfiguration={
                'type': 'VECTOR',
                'vectorKnowledgeBaseConfiguration': {
                    'embeddingModelArn': f'arn:aws:bedrock:{region}::foundation-model/amazon.titan-embed-text-v2:0'
                }
            },
            storageConfiguration={
                'type': 'OPENSEARCH_SERVERLESS',
                'opensearchServerlessConfiguration': {
                    'collectionArn': collection_arn,
                    'vectorIndexName': 'bedrock-knowledge-base-default-index',
                    'fieldMapping': {
                        'vectorField': 'bedrock-knowledge-base-default-vector',
                        'textField': 'AMAZON_BEDROCK_TEXT',
                        'metadataField': 'AMAZON_BEDROCK_METADATA'
                    }
                }
            }
        )
        
        kb_id = response['knowledgeBase']['knowledgeBaseId']
        kb_arn = response['knowledgeBase']['knowledgeBaseArn']
        
        print(f"✅ Knowledge Base 생성 완료!")
        print(f"Knowledge Base ID: {kb_id}")
        print(f"Knowledge Base ARN: {kb_arn}")
        
        return kb_id, kb_arn
        
    except ClientError as e:
        print(f"❌ Knowledge Base 생성 오류: {e}")
        return None, None

# 사용 예시
if __name__ == "__main__":
    kb_name = "my-rag-chatbot-kb"
    role_arn = "arn:aws:iam::YOUR_ACCOUNT:role/AmazonBedrockExecutionRoleForKnowledgeBase_YOUR_ROLE"
    
    print("🚀 AWS 자동 생성 방식으로 Knowledge Base 생성 중...")
    kb_id, kb_arn = create_knowledge_base_with_auto_vector_store(kb_name, role_arn)
    
    if kb_id:
        print(f"\n🎉 성공! Knowledge Base가 생성되었습니다.")
        print(f"다음 단계: Data Source를 연결하세요.")
    else:
        print(f"\n❌ 실패! 로그를 확인하세요.")
