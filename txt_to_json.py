import json

data = {"Reference document": [], "Question": "", "Answer": "", "Supporting facts": []}
a = []
message = ""
supporting_sentence = ""
supporting_ = False

with open("output_answer.txt", "r", encoding="UTF-8") as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if line == "\n":
            supporting_ = False
            continue
        if "Reference documents" in line and i != 2:
            a.append(data)
            data = {"Reference document": [], "Question": "", "Answer": "", "Supporting facts": []}
            message = ""
        if (
            "Reference documents" not in line
            and "Question" not in line
            and "Answer" not in line
            and "Supporting facts" not in line
            and supporting_ == False
        ):
            data["Reference document"].append(line)

        if "Question" in line:
            data["Question"] = line.split(":", 1)[1].strip()

        if "Answer" in line:
            data["Answer"] = line.split(":", 1)[1].strip()
        if "Supporting facts" in line and supporting_ == False:
            supporting_ = True
            data["Supporting facts"].append(line.split(":", 1)[1].strip())
        if "Supporting facts" not in line and supporting_ == True:
            data["Supporting facts"].append(line)

# 파일 쓰기를 위한 with 문을 별도로 설정
with open("output_extract_supporting_fact.json", "w", encoding="UTF-8") as output_file:
    json.dump(a, output_file, indent=4, ensure_ascii=False)
