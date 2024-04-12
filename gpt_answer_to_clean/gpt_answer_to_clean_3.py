import json
import re
from tqdm import tqdm


## 대용량 json 파일 불러와 로드
with open("output\experiment3\output_3.json", "r", encoding="UTF-8") as f:
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

    re_json_data["real_support"] = data["supporting_fact"]

    gpt_answer = data["gpt_answer"]
    if "## Answer" in gpt_answer:
        gpt_answer_only_answer = gpt_answer.split("## Answer")[1].replace(":", "").split("##")[0]
        re_json_data["gpt_answer"] = gpt_answer_only_answer
    if "## Supporting fact" in gpt_answer:
        gpt_answer_only_supporting_facts = gpt_answer.split("## Supporting fact :")[1:]
        for part in gpt_answer_only_supporting_facts:
            re_json_data["gpt_support"].append(part.strip())

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

with open("output\experiment3\output_3_clean.json", "w", encoding="UTF-8") as out_file:
    json.dump(a, out_file, indent=4, ensure_ascii=False)
