import json
from tqdm import tqdm

## 대용량 json 파일 불러와 로드
with open("data\hotpot_train_v1.1.json", "r") as f:
    json_data = json.load(f)

# 길이가 짧은 document만 담을 list
sample_number = []

# 모든 데이터의 document 길이를 담을 list
context_size = 0  # 전체 문장 길이를 세기 위한 변수
context_dic = {}

# json_data 자체가 데이터 하나임, 문서는 10개씩 있으니까 context_size 계산할 때 문서 10개 for 문 j가 있는 곳을 10번 돌아야함
for i, data in tqdm(enumerate(json_data)):
    context = data["context"]
    if len(context) != 10:
        continue
    context_size = 0  # 초기화
    for j in context:
        context_size += len(j[0])  # 제목의 character 수 넣기
        for sent in j[1]:
            context_size += len(sent)
    context_dic[i] = context_size

# 딕셔너리를 구성하고 나서 이제 context_dic 의 value 값을 기준으로 정렬을 진행
sorted_items = sorted(context_dic.items(), key=lambda item: item[1])

# Convert the sorted items back into a dictionary
sorted_dict = dict(sorted_items)
selected_data = []
for i, j in enumerate(sorted_dict.keys()):
    if i > 99:
        selected_data.append(json_data[j])
    if i > 200:
        break


## json 파일 정렬해서 a에 저장
a = json.dumps(selected_data, indent=2)

## 새로운 파일을 생성, 열어서 a를 write
with open("data/new_hotpot_2.json", "w") as file:
    file.write(a)

## 완료시 출력
print("finish------------")
