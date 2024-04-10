import json


with open("gpt_answer\output_gpt_2_jjs_2.json", "r", encoding="UTF8") as f:
    json_data = json.load(f)

a = []
json_writing = {
    "data_number": "",
    "context": [],
    "question": "",
    "real_answer": "",
    "supporting_fact": [],
    "gpt_answer": "",
    "message_for_gpt": "",
}

for i, data in enumerate(json_data):
    json_writing["data_number"] = "number #{}".format(i)
    json_writing["question"] = data["question"]
    json_writing["real_answer"] = data["real_answer"]
