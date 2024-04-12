f1_candidate = [[0.7, 0.3, 0.1], [0.9, 0.6, 0.1], [0.3, 0.1, 0.3], [0.5, 0.3, 0.2]]

duplicate_index = True


def find_max_f1(f1_candidate, max_index_list):
    max_f1_ = []
    for i, f1_list in enumerate(f1_candidate):
        # f1_list는 최대값을 찾으러 가야함
        max_f1_in_list = max(f1_list)
        index_of_max_f1_current = f1_list.index(max_f1_in_list)
        max_index_list[i] = index_of_max_f1_current
        max_f1_.append(max_f1_in_list)

    return f1_candidate, max_index_list, max_f1_


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
        print(f1_scores)
        break
