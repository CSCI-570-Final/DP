#!/usr/bin/env python3
import sys
import time
import psutil
from resource import *
# ------------------------------------
# Constants
# ------------------------------------
GAP_PENALTY = 30
MISMATCH_COST = {
    'A': {'A': 0,   'C': 110, 'G': 48,  'T': 94},
    'C': {'A': 110, 'C': 0,   'G': 118, 'T': 48},
    'G': {'A': 48,  'C': 118, 'G': 0,   'T': 110},
    'T': {'A': 94,  'C': 48,  'G': 110, 'T': 0},
}

# ------------------------------------
# Input processing
# ------------------------------------

def read_input_file(filepath):
    f = open(filepath, 'r')
    lines = []
    for line in f:
        text = line.strip()
        if text != "":
            lines.append(text)
    f.close()
    s1 = lines[0]
    s2_start = 0
    for i in range(1, len(lines)):
        ok = True
        for ch in lines[i]:
            if ch not in ['A','C','G','T']:
                ok = False
                break
        if ok:
            s2_start = i
            break
    idx1 = []
    for k in range(1, s2_start):
        num = int(lines[k])
        idx1.append(num)
    s2 = lines[s2_start]
    idx2 = []
    for k in range(s2_start + 1, len(lines)):
        num = int(lines[k])
        idx2.append(num)
    return s1, idx1, s2, idx2

def generate_string(base, indices):
    result = base
    for idx in indices:
        part1 = result[:idx+1]
        part2 = result[idx+1:]
        result = part1 + result + part2
    return result

# ------------------------------------
# Cost function
# ------------------------------------
def get_alpha(c1, c2):
    if c1 == '_' or c2 == '_':
        return GAP_PENALTY
    return MISMATCH_COST[c1][c2]

# ------------------------------------
# Full DP (basic)
# ------------------------------------
def dp_sequence_alignment_return(x, y):
    m = len(x)
    n = len(y)
    opt = []
    for _ in range(n + 1):
        row = []
        for _ in range(m + 1):
            row.append(0)
        opt.append(row)
    for i in range(m + 1):
        opt[0][i] = i * GAP_PENALTY
    for j in range(n + 1):
        opt[j][0] = j * GAP_PENALTY
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            match_cost  = opt[j-1][i-1] + get_alpha(x[i-1], y[j-1])
            delete_cost = opt[j-1][i]   + GAP_PENALTY
            insert_cost = opt[j][i-1]   + GAP_PENALTY
            if match_cost <= delete_cost and match_cost <= insert_cost:
                opt[j][i] = match_cost
            elif delete_cost <= insert_cost:
                opt[j][i] = delete_cost
            else:
                opt[j][i] = insert_cost
    seq1 = []
    seq2 = []
    i = m
    j = n
    while i > 0 and j > 0:
        curr = opt[j][i]
        if curr == opt[j-1][i-1] + get_alpha(x[i-1], y[j-1]):
            seq1.append(x[i-1])
            seq2.append(y[j-1])
            i = i - 1
            j = j - 1
        elif curr == opt[j-1][i] + GAP_PENALTY:
            seq1.append('_')
            seq2.append(y[j-1])
            j = j - 1
        else:
            seq1.append(x[i-1])
            seq2.append('_')
            i = i - 1
    while i > 0:
        seq1.append(x[i-1])
        seq2.append('_')
        i = i - 1
    while j > 0:
        seq1.append('_')
        seq2.append(y[j-1])
        j = j - 1
    seq1.reverse()
    seq2.reverse()
    cost = opt[n][m]
    aligned_x = ''
    for c in seq1:
        aligned_x = aligned_x + c
    aligned_y = ''
    for c in seq2:
        aligned_y = aligned_y + c
    return cost, aligned_x, aligned_y


