

INPUT_DIR="datapoints"
OUTPUT_DIR="efficient"
SCRIPT="efficient_3.py"

mkdir -p "$OUTPUT_DIR"

for infile in "$INPUT_DIR"/in*.txt; do
  base=$(basename "$infile" .txt)
  num=${base#in}
  outfile="$OUTPUT_DIR/output${num}_efficient.txt"

  echo "[$(date '+%H:%M:%S')] $infile → $outfile"
  python3 "$SCRIPT" "$infile" "$outfile"
done
