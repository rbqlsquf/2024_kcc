import json

with open("output/experiment1_few_shot_no_document/1-shot/output.json", "r", encoding="UTF-8") as f:
    json_data = json.load(f)

a = []

for i, data in enumerate(json_data):
    data["data_number"] = "number #{}".format(i)
    a.append(data)

with open("output/experiment1_few_shot_no_document/1-shot/output_.json", "w", encoding="UTF-8") as out_file:
    json.dump(a, out_file, indent=4, ensure_ascii=False)
