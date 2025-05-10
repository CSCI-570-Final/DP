import sys

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

    # Parse base strings and insert indices
    s1 = lines[0]
    s2_start_index = next(i for i in range(1, len(lines)) if set(lines[i]).issubset({'A','C','G','T'}))
    indices1 = list(map(int, lines[1:s2_start_index]))
    s2 = lines[s2_start_index]
    indices2 = list(map(int, lines[s2_start_index+1:]))

    return s1, indices1, s2, indices2

def generate_string(base, indices):
    for index in indices:
        base = base[:index+1] + base + base[index+1:]
    return base

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
    m, n = len(x), len(y)
    # DP 테이블 초기화
    opt = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(m + 1):
        opt[0][i] = i * GAP_PENALTY
    for j in range(n + 1):
        opt[j][0] = j * GAP_PENALTY

    # BOTTOM-UP 계산
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            cost_match = opt[j-1][i-1] + get_alpha(y[j-1], x[i-1])
            cost_gap1  = opt[j-1][i]   + GAP_PENALTY
            cost_gap2  = opt[j][i-1]   + GAP_PENALTY
            opt[j][i] = min(cost_match, cost_gap1, cost_gap2)

    print_opt(opt)

    # TOP-DOWN 추적
    seq1, seq2 = [], []
    i, j = m, n
    while i > 0 and j > 0:
        curr = opt[j][i]
        if curr == opt[j-1][i-1] + get_alpha(y[j-1], x[i-1]):
            seq1.append(x[i-1])
            seq2.append(y[j-1])
            i, j = i-1, j-1
        elif curr == opt[j-1][i] + GAP_PENALTY:
            seq1.append('_')
            seq2.append(y[j-1])
            j -= 1
        else:
            seq1.append(x[i-1])
            seq2.append('_')
            i -= 1

    # 남은 prefix 처리
    while i > 0:
        seq1.append(x[i-1]); seq2.append('_'); i -= 1
    while j > 0:
        seq1.append('_');    seq2.append(y[j-1]); j -= 1

    seq1.reverse()
    seq2.reverse()

    print("Cost of alignment:", opt[n][m])
    print("First string alignment: ", ''.join(seq1))
    print("Second string alignment:", ''.join(seq2))

# ---- main ----
def main():
    if len(sys.argv) != 2:
        print("Usage: python combined_alignment.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    s1, indices1, s2, indices2 = read_input_file(input_file)

    # 생성기 실행
    full_s1 = generate_string(s1, indices1)
    full_s2 = generate_string(s2, indices2)

    print("Generated Strings:")
    print("String 1:", full_s1)
    print("String 2:", full_s2)
    print()

    # 정렬 알고리즘 실행
    dp_sequence_alignment(full_s1, full_s2)

if __name__ == "__main__":
    main()
