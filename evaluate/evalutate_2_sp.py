import sys
import re
import string
from collections import Counter
import pickle
import json


def update_sp(metrics, prediction, gold):
    cur_sp_pred = set(map(tuple, prediction))
    gold_sp_pred = set(map(tuple, gold))
    tp, fp, fn = 0, 0, 0
    for e in cur_sp_pred:
        if e in gold_sp_pred:
            tp += 1
        else:
            fp += 1
    for e in gold_sp_pred:
        if e not in cur_sp_pred:
            fn += 1
    prec = 1.0 * tp / (tp + fp) if tp + fp > 0 else 0.0
    recall = 1.0 * tp / (tp + fn) if tp + fn > 0 else 0.0
    f1 = 2 * prec * recall / (prec + recall) if prec + recall > 0 else 0.0
    em = 1.0 if fp + fn == 0 else 0.0
    metrics["sp_em"] += em
    metrics["sp_f1"] += f1
    metrics["sp_prec"] += prec
    metrics["sp_recall"] += recall
    return em, prec, recall


def eval(file):
    with open(file) as f:
        json_data = json.load(f)

    metrics = {
        "sp_em": 0,
        "sp_f1": 0,
        "sp_prec": 0,
        "sp_recall": 0,
    }

    for data in json_data:
        data_number = data["data_number"]
        real_answer = data["real_answer"]
        gpt_answer = data["gpt_answer"]
        real_support = data["real_support"]
        gpt_support = data["gpt_support"]

        # supporting fact 점수 측정
        sp_em, sp_prec, sp_recall = update_sp(metrics, gpt_support, real_support)

    N = len(json_data)
    for k in metrics.keys():
        metrics[k] /= N

    print(metrics)


if __name__ == "__main__":
    eval("output\experiment2\output_2_clean.json")