# ------------------------------------
# Linear-space cost (helper for Hirschberg)
# ------------------------------------
def cost_linear(x, y):
    m = len(x)
    prev = []
    for i in range(m + 1):
        cost = i * GAP_PENALTY
        prev.append(cost)
    curr = []
    for i in range(m + 1):
        curr.append(0)
    for j in range(1, len(y) + 1):
        curr[0] = j * GAP_PENALTY
        for i in range(1, m + 1):
            match_cost  = prev[i-1] + get_alpha(x[i-1], y[j-1])
            delete_cost = prev[i]   + GAP_PENALTY
            insert_cost = curr[i-1] + GAP_PENALTY
            if match_cost <= delete_cost and match_cost <= insert_cost:
                curr[i] = match_cost
            elif delete_cost <= insert_cost:
                curr[i] = delete_cost
            else:
                curr[i] = insert_cost
        new_prev = []
        for value in curr:
            new_prev.append(value)
        prev = new_prev
        curr = []
        for i in range(m + 1):
            curr.append(0)
    return prev


# ------------------------------------
# Hirschberg’s algorithm (memory-efficient)
# ------------------------------------
def hirschberg(x, y):
    m = len(x)
    n = len(y)
    if m == 0:
        seq1 = ''
        for _ in range(n):
            seq1 = seq1 + '_'
        seq2 = ''
        for ch in y:
            seq2 = seq2 + ch
        cost1 = n * GAP_PENALTY
        return seq1, seq2, cost1
    if n == 0:
        seq1 = ''
        for ch in x:
            seq1 = seq1 + ch
        seq2 = ''
        for _ in range(m):
            seq2 = seq2 + '_'
        cost2 = m * GAP_PENALTY
        return seq1, seq2, cost2
    if m == 1 or n == 1:
        cost3, sx, sy = dp_sequence_alignment_return(x, y)
        return sx, sy, cost3

    mid = n // 2
    y_left = ''
    for j in range(mid):
        y_left = y_left + y[j]
    y_right = ''
    for j in range(mid, n):
        y_right = y_right + y[j]

    rev_x = ''
    for i in range(m-1, -1, -1):
        rev_x = rev_x + x[i]
    rev_y_right = ''
    for j in range(len(y_right)-1, -1, -1):
        rev_y_right = rev_y_right + y_right[j]

    left_cost = cost_linear(x, y_left)
    right_cost_rev = cost_linear(rev_x, rev_y_right)

    right_cost = []
    for k in range(len(right_cost_rev)-1, -1, -1):
        right_cost.append(right_cost_rev[k])

    best_i = 0
    min_sum = left_cost[0] + right_cost[0]
    for i in range(1, m+1):
        sum_cost = left_cost[i] + right_cost[i]
        if sum_cost < min_sum:
            min_sum = sum_cost
            best_i = i
    split = best_i

    left_x = ''
    for i in range(split):
        left_x = left_x + x[i]
    left_y = ''
    for j in range(mid):
        left_y = left_y + y[j]
    right_x = ''
    for i in range(split, m):
        right_x = right_x + x[i]
    right_y = ''
    for j in range(mid, n):
        right_y = right_y + y[j]

    lx, ly, lc = hirschberg(left_x, left_y)
    rx, ry, rc = hirschberg(right_x, right_y)

    seq1 = lx + rx
    seq2 = ly + ry
    total_cost = lc + rc
    return seq1, seq2, total_cost


# ------------------------------------
# Process-memory & Time-wrapper (from sample)
# ------------------------------------
def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed

def time_wrapper(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time   = time.time()
    time_taken = (end_time - start_time) * 1000
    return time_taken, result

# ------------------------------------
# Main entry point
# ------------------------------------
def main():
    if len(sys.argv) != 3:
        print("Usage: python3 combined_alignment.py <input> <output>")
        sys.exit(1)

    inp, outp = sys.argv[1], sys.argv[2]
    s1, i1, s2, i2 = read_input_file(inp)
    x = generate_string(s1, i1)
    y = generate_string(s2, i2)

    mem_before = process_memory()
    time_ms, (aligned1, aligned2, cost) = time_wrapper(hirschberg, x, y)
    mem_after  = process_memory()
    mem_used   = mem_after - mem_before

    # stdout: 시간, 메모리 차이
    print(f"{time_ms:.6f}")
    print(f"{mem_used:.1f}")

    # output file: cost, seq1, seq2, time, memory
    with open(outp, 'w') as f:
        f.write(f"{cost}\n")
        f.write(f"{aligned1}\n")
        f.write(f"{aligned2}\n")
        f.write(f"{time_ms:.6f}\n")
        f.write(f"{mem_used:.1f}\n")

if __name__ == '__main__':
    main()
