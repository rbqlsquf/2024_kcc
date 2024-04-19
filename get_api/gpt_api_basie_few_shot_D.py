import os
from openai import OpenAI
import json

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
    os.environ["OPENAI_API_KEY"] = "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"

    messages = [
        {
            "role": "system",
            "content": "Here are examples.\n\n<Output format>\n## Question : What profession do Fred Olen Ray and R. G. Springsteen have in common?\n## Answer : director\n## Supporting fact :\nFred Olen Ray (born September 10, 1954) is an American film director, producer, screenwriter, actor, and cinematographer.\nRobert G. Springsteen (September 8, 1904 \u2013 December 9, 1989) was an American director of Hollywood B movies and television shows.\n\n<Output format>\n## Question : Do both Holcus and Limonium belong to the same taxonomic category?\n## Answer : yes\n## Supporting fact :\nHolcus (soft-grass or velvetgrass) is a genus of African and Eurasian plants in the oat tribe within the grass family.\nLimonium is a genus of 120 flowering plant species.\n\n<Output format>\n## Question : To which taxonomic category do both Wittrockia and Aristotelia belong?\n## Answer : genus\n## Supporting fact :\nWittrockia is a genus of the botanical family Bromeliaceae, subfamily Bromelioideae.\nIt is named in honor of the Greek philosopher Aristoteles.\n\n<Instruction>\nI would like to request you to make an answer for the following question.\nI also request you to provide supporting facts of the answer. Supporting fact refers to a sentence that is necessary to infer the answer of the question. The number of supporting facts can be one or more.\nPlease provide answer and supporting facts in the output format at the bottom.\nNever leave an answer blank. Always fill in the output format",
        },
        {"role": "user", "content": "user query here (optional)"},
    ]

    # gpt에 넣을 데이터 불러오기
    with open("data/new_hotpot.json", "r") as f:
        json_data = json.load(f)

    a = []
    json_writing = {
        "data_number": "",
        "question": "",
        "real_answer": "",
        "supporting_fact": [],
        "gpt_answer": "",
        "message_for_gpt": "",
    }

    document_set = {"number": "", "title": "", "sentences": []}
    # 데이터 한 세트에 대해서 gpt한테 질문할 내용
    message = ""
    for i, data in enumerate(json_data):
        message = ""
        context = data["context"]
        supporting_facts = data["supporting_facts"]

        json_writing["data_number"] = "number #{}".format(i)
        message = "<Output format>"
        message = message + "\n" + "## Question : " + data["question"]
        json_writing["question"] = data["question"]
        message = message + "\n" + "## Answer : "
        json_writing["real_answer"] = data["answer"]
        message = message + "\n" + "## Supporting fact : "
        json_writing["message_for_gpt"] = message
        # gpt에게 message와 respnse 받아오기
        messages[1]["content"] = message
        response = gpt_api(messages)
        print("\n\n\n")
        print("message")
        print(message)
        print("\n\n\n")
        print("response")
        print(response)
        json_writing["gpt_answer"] = response
        a.append(json_writing)
        json_writing = {"data_number": "", "question": "", "real_answer": "", "supporting_fact": [], "gpt_answer": ""}

    with open("output/experiment1_few_shot_no_document/3-shot/output_must.json", "w", encoding="UTF-8") as out_file:
        json.dump(a, out_file, indent=4, ensure_ascii=False)
