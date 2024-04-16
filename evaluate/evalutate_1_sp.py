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
import pandas as pd

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


def _align_bags(predicted, gold):
    f1_candidate = []
    for gold_index, gold_item in enumerate(gold):
        f1_current_list = []
        for pred_index, pred_item in enumerate(predicted):
            current_f1 = _compute_f1(pred_item, gold_item)
            f1_current_list.append(current_f1)
        f1_candidate.append(f1_current_list)

    # 만약에 f1이 높으면, 인덱스 먼저 비교?
    # max_index_list 안에 겹치는 index 번호가 있으면 찾으러 가야함

    df = pd.DataFrame(f1_candidate)

    couple = []

    while df.columns.tolist() and df.index.tolist():
        col_nm = df.columns[0]
        col_max_idx = df[col_nm].tolist().index(max(df[col_nm].tolist()))
        row_nm = df.index[col_max_idx]

        if df.loc[row_nm][col_nm] == max(df.loc[row_nm].tolist()):
            couple.append((row_nm, col_nm))
            df.drop([row_nm], axis=0, inplace=True)
            df.drop([col_nm], axis=1, inplace=True)
        else:
            new_col_nm = df.columns[df.loc[row_nm].tolist().index(max(df.loc[row_nm].tolist()))]
            couple.append((row_nm, new_col_nm))
            df.drop([row_nm], axis=0, inplace=True)
            df.drop([new_col_nm], axis=1, inplace=True)

    f1_score = [0] * len(f1_candidate)

    for i, j in couple:
        f1_score[i] = f1_candidate[i][j]

    return f1_score


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

    return exact_match, f1, recall, precision


with open("output/experiment_few_shot/2-shot/output_instruction_clean.json", "r", encoding="UTF8") as f:
    json_data = json.load(f)

total_f1 = 0.0
total_recall = 0.0
total_precision = 0.0
with open("output/experiment_few_shot/2-shot/output_f1.txt", "w", encoding="UTF-8") as out_file:
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

        em, f1, recall, precision = get_metrics(predicted, gold)
        out_file.write("number #{} em : {} f1 : {}\n".format(data_number, em, f1))
        total_f1 += f1
        total_recall += recall
        total_precision += precision
    total_f1 = total_f1 / 100
    total_recall = total_recall / 100
    total_precision = total_precision / 100
    out_file.write(
        "\n\n\ntotal_f1 : {}\ntotal_recall : {}\ntotal_precision : {}".format(total_f1, total_recall, total_precision)
    )

    print(total_f1)
    print(total_recall)
    print(total_precision)
