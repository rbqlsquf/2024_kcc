import os
from openai import OpenAI

# openai 라이브러리 설치 필수
# pip install openai


def gpt_api(messages):
    client = OpenAI()

    # https://platform.openai.com/docs/models/overview
    # 사용할 수 있는 모델의 종류는 여기서 확인
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    # https://platform.openai.com/api-keys
    # 여기서 key 발급 후 SECRET KEY (sk-...) 를 string으로
    os.environ["OPENAI_API_KEY"] = "(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)"

    messages = [
        {"role": "system", "content": "system prompt here (optional)"},
        {"role": "user", "content": "user query here (optional)"},
    ]

    response = gpt_api(messages)
    print(response)
