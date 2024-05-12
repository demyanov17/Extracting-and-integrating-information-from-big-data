def jaro_similarity(s1, s2):

    s1_len = len(s1)
    s2_len = len(s2)
    s1_matches, s2_matches = [False] * s1_len, [False] * s2_len

    max_dist = max(s1_len, s2_len) // 2 - 1
    match_count = 0

    for i in range(s1_len):
        start = max(0, i - max_dist)
        end = min(i + max_dist + 1, s2_len)

        for j in range(start, end):
            if not s2_matches[j] and s1[i] == s2[j]:
                s1_matches[i] = s2_matches[j] = True
                match_count += 1
                break

    if match_count == 0:
        return 0.0

    transpositions, k = 0, 0

    for i in range(s1_len):
        if s1_matches[i]:
            while not s2_matches[k]:
                k += 1
            if s1[i] != s2[k]:
                transpositions += 1
            k += 1

    return (
        match_count / s1_len
        + match_count / s2_len
        + (match_count - transpositions / 2) / match_count
    ) / 3


def jaro_winkler_similarity(s1, s2, p=0.1):

    jaro_sim = jaro_similarity(s1, s2)

    prefix_len = 0
    min_len = min(len(s1), len(s2))
    for i in range(min_len):
        if s1[i] == s2[i]:
            prefix_len += 1
        else:
            break

    return jaro_sim + (prefix_len * p * (1 - jaro_sim))
