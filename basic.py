#!/usr/bin/env python3
import sys
import time
import resource
import psutil
from process_input import read_input_file, generate_string, GAP_PENALTY, MISMATCH_COST

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
    # return float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed


# ------------------------------------
# Main: read input, measure, run, output
# ------------------------------------
def main():
    # python3 DP+Time_Efficient.py SampleTestCases/input1.txt Ours/output1_ours.txt
    if len(sys.argv) != 3:
        print("Usage: python3 DP+Time_Efficient.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    s1, idx1, s2, idx2 = read_input_file(input_file)
    x = generate_string(s1, idx1)
    y = generate_string(s2, idx2)

    # 1) 메모리(peak RSS) 측정 함수
    def memory_kb():
        return float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

    # 2) 실행 전 시간·메모리
    mem_before = memory_kb()
    t0 = time.time()

    # 3) 본 함수 호출
    cost, aligned1, aligned2 =dp_sequence_alignment_return(x, y)

    # 4) 실행 후 시간·메모리
    t1 = time.time()
    mem_after = memory_kb()

    # 5) 결과 출력 (원래 출력 뒤에 두 줄)
    time_ms = (t1 - t0) * 1000.0
    # peak RSS 그대로 출력하려면 mem_after,
    # 혹은 차이를 보시려면 mem_after - mem_before
    print(f"{time_ms:.6f}")
    print(f"{mem_after:.6f}")
    
    with open(output_file, 'w') as f:
        f.write(f"{cost}\n")
        f.write(f"{aligned1}\n")
        f.write(f"{aligned2}\n")
        f.write(f"{time_ms:.6f}\n")
        f.write(f"{mem_after - mem_before:.1f}\n")

if __name__ == "__main__":
    main()
