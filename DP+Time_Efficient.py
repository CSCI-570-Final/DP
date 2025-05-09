#!/usr/bin/env python3
import sys
import time
import resource
from process_input import read_input_file, generate_string, GAP_PENALTY, MISMATCH_COST

def get_alpha(c1, c2):
    return MISMATCH_COST[c1][c2]

def dp_sequence_alignment(x, y):
    m = len(x)
    n = len(y)
    gap_penalty = 30

    # create DP table and fill base cases
    opt = [[0] * (m + 1) for k in range(n + 1)]

    for i in range(m + 1):
        opt[0][i] = i * gap_penalty
    for i in range(n + 1):
        opt[i][0] = i * gap_penalty
    # print_opt(opt)

    # BOTTOM-UP PASS
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            cost_match = opt[j - 1][i - 1] + get_alpha(y[j - 1], x[i - 1])
            cost_gap1 = opt[j - 1][i] + gap_penalty
            cost_gap2 = opt[j][i - 1] + gap_penalty
            opt[j][i] = min(cost_match, cost_gap1, cost_gap2)
    print_opt(opt)

    # TOP-DOWN PASS
    seq1 = []
    seq2 = []
    i = m
    j = n

    while i > 0 and j > 0:
        curr = opt[j][i]
        if curr == opt[j - 1][i - 1] + get_alpha(y[j - 1], x[i - 1]):
            seq1.append(x[i - 1])
            seq2.append(y[j - 1])
            i -= 1
            j -= 1

        # gap 1
        elif curr == opt[j - 1][i] + gap_penalty:
            seq1.append('_')
            seq2.append(y[j - 1])
            j -= 1

        # gap 2
        else:
            seq1.append(x[i - 1])
            seq2.append('_')
            i -= 1

    # if either sequence not yet completed, fill rest with spaces
    while i > 0:
        seq1.append(x[i - 1])
        seq2.append('_')
        i -= 1

    while j > 0:
        seq1.append('_')
        seq2.append(y[j - 1])
        j -= 1

    # started from end of sequences; need to reverse
    seq1.reverse()
    seq2.reverse()

    print("Cost of alignment: ", opt[n][m],
          "\nFirst string alignment: ", ''.join(seq1),
          "\nSecond string alignment: ", ''.join(seq2))
    


def print_opt(opt):
    # print input dp table, opt, to help visualization
    # horizontal axis is first string, x, and vertical axis is y
    # origin is bottom left-most element
    output = ""
    n = len(opt) - 1
    for a in range(n, -1, -1):
        output += str(opt[a])
        if a > 0:
            output += "\n"
    print(output)


def get_alpha(j, i):
    idx1, idx2 = -1, -1
    alpha_matrix = [[0, 110, 48, 94],
                    [110, 0, 118, 48],
                    [48, 118, 0, 110],
                    [94, 48, 110, 0]]

    # !!! NEED TO ADD CASE FOR _ CHARACTERS !!!
    match j:
        case 'A':
            idx1 = 0
        case 'C':
            idx1 = 1
        case 'G':
            idx1 = 2
        case 'T':
            idx1 = 3

    match i:
        case 'A':
            idx2 = 0
        case 'C':
            idx2 = 1
        case 'G':
            idx2 = 2
        case 'T':
            idx2 = 3
    return alpha_matrix[idx1][idx2]


# ------------------------------------
# 여기부터 추가된 부분
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
    dp_sequence_alignment(x, y)

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
        # f.write(f"{cost}\n")
        # f.write(f"{aligned1}\n")
        # f.write(f"{aligned2}\n")
        f.write(f"{time_ms:.6f}\n")
        f.write(f"{mem_after:.1f}\n")

if __name__ == "__main__":
    main()