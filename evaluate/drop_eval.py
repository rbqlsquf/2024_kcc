import re
from typing import List, Set
import string
import numpy as np
import json
import nltk
from nltk.stem import PorterStemmer
from collections import Counter
import string
from nltk.tokenize import sent_tokenize

EXCLUDE = set(string.punctuation)


def _compute_f1(predicted_bag, gold_bag):
    intersection = len(gold_bag.intersection(predicted_bag))
    if not predicted_bag:
        precision = 1.0
    else:
        precision = intersection / float(len(predicted_bag))
    if not gold_bag:
        recall = 1.0
    else:
        recall = intersection / float(len(gold_bag))
    f1 = (2 * precision * recall) / (precision + recall) if not (precision == 0.0 and recall == 0.0) else 0.0
    return f1


def _is_number(text: str) -> bool:
    try:
        float(text)
        return True
    except ValueError:
        return False


def _match_numbers_if_present(gold_bag, predicted_bag):
    gold_numbers = set()
    predicted_numbers = set()
    for word in gold_bag:
        if _is_number(word):
            gold_numbers.add(word)
    for word in predicted_bag:
        if _is_number(word):
            predicted_numbers.add(word)
    if (not gold_numbers) or gold_numbers.intersection(predicted_numbers):
        return True
    return False


def _answer_to_bags(answer):
    if isinstance(answer, (list, tuple)):
        raw_spans = answer
    else:
        raw_spans = [answer]
    span_bag = set()
    token_bag = []
    for raw_span in raw_spans:
        span = _normalize_answer(raw_span)
        span_bag.add(span)
        token_bag.append(set(span.split()))
    return span_bag, token_bag


def _remove_articles(text: str) -> str:
    regex = re.compile(r"\b(a|an|the)\b", re.UNICODE)
    return re.sub(regex, " ", text)


def _white_space_fix(text: str) -> str:
    return " ".join(text.split())


def _remove_punc(text: str) -> str:
    if not _is_number(text):
        return "".join(ch for ch in text if ch not in EXCLUDE)
    else:
        return text


def _lower(text: str) -> str:
    return text.lower()


def _tokenize(text: str) -> List[str]:
    return re.split(" |-", text)


def _normalize_number(text: str) -> str:
    if _is_number(text):
        return str(float(text))
    else:
        return text


def _normalize_answer(text: str) -> str:
    """Lower text and remove punctuation, articles and extra whitespace."""

    parts = [
        _white_space_fix(_remove_articles(_normalize_number(_remove_punc(_lower(token))))) for token in _tokenize(text)
    ]
    parts = [part for part in parts if part.strip()]
    normalized = " ".join(parts).strip()
    return normalized


def find_duplicates(index_list):
    value_counts = {}
    duplicates = {}

    # Counting occurrences of each value
    for index, value in enumerate(index_list):
        if value in value_counts:
            value_counts[value].append(index)
        else:
            value_counts[value] = [index]

    # Identifying duplicates and storing their indexes
    for value, indexes in value_counts.items():
        if len(indexes) > 1:
            duplicates[value] = indexes

    return duplicates


def find_max_f1(f1_candidate, max_index_list):
    max_f1_ = []
    for i, f1_list in enumerate(f1_candidate):
        # f1_list는 최대값을 찾으러 가야함
        max_f1_in_list = max(f1_list)
        index_of_max_f1_current = f1_list.index(max_f1_in_list)
        max_index_list[i] = index_of_max_f1_current
        max_f1_.append(max_f1_in_list)

    return f1_candidate, max_index_list, max_f1_


def _align_bags(predicted, gold):
    f1_candidate = []
    for gold_index, gold_item in enumerate(gold):
        max_f1 = 0.0
        f1_current_list = []
        max_index_list = []
        max_index = None
        best_alignment = (set(), set())
        for pred_index, pred_item in enumerate(predicted):
            current_f1 = _compute_f1(pred_item, gold_item)
            best_alignment = (gold_item, pred_item)
            match_flag = _match_numbers_if_present(*best_alignment)
            if match_flag:
                f1_current_list.append(current_f1)
            else:
                f1_current_list.append(0.0)
        f1_candidate.append(f1_current_list)

    # 만약에 f1이 높으면, 인덱스 먼저 비교?
    # max_index_list 안에 겹치는 index 번호가 있으면 찾으러 가야함
    duplicate_index = True
    max_index_list = [0] * len(f1_candidate)

    while 1:

        duplicates = find_duplicates(max_index_list)
        compare_list = []
        for key, values in duplicates.items():
            for j in values:
                compare_list.append(f1_candidate[j][key])

            max_f1_compare = max(compare_list)
            index_of_max_compare = compare_list.index(max_f1_compare)
            for i, j in enumerate(values):
                if index_of_max_compare != i:
                    f1_candidate[j][key] = 0
        f1_candidate, max_index_list, f1_scores = find_max_f1(f1_candidate, max_index_list)
        filtered_list = [x for x in max_index_list if x != 0]
        if len(filtered_list) == len(set(filtered_list)):
            # print(f1_scores)
            break

    return f1_scores


def get_metrics(predicted, gold):
    """
    Takes a predicted answer and a gold answer (that are both either a string or a list of
    strings), and returns exact match and the DROP F1 metric for the prediction.  If you are
    writing a script for evaluating objects in memory (say, the output of predictions during
    validation, or while training), this is the function you want to call, after using
    :func:`answer_json_to_strings` when reading the gold answer from the released data file.
    """
    # answer_to_bags -> 답변 다 담은거 0번째, 1번재는 토큰별로 넣어놓은 거임
    predicted_bags = _answer_to_bags(predicted)
    gold_bags = _answer_to_bags(gold)

    exact_match = 1.0 if predicted_bags[0] == gold_bags[0] else 0

    recall_per_bag = _align_bags(predicted_bags[1], gold_bags[1])

    predicted_bags = _answer_to_bags(predicted)
    gold_bags = _answer_to_bags(gold)
    precision_per_bag = _align_bags(gold_bags[1], predicted_bags[1])

    recall = np.mean(recall_per_bag)
    recall = round(recall, 2)

    precision = np.mean(precision_per_bag)
    precision = round(precision, 2)

    f1 = (recall * precision * 2) / (precision + recall)

    return exact_match, f1


with open("output\experiment1\output_1_clean.json", "r", encoding="UTF8") as f:
    json_data = json.load(f)

with open("output\experiment1\output_f1.txt", "w", encoding="UTF-8") as out_file:
    for data in json_data:
        data_number = data["data_number"]
        real_answer = data["real_answer"]
        gpt_answer = data["gpt_answer"]
        real_support = data["real_support"]
        gpt_support = data["gpt_support"]

        sentences = []
        for sentence in real_support:
            sentences.append(sentence.split("]")[1].strip())

        gold = sentences

        predicted = gpt_support

        em, f1 = get_metrics(predicted, gold)
        out_file.write("number #{} em : {} f1 : {}\n".format(data_number, em, f1))
