def sort_for_sim(ans_positive: list) -> list:
    i, j = 0, len(ans_positive) - 1
    reordered_ans_positive = []
    while i <= j:
        if i == j:
            reordered_ans_positive.append(ans_positive[i])  # 当i和j相等时，只需添加一次
        else:
            reordered_ans_positive.append(ans_positive[i])
            reordered_ans_positive.append(ans_positive[j])
        i += 1
        j -= 1
    return reordered_ans_positive