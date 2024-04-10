import json

messages = [
    {
        "role": "system",
        "content": "## Instruction : Write the answer using only Reference documents(some of which might be irrelevant). And for the answer, extract the supporting facts exactly matched the Reference document.",
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

# 데이터 한 세트에 대해서 gpt한테 질문할 내용
message = ""
for i, data in enumerate(json_data):
    message = ""
    context = data["context"]
    supporting_facts = data["supporting_facts"]
    message = "## Reference documents" + "\n"

    concat_supporting_sent = ""
    support_dic = {}
    write_supporting_sent = ""
    for sup_sent in supporting_facts:
        title = sup_sent[0]  # supporting fact의 제목
        set_num = sup_sent[1]  # 문장번호
        support_dic[title] = []
        support_dic[title].append(set_num)

    for index, j in enumerate(context):
        title = j[0]
        if title in support_dic:
            concat_supporting_sent = "[{}] ".format(index + 1)
            for dic_num in support_dic[title]:
                concat_supporting_sent = concat_supporting_sent + j[1][dic_num]
                json_writing["supporting_fact"].append(concat_supporting_sent)
                write_supporting_sent = write_supporting_sent + concat_supporting_sent
                write_supporting_sent = write_supporting_sent + "\n"
        sentences = ""
        for sent in j[1]:
            sentences = sentences + sent
        write_sent = '[{}] "{}", {}'.format(index + 1, title, sentences)
        json_writing["context"].append("document #{}, {} : {} ".format(index + 1, title, sentences))

        message = message + write_sent + "\n"

    message = message + "\n" + "## Question : " + data["question"]
    json_writing["question"] = data["question"]
    message = message + "\n" + "## Answer : "
    json_writing["real_answer"] = data["answer"]
    message = message + "\n" + "## Supporting facts : "
    json_writing["message_for_gpt"] = message
    # gpt에게 message와 respnse 받아오기
    messages[1]["content"] = message
    print("message")
    print(message)
    print("response")
    print("response")
    json_writing["gpt_answer"] = "response"
    a.append(json_writing)
    json_writing = {"context": [], "question": "", "real_answer": "", "supporting_fact": [], "gpt_answer": ""}

with open("output_gpt.json", "w", encoding="UTF-8") as out_file:
    json.dump(a, out_file, indent=4, ensure_ascii=False)
