\#!/usr/bin/env bash
set -e

# ------------------------------------

# Paths and Scripts Configuration

# ------------------------------------

BASE\_DIR="\$(cd "\$(dirname "\${BASH\_SOURCE\[0]}")" && pwd)"
BASIC\_SCRIPT="\$BASE\_DIR/basic.py"
EFF\_SCRIPT="\$BASE\_DIR/efficient_3.py"
IN\_DIR="\$BASE\_DIR/datapoints"
OUT\_DIR\_BASIC="\$BASE\_DIR/Ours/basic"
OUT\_DIR\_EFF="\$BASE\_DIR/Ours/efficient"

# ------------------------------------

# Create output directories if needed

# ------------------------------------

mkdir -p "\$OUT\_DIR\_BASIC" "\$OUT\_DIR\_EFF"

# ------------------------------------

# Process each input file

# ------------------------------------

for infile in "\$IN\_DIR"/*; do
filename=\$(basename "\$infile")
base="\${filename%.*}"

```
echo "[INFO] Processing input: $filename"

# Basic DP output
python3 "$BASIC_SCRIPT" "$infile" "$OUT_DIR_BASIC/${base}_basic.out"

# Memory-efficient DP output
python3 "$EFF_SCRIPT" "$infile" "$OUT_DIR_EFF/${base}_eff.out"
```

done

echo "\[INFO] All files processed. Outputs in:"
echo "  - Basic: \$OUT\_DIR\_BASIC"
echo "  - Efficient: \$OUT\_DIR\_EFF"