# Group Analysis Script

The `analyze_group.py` script analyzes the impact of variable groups by comparing responses with and without specific variable groups.

## Features

1. **Reads response files** from `responses_full_group_X.csv` and `responses_without_group_X.csv`
2. **Generates embeddings** using three different models (384, 768, and 1024 dimensions)
3. **Calculates metrics**: Euclidean distance, Cosine similarity, and Pearson correlation
4. **Saves results** to both screen and file
5. **Organized output** with embeddings saved in binary format and results in text files

## Usage

### Basic Usage

```bash
# Analyze a specific group (e.g., group K)
python analyze_group.py --group K
```

### Options

```bash
# Regenerate embeddings even if they exist
python analyze_group.py --group K --regenerate

# Process only one specific dimension
python analyze_group.py --group K --model dim_768

# Specify custom directories
python analyze_group.py --group K --responses-dir /path/to/responses --output-dir /path/to/output
```

## Output Structure

The script creates the following directory structure:

```
outputs/
├── embeddings/
│   ├── dimension_384/
│   │   ├── full_group_K.bin
│   │   └── without_group_K.bin
│   ├── dimension_768/
│   │   ├── full_group_K.bin
│   │   └── without_group_K.bin
│   └── dimension_1024/
│       ├── full_group_K.bin
│       └── without_group_K.bin
└── results/
    └── group_K_analysis.txt
```

## Metrics Calculated

For each dimension, the script calculates:

1. **Euclidean Distance**: Measures the straight-line distance between embeddings
   - Mean, standard deviation, min, max

2. **Cosine Similarity**: Measures the cosine of the angle between embeddings (0-1 scale)
   - Mean, standard deviation, min, max

3. **Pearson Correlation**: Measures linear correlation between embeddings (-1 to 1 scale)
   - Mean, standard deviation, min, max

## Models Used

- **dim_384**: `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions)
- **dim_768**: `sentence-transformers/all-mpnet-base-v2` (768 dimensions)
- **dim_1024**: `sentence-transformers/all-roberta-large-v1` (1024 dimensions)

## Requirements

Install dependencies:
```bash
pip install -r requirements.txt
```

The script requires:
- sentence-transformers
- numpy
- scipy
- scikit-learn
- torch
- transformers

## Notes

- Embeddings are cached in binary format for faster subsequent runs
- Use `--regenerate` to force regeneration of embeddings
- The script automatically matches IDs between full and without group responses
- Results are printed to screen and saved to `outputs/results/group_X_analysis.txt`
