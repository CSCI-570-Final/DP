#!/usr/bin/env python3
import sys
import time
import resource

# ------------------------------------
# Constants
# ------------------------------------
GAP_PENALTY = 30

# ------------------------------------
# get_alpha: substitution/gap cost
# ------------------------------------
def get_alpha(c1, c2):
    if c1 == '_' or c2 == '_':
        return GAP_PENALTY
    mp = {'A':0, 'C':1, 'G':2, 'T':3}
    alpha = [
        [  0, 110,  48,  94],
        [110,   0, 118,  48],
        [ 48, 118,   0, 110],
        [ 94,  48, 110,   0]
    ]
    return alpha[mp[c1]][mp[c2]]

# ------------------------------------
# dp_sequence_alignment_return:
# full DP, returns (cost, aligned_x, aligned_y)
# ------------------------------------
def dp_sequence_alignment_return(x, y):
    m, n = len(x), len(y)
    opt = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(m + 1):
        opt[0][i] = i * GAP_PENALTY
    for j in range(n + 1):
        opt[j][0] = j * GAP_PENALTY

    for j in range(1, n + 1):
        for i in range(1, m + 1):
            c_match = opt[j-1][i-1] + get_alpha(x[i-1], y[j-1])
            c_del   = opt[j-1][i]   + GAP_PENALTY
            c_ins   = opt[j][i-1]   + GAP_PENALTY
            opt[j][i] = min(c_match, c_del, c_ins)

    # traceback
    seq1, seq2 = [], []
    i, j = m, n
    while i > 0 and j > 0:
        curr = opt[j][i]
        if curr == opt[j-1][i-1] + get_alpha(x[i-1], y[j-1]):
            seq1.append(x[i-1]); seq2.append(y[j-1])
            i -= 1; j -= 1
        elif curr == opt[j-1][i] + GAP_PENALTY:
            seq1.append('_'); seq2.append(y[j-1]); j -= 1
        else:
            seq1.append(x[i-1]); seq2.append('_'); i -= 1

    while i > 0:
        seq1.append(x[i-1]); seq2.append('_'); i -= 1
    while j > 0:
        seq1.append('_'); seq2.append(y[j-1]); j -= 1

    seq1.reverse(); seq2.reverse()
    return opt[n][m], ''.join(seq1), ''.join(seq2)

# ------------------------------------
# memory_kb: peak RSS in KB
# ------------------------------------
def memory_kb():
    return float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

# ------------------------------------
# Main: read input, measure, run, output
# ------------------------------------
if __name__ == '__main__':
    # read from file if provided
    if len(sys.argv) >= 3:
        in_path, out_path = sys.argv[1], sys.argv[2]
        with open(in_path) as f:
            x = f.readline().strip()
            y = f.readline().strip()
    else:
        x = "ACACTGACTACTGACTGGTGACTACTGACTGG"
        y = "TATTATACGCTATTATACGCGACGCGGACGCG"
        out_path = None

    t0 = time.time()
    # call DP
    cost, aligned_x, aligned_y = dp_sequence_alignment_return(x, y)
    t1 = time.time()

    mem_kb = memory_kb()
    time_ms = (t1 - t0) * 1000.0

    # print exactly 5 lines: cost, align1, align2, time, memory
    output = '\n'.join([
        str(cost),
        aligned_x,
        aligned_y,
        f"{time_ms:.6f}",
        f"{mem_kb:.6f}"
    ])

    if out_path:
        with open(out_path, 'w') as f:
            f.write(output)
    else:
        print(output)
