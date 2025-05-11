import sys
import psutil
from resource import getrusage, RUSAGE_SELF
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
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    s1 = lines[0]
    s2_start = 0
    for i in range(1, len(lines)):
        if all(ch in 'ACGT' for ch in lines[i]):
            s2_start = i
            break
    idx1 = [int(x) for x in lines[1:s2_start]]
    s2 = lines[s2_start]
    idx2 = [int(x) for x in lines[s2_start+1:]]
    return s1, idx1, s2, idx2


def generate_string(base, indices):
    result = base
    for idx in indices:
        result = result[:idx+1] + result + result[idx+1:]
    return result


def get_alpha(c1, c2):
    if c1 == '_' or c2 == '_':
        return GAP_PENALTY
    return MISMATCH_COST[c1][c2]


def align_sequences(x, y):
    m, n = len(x), len(y)
    opt = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(m + 1):
        opt[0][i] = i * GAP_PENALTY
    for j in range(n + 1):
        opt[j][0] = j * GAP_PENALTY

    for j in range(1, n + 1):
        for i in range(1, m + 1):
            cost_match = opt[j-1][i-1] + get_alpha(y[j-1], x[i-1])
            cost_del   = opt[j-1][i]   + GAP_PENALTY
            cost_ins   = opt[j][i-1]   + GAP_PENALTY
            opt[j][i] = min(cost_match, cost_del, cost_ins)

    seq1, seq2 = [], []
    i, j = m, n
    while i > 0 and j > 0:
        curr = opt[j][i]
        if curr == opt[j-1][i-1] + get_alpha(y[j-1], x[i-1]):
            seq1.append(x[i-1]); seq2.append(y[j-1]); i -= 1; j -= 1
        elif curr == opt[j-1][i] + GAP_PENALTY:
            seq1.append('_'); seq2.append(y[j-1]); j -= 1
        else:
            seq1.append(x[i-1]); seq2.append('_'); i -= 1
    while i > 0:
        seq1.append(x[i-1]); seq2.append('_'); i -= 1
    while j > 0:
        seq1.append('_'); seq2.append(y[j-1]); j -= 1
    return opt[n][m], ''.join(reversed(seq1)), ''.join(reversed(seq2))


def process_memory():
    proc = psutil.Process()
    return proc.memory_info().rss / 1024.0  # KB 단위, 소수점 포함


def time_wrapper(func, *args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    return (end - start) * 1000.0, result  # ms 단위

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python basic.py <input_file> <output_file>")
        sys.exit(1)

    infile, outfile = sys.argv[1], sys.argv[2]
    s1, i1, s2, i2 = read_input_file(infile)
    full_s1 = generate_string(s1, i1)
    full_s2 = generate_string(s2, i2)

    mem_before = process_memory()
    time_ms, (cost, aligned_x, aligned_y) = time_wrapper(align_sequences, full_s1, full_s2)
    mem_after = process_memory()
    mem_used = mem_after - mem_before

    with open(outfile, 'w') as f:
        f.write(f"{cost}\n")
        f.write(aligned_x + "\n")
        f.write(aligned_y + "\n")
        f.write(f"{time_ms:.6f}\n")
        f.write(f"{mem_used:.1f}\n")
