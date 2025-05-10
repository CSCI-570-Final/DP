import sys
import psutil
from resource import *
import time
# ---- constants & utils ----
GAP_PENALTY = 30
MISMATCH_COST = {
    'A': {'A': 0, 'C': 110, 'G': 48,  'T': 94},
    'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
    'G': {'A': 48,  'C': 118, 'G': 0, 'T': 110},
    'T': {'A': 94,  'C': 48, 'G': 110, 'T': 0},
}

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

# ---- alignment DP ----
def get_alpha(c1, c2):
    if c1 == '_' or c2 == '_':
        return GAP_PENALTY
    return MISMATCH_COST[c1][c2]

def print_opt(opt):
    # DP 표를 시각화해서 출력 (원점은 왼쪽 아래)
    output = ""
    n = len(opt) - 1
    for a in range(n, -1, -1):
        output += str(opt[a])
        if a > 0:
            output += "\n"
    print(output)

def dp_sequence_alignment(x, y):
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
            cost_match = opt[j-1][i-1] + get_alpha(y[j-1], x[i-1])
            cost_del   = opt[j-1][i]   + GAP_PENALTY
            cost_ins   = opt[j][i-1]   + GAP_PENALTY
            if cost_match <= cost_del and cost_match <= cost_ins:
                opt[j][i] = cost_match
            elif cost_del <= cost_ins:
                opt[j][i] = cost_del
            else:
                opt[j][i] = cost_ins
    seq1 = []
    seq2 = []
    i = m
    j = n
    while i > 0 and j > 0:
        curr = opt[j][i]
        if curr == opt[j-1][i-1] + get_alpha(y[j-1], x[i-1]):
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
    print("Cost of alignment:", cost)
    print("First string alignment: ", aligned_x)
    print("Second string alignment:", aligned_y)

def process_memory():
    proc = psutil.Process()
    return proc.memory_info().rss / 1024.0  # KB 단위, 소수점 포함

def time_wrapper(func, *args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    return (end - start) * 1000.0, result  # ms 단위

# ---- main ----
def main():
    if len(sys.argv) != 2:
        print("Usage: python combined_alignment.py <input_file>")
        sys.exit(1)

    inp = sys.argv[1]
    s1, i1, s2, i2 = read_input_file(inp)
    full_s1 = generate_string(s1, i1)
    full_s2 = generate_string(s2, i2)

    print("Generated Strings:")
    print("String 1:", full_s1)
    print("String 2:", full_s2)
    print()

    # 1) 메모리·시간 측정 시작
    mem_before = process_memory()
    time_ms, _ = time_wrapper(dp_sequence_alignment, full_s1, full_s2)
    mem_after = process_memory()

    # 2) 메모리 사용량 계산
    mem_used = mem_after - mem_before

    print(f"{time_ms:.6f}")
    print(f"{mem_used:.1f}")

if __name__ == "__main__":
    main()
