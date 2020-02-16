from pprint import pprint
def lcs(a, b):
    # generate matrix of length of longest common subsequence for substrings of both words
    lengths = [[0] * (len(b)+1) for _ in range(len(a)+1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                lengths[i+1][j+1] = lengths[i][j] + 1
            else:
                lengths[i+1][j+1] = max(lengths[i+1][j], lengths[i][j+1])
 
    # read a substring from the matrix
    result = ''
    triplets = []
    # format (a seq, b seq, is_match=bool)
    j = len(b)
    g = len(a)
    last_match_a = -1
    last_match_b = 0
    for i in range(1, len(a)+1):
        if lengths[i][j] != lengths[i-1][j]:
            result += a[i-1]
            matched_b_index = None
            for k in range(len(b) - 1, 0, -1):
                # print(i, k, lengths[i][k], lengths[i][k-1])
                if lengths[i][k] != lengths[i][k-1]:
                    matched_b_index = k
                    break
            if matched_b_index is None:
                print("wtf", a, b)
                matched_b_index = j
                
                # pprint(lengths)
                # print(i, j)
            unmatched_a = a[last_match_a + 1:i-1]
            unmatched_b = b[last_match_b:matched_b_index-1]
            if len(unmatched_a + unmatched_b) > 0:
                triplets.append((
                    unmatched_a,
                    unmatched_b,
                    False
                ))
            triplets.append((a[i-1], a[i-1], True))
            last_match_a = i-1
            last_match_b = matched_b_index
    last_triplet = [a[last_match_a + 1:], [], False]
    if len(triplets) > 0:
        last_matched_b_word = triplets[-1][1]
        for k in range(len(b) - 1, 0, -1):
            if b[k] == last_matched_b_word:
                last_triplet[1] = b[k+1:]
                break
    else:
        last_triplet[1] = b

    if len(last_triplet[0]) + len(last_triplet[1]) > 0:
        triplets.append(tuple(last_triplet))

    # pprint(triplets)
 
    return result, triplets