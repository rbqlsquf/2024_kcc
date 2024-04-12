import json
import re
import string
from collections import Counter


def preprocess_sentence(sentence):
    # Remove punctuation
    sentence = sentence.translate(str.maketrans("", "", string.punctuation))
    # Convert to lowercase
    sentence = sentence.lower()
    # Split into words
    words = sentence.split()
    return words


def calculate_similarity_score(correct_answer, guessed_answer):
    # Preprocess sentences
    correct_words = preprocess_sentence(correct_answer)
    guessed_words = preprocess_sentence(guessed_answer)

    # Count words in each sentence
    correct_word_count = Counter(correct_words)
    guessed_word_count = Counter(guessed_words)

    # Calculate the sum of minimum counts for shared words
    shared_words = set(correct_words) & set(guessed_words)
    score = sum(min(correct_word_count[word], guessed_word_count[word]) for word in shared_words)

    # Normalize the score by the total number of words in the correct answer
    # to get a fractional similarity measure
    if len(correct_words) == 0:
        return 0  # Avoid division by zero
    normalized_score = score / len(correct_words)

    return normalized_score


with open("output\experiment1\output_1_clean.json", "r", encoding="UTF8") as f:
    json_data = json.load(f)


support_score = 0
support_score_a = 0
support_score_b = 0
support_score_c = 0
total_similarity_score = 0

with open("output_similarity.txt", "w", encoding="UTF-8") as out_file:
    for data in json_data:
        data_number = data["data_number"]
        real_answer = data["real_answer"]
        gpt_answer = data["gpt_answer"]
        real_support = data["real_support"]
        gpt_support = data["gpt_support"]
        similarity_score = calculate_similarity_score(real_answer, gpt_answer)
        # print(f"Similarity Score: {similarity_score}")
        out_file.write("{} : {}\n".format(data_number, similarity_score))
        total_similarity_score += similarity_score
        set_real_support = set(real_support)
        set_gpt_support = set(gpt_support)

        if set_real_support == set_gpt_support:
            support_score += 1
        if set_real_support.issubset(set_gpt_support):
            support_score_a += 1
        if set_gpt_support.issubset(set_real_support):
            support_score_b += 1
        if set_gpt_support.isdisjoint(set_real_support):
            support_score_c += 1
            print(data_number)

    total_similarity_score = total_similarity_score / 100
    out_file.write("total_similarity_score : {}\n".format(total_similarity_score))


print(total_similarity_score)
print(support_score)
print(support_score_a)
print(support_score_b)
print(support_score_c)
