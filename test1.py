import json
from tqdm import tqdm

## 대용량 json 파일 불러와 로드
with open("new_hotpot.json", "r") as f:
    json_data = json.load(f)

with open("output_answer.txt", "w", encoding="UTF-8") as out_file:
    for i, data in tqdm(enumerate(json_data)):
        context = data["context"]
        out_file.write("\n\n" + "## Reference documents" + "\n")
        for index, j in enumerate(context):
            title = j[0]
            sentences = ""
            for sent in j[1]:
                sentences = sentences + sent
            write_sent = '[{}] "{}", {}'.format(index + 1, title, sentences)
            out_file.write(write_sent + "\n")

        out_file.write("\n" + "## Question : " + data["question"])
        out_file.write("\n" + "## Answer : " + data["answer"] + "\n\n")
        out_file.write("\n" + "## Supporting facts : " + data["supporting_facts"] + "\n\n")
