import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def summarize_title(title):
    # 簡短一句話摘要（若無 API Key 則回傳標題本身）
    if not openai.api_key:
        return title
    try:
        prompt = f"""請用繁體中文用一句話摘要以下新聞標題的重點，並用簡短一句話說明它可能對股市的影響：\n\n{title}\n"""
        resp = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role':'user','content':prompt}],
            max_tokens=60,
            temperature=0.2
        )
        return resp.choices[0].message['content'].strip()
    except Exception as e:
        print('OpenAI error:', e)
        return title
