import openai
# OpenAI 라이브러리 버전 0.28로 다운그레이드하여 이전 API 방식으로 코드를 실행
# pip install openai==0.28

def get_gpt_response(key,prompt):
    openai.api_key = key
    response = openai.chat.completions.create(
        model="gpt-4",  # 사용 모델
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
        max_tokens=300
            
    )        
    return response.choices[0].message.content
    
def check_openai_api_key(api_key):
    client = openai.OpenAI(api_key=api_key)
    try:
        client.models.list()
        return True
    except:
        return False
