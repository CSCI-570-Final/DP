import sys

# sequence_alignment_utils.py
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


def main():
    if len(sys.argv) != 2:
        print("Usage: python process_input.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    s1, indices1, s2, indices2 = read_input_file(input_file)

    # Generate the full strings
    full_s1 = generate_string(s1, indices1)
    full_s2 = generate_string(s2, indices2)

    print("Generated Strings:")
    print("String 1:", full_s1)
    print("String 2:", full_s2)

if __name__ == "__main__":
        main()   