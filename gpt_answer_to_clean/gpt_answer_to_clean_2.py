import json
import re
from tqdm import tqdm


def extract_number_from_brackets(text):
    pattern = r"\[\d+\]|\['\d+'\]"
    matches = re.findall(pattern, text)
    numbers = []
    for match in matches:
        numbers.append(re.sub(r"[^0-9]", "", match))
    if numbers == []:
        text_s = text.split(",")
        for num in text_s:
            numbers.append(re.sub(r"[^0-9]", "", num))

    return numbers


## 대용량 json 파일 불러와 로드
with open("output\experiment1\output_1.json", "r", encoding="UTF-8") as f:
    json_data = json.load(f)


a = []
re_json_data = {
    "data_number": "",
    "question": "",
    "real_answer": "",
    "gpt_answer": "",
    "real_support": [],
    "gpt_support": [],
}


for i, data in tqdm(enumerate(json_data)):
    re_json_data["data_number"] = "number #{}".format(i)
    re_json_data["question"] = data["question"]
    re_json_data["real_answer"] = data["real_answer"]

    supporting_fact = data["supporting_fact"]
    for sent in supporting_fact:
        split_sent = sent.split(":", maxsplit=1)[1].split("[")[1].split("]")[0]
        # 문장 인덱스 번호를 가지고 옴
        re_json_data["real_support"].append(split_sent)

    gpt_answer = data["gpt_answer"]
    if "## Answer" in gpt_answer:
        gpt_answer_only_answer = gpt_answer.split("## Answer")[1].replace(":", "").split("##")[0]
        re_json_data["gpt_answer"] = gpt_answer_only_answer
    if "## Supporting fact" in gpt_answer:
        gpt_answer_only_supporting_facts = gpt_answer.split("## Supporting fact")[1]
        gpt_support_number = extract_number_from_brackets(gpt_answer_only_supporting_facts)
        re_json_data["gpt_support"] = gpt_support_number
    else:
        re_json_data["gpt_answer"] = "Error"
        re_json_data["gpt_support"] = gpt_answer

    a.append(re_json_data)
    re_json_data = {
        "data_number": "",
        "question": "",
        "real_answer": "",
        "gpt_answer": "",
        "real_support": [],
        "gpt_support": [],
    }

with open("output\experiment1\output_1_clean.json", "w", encoding="UTF-8") as out_file:
    json.dump(a, out_file, indent=4, ensure_ascii=False)
