#!/usr/bin/env bash
# efficient.sh: run DP+Time_Efficient.py on all inputs, put outputs in Ours/efficient/

INPUT_DIR="datapoints"
OUTPUT_DIR="Ours/efficient"
SCRIPT="efficient_3.py"

# 출력 폴더 생성
mkdir -p "$OUTPUT_DIR"

for infile in "$INPUT_DIR"/in*.txt; do
  name=$(basename "$infile" .txt)
  outfile="$OUTPUT_DIR/${name}_eff.txt"
  echo "[$(date '+%H:%M:%S')] $infile → $outfile"
  python3 "$SCRIPT" "$infile" "$outfile"
done
