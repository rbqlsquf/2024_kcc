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
            "content": "## Instruction : Write the answer using only Reference documents(some of which might be irrelevant). And extract the supporting facts to the given sentence number.",
        },
        {"role": "user", "content": "user query here (optional)"},
    ]

    # gpt에 넣을 데이터 불러오기
    with open("new_hotpot.json", "r") as f:
        json_data = json.load(f)

    a = []
    json_writing = {
        "context": [],
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
        message = "## Reference documents" + "\n"

        concat_supporting_sent = ""
        document_number_support_sent = ""
        support_dic = {}
        write_supporting_sent = ""
        for sup_sent in supporting_facts:
            title = sup_sent[0]  # supporting fact의 제목
            set_num = sup_sent[1]  # 문장번호
            support_dic[title] = []
            support_dic[title].append(set_num)
        # 전체 sentence number 세기 위함
        total_sentence_number = 1
        document_sentence_number = 0
        for index, j in enumerate(context):
            title = j[0]
            document_set = {"number": "", "title": "", "sentences": []}
            sentences = ""
            if title in support_dic:
                document_sentence_number = 0
                for sent in j[1]:
                    sentence = "[{}] {}".format(total_sentence_number, sent) + "\n"
                    sentences = sentences + sentence
                    document_set["sentences"].append(sentence)
                    document_number_support_sent = "Document {} : [{}]".format(index + 1, total_sentence_number)
                    total_sentence_number += 1
                    if document_sentence_number in support_dic[title]:
                        concat_supporting_sent = document_number_support_sent + j[1][document_sentence_number]
                        json_writing["supporting_fact"].append(concat_supporting_sent)
                    document_sentence_number += 1

            else:
                for sent in j[1]:
                    sentence = "[{}] {}".format(total_sentence_number, sent) + "\n"
                    sentences = sentences + sentence
                    document_set["sentences"].append(sentence)
                    total_sentence_number += 1

            write_sent = "Document {} : {}".format(index + 1, title) + "\n" + "{}".format(sentences)
            document_set["number"] = index + 1
            document_set["title"] = title
            json_writing["context"].append(document_set)

            message = message + write_sent + "\n"

        message = message + "\n" + "## Question : " + data["question"]
        json_writing["question"] = data["question"]
        message = message + "\n" + "## Answer : "
        json_writing["real_answer"] = data["answer"]
        message = message + "\n" + "## Supporting facts : "
        json_writing["message_for_gpt"] = message
        # gpt에게 message와 respnse 받아오기
        messages[1]["content"] = message
        response = gpt_api(messages)
        print("\n\n\n")
        print("message")
        print(message)
        print("\n\n\n")
        print("response")
        print("response")
        json_writing["gpt_answer"] = response
        a.append(json_writing)
        json_writing = {"context": [], "question": "", "real_answer": "", "supporting_fact": [], "gpt_answer": ""}

    with open("output_gpt_2.json", "w", encoding="UTF-8") as out_file:
        json.dump(a, out_file, indent=4, ensure_ascii=False)
