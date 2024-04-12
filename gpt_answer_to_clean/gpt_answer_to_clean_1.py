import json
import re
from tqdm import tqdm
from nltk.tokenize import sent_tokenize


def find_no_need_mention(text):

    pattern_1 = r"in Document \d"
    pattern_2 = r"\(Document \d+\)"
    pattern_3 = r"Reference Document \d"
    pattern_4 = r"\d+\. "
    pattern_5 = r"Document \d"

    clean_text = re.sub(pattern_1, "", text)
    clean_text = re.sub(pattern_2, "", clean_text)
    clean_text = re.sub(pattern_3, "", clean_text)
    clean_text = re.sub(pattern_4, "", clean_text)
    clean_text = re.sub(pattern_5, "", clean_text)
    if clean_text.startswith("- "):
        clean_text = clean_text.replace("-", "")
    return clean_text


## 대용량 json 파일 불러와 로드
with open("output\experiment3\output_3_same_ex1.json", "r", encoding="UTF-8") as f:
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
        if gpt_answer_only_supporting_facts == []:
            gpt_answer_only_supporting_facts = gpt_answer.split("## Supporting fact:")[1:]
            if gpt_answer_only_supporting_facts == []:
                gpt_answer_only_supporting_facts = gpt_answer.split("## Supporting facts :")[1:]
        if gpt_answer_only_supporting_facts == []:
            print("supporting fact 없음")
            print(i)
        for sentences_set in gpt_answer_only_supporting_facts:
            clean_sentence = find_no_need_mention(sentences_set.strip())
            sentences = sent_tokenize(clean_sentence)
            for part in sentences:
                clean_sentence = find_no_need_mention(part.strip())
                if clean_sentence.strip() != "":
                    re_json_data["gpt_support"].append(clean_sentence.strip())

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

with open("output\experiment3\output_3_clean_ex1_.json", "w", encoding="UTF-8") as out_file:
    json.dump(a, out_file, indent=4, ensure_ascii=False)
