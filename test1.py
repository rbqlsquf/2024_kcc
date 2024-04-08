import json
from tqdm import tqdm

## 대용량 json 파일 불러와 로드
with open("new_hotpot.json", "r") as f:
    json_data = json.load(f)

with open("output_answer.txt", "w", encoding="UTF-8") as out_file:
    for i, data in tqdm(enumerate(json_data)):
        context = data["context"]
        out_file.write("\n\n" + "## Reference documents" + "\n")

        # supporting fact 전처리 진행과정
        supporting_facts = data["supporting_facts"]
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
                    write_supporting_sent = write_supporting_sent + concat_supporting_sent
                    write_supporting_sent = write_supporting_sent + "\n"
            sentences = ""
            for sent in j[1]:
                sentences = sentences + sent
            write_sent = '[{}] "{}", {}'.format(index + 1, title, sentences)
            out_file.write(write_sent + "\n")

        out_file.write("\n" + "## Question : " + data["question"])
        out_file.write("\n" + "## Answer : " + data["answer"])
        out_file.write("\n" + "## Supporting facts : " + write_supporting_sent + "\n\n")
