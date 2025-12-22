# Experiment 1: Persona Pattern Variability Analysis

This folder contains the analysis scripts for investigating the impact of persona patterns on GPT-4o annotation behavior. The experiment consists of two main analyses that examine different aspects of persona conditioning.

## Dataset Overview

The dataset corresponds to 12 iterations (from iteration_3 to iteration_14), where each iteration has 100 reviews, except for the last one. In each iteration, 3 humans participated, while the LLMs participated in all of them.

### Files Structure

- **`persona-pattern_Ann_X.json`**: JSON files with the personas we generated (Ann_1 → Ann_5)
- **`iteration-persona.xlsx`**: Contains the relationship between personas (Ann_X) and the iterations in which they participated
- **`Ann_X.xlsx`**: Contains the reviews annotated by persona Ann_X (human annotations)
- **`gpt-4o-Y-annotations.xlsx`**: Contains the reviews annotated by GPT-4o without a persona pattern (3 different executions: gpt-4o-1, gpt-4o-2, gpt-4o-3)
- **`gpt-4o-Ann_X-annotations.xlsx`**: Contains the reviews annotated by GPT-4o applying the persona pattern of persona Ann_X

### Data Format

Each Excel file contains rows representing sentence-level annotations with the following structure:
- **`reviewId`**: Unique identifier for each review
- **`sentenceId`**: Identifier for sentences within a review
- **Emotion columns**: `Joy`, `Trust`, `Fear`, `Surprise`, `Sadness`, `Disgust`, `Anger`, `Anticipation`, `Neutral`, `Reject` (binary 0/1 values)
- Other metadata: `iteration`, `app_name`, `categoryId`, `review`, `sentence`, etc.

**Note**: Some reviews have multiple sentences (rows with the same `reviewId`). The scripts group by `reviewId` and skip reviews with duplicate IDs to ensure one annotation per review.

## Experiment 1: Global Variability Analysis

### Purpose

This experiment investigates whether applying different persona patterns has a real impact on the variability of the LLM's behavior. It compares the variability among GPT-4o annotations with and without persona patterns.

### Scripts

1. **`global_variability.py`**: Compares variability among all 3 without-persona files vs all 5 with-persona files
2. **`global_variability_combinations.py`**: Compares variability among 3 without-persona files vs all possible combinations of 3 personas from 5 available personas (C(5,3) = 10 combinations)

### Methodology

#### Data Processing

1. **Load annotations**: Each Excel file is loaded and processed
2. **Extract by reviewId**: For each `reviewId`, all emotions from all sentences in that review are collected into a single set
3. **Skip duplicates**: Reviews with multiple rows (same `reviewId` appearing multiple times) are skipped to ensure one annotation per review
4. **Find common reviews**: Only `reviewId`s that exist in all files being compared are used

#### Variability Calculation

For each group of files (e.g., 3 without-persona files or a combination of 3 with-persona files):

1. **Find common reviewIds**: Intersect all `reviewId`s across all files in the group
2. **Calculate pairwise similarities**: For each common `reviewId`, calculate Jaccard similarity between all pairs of files
3. **Compute statistics**: 
   - Mean Jaccard similarity
   - Standard deviation
   - Min/Max values
   - Variability = 1 - mean similarity (lower similarity = higher variability)

#### Jaccard Similarity

Jaccard similarity measures agreement between two sets of emotion labels:
```
Jaccard(A, B) = |A ∩ B| / |A ∪ B|
```

Where A and B are sets of emotion labels (e.g., {Joy, Trust, Neutral}).

### Running the Analysis

```bash
# Basic global variability (all 5 personas vs 3 without-persona)
python global_variability.py

# Global variability with combinations (all combinations of 3 personas)
python global_variability_combinations.py
```

### Output

- **Console output**: Formatted tables showing variability statistics
- **JSON files**: 
  - `global_variability_results.json`
  - `global_variability_combinations_results.json`

### Key Findings

- **Without persona**: Mean variability = 0.0783 (high consistency)
- **With persona**: Mean variability = 0.1535 (approximately 2x higher)
- **Conclusion**: Persona patterns significantly increase variability in GPT-4o annotations

---

## Experiment 2: Persona-level Similarity Analysis

### Purpose

This experiment investigates whether conditioning GPT-4o with a specific persona pattern increases its alignment with the corresponding human annotator. For each persona Ann_X, we compare the similarity between Ann_X's human annotations and GPT-4o annotations generated with the matching persona pattern, against the similarity between Ann_X and GPT-4o annotations produced without any persona pattern.

### Script

**`analyze_variability.py`**: Performs persona-level similarity analysis for all 5 personas

### Methodology

#### Data Processing

1. **Load all files**: 
   - Human persona annotations (Ann_X.xlsx)
   - GPT-4o with persona annotations (gpt-4o-Ann_X-annotations.xlsx)
   - GPT-4o without persona annotations (all 3 files: gpt-4o-1, gpt-4o-2, gpt-4o-3)

2. **Extract by reviewId**: Same as Experiment 1 - group by `reviewId` and skip duplicates

3. **Find common reviews**: Only use `reviewId`s that exist in:
   - The human persona file
   - The corresponding GPT-4o with persona file
   - All 3 GPT-4o without persona files

#### Similarity Calculation

For each persona Ann_X:

1. **With persona pattern**: 
   - Calculate Jaccard similarity between human annotations and GPT-4o-with-persona annotations for each common `reviewId`
   - Compute mean, std, min, max across all reviews

2. **Without persona pattern**:
   - For each common `reviewId`, calculate Jaccard similarity between human annotations and each of the 3 GPT-4o-without-persona files
   - Average the 3 similarities to get a single value per review
   - Compute mean, std, min, max across all reviews

3. **Compare**: Calculate the difference (with persona - without persona)

### Running the Analysis

```bash
python analyze_variability.py
```

### Output

- **Console output**: 
  - Detailed results for each persona
  - Summary table comparing all personas
- **JSON file**: `persona_similarity_results.json`

### Key Findings

For all 5 personas:
- **Similarity with persona**: 0.42-0.47 (mean ~0.44)
- **Similarity without persona**: 0.56-0.64 (mean ~0.60)
- **Difference**: -0.14 to -0.19 (persona reduces similarity)
- **Conclusion**: Persona conditioning does NOT improve alignment with human annotators; instead, it reduces similarity and approaches random chance (~0.44 ≈ 0.5)

---

## Technical Implementation Details

### Common Functions

Both experiments share the following core functions:

#### `jaccard_similarity(set1, set2) -> float`
Calculates Jaccard similarity between two sets of emotion labels.
- Returns 1.0 if both sets are empty
- Returns 0.0 if one set is empty
- Otherwise: `|intersection| / |union|`

#### `load_annotations(file_path) -> pd.DataFrame`
Loads an Excel file using pandas and returns a DataFrame.

#### `extract_annotations_by_review(df, skip_duplicates=True) -> Dict[str, Set]`
Extracts annotations grouped by `reviewId`:
1. Groups DataFrame by `reviewId`
2. If `skip_duplicates=True`, skips reviews with multiple rows (same `reviewId`)
3. For each review, collects all emotions from all sentences into a single set
4. Returns dictionary: `{reviewId: {emotion1, emotion2, ...}}`

### Data Handling

- **Grouping**: All analyses group by `reviewId` to handle multi-sentence reviews
- **Duplicate handling**: Reviews with duplicate `reviewId`s are skipped
- **Common reviews**: Only `reviewId`s present in all compared files are used
- **Emotion extraction**: Only emotions with value = 1 are included in the sets

### Dependencies

- `pandas`: For reading Excel files
- `numpy`: For numerical operations and statistics
- `openpyxl`: For Excel file support
- `itertools.combinations`: For generating persona combinations
- `pathlib`: For file path handling
- `json`: For saving results

### Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Requirements File

The `requirements.txt` includes:
```
pandas>=2.0.0
numpy>=1.24.0
openpyxl>=3.1.0
```

---

## Results Summary

### Experiment 1: Global Variability
- **Finding**: Persona patterns increase variability (0.1535 vs 0.0783)
- **Interpretation**: Different personas lead to more diverse annotation patterns

### Experiment 2: Persona-level Similarity
- **Finding**: Persona patterns reduce similarity with human annotators (0.44 vs 0.60)
- **Interpretation**: Persona conditioning does not effectively replicate individual human annotation styles

### Overall Conclusion

The persona patterns increase variability among GPT-4o annotations but do not improve alignment with individual human annotators. The similarity with persona patterns approaches random chance, suggesting that the current persona approach may not effectively capture or replicate individual annotation tendencies.

---

## File Structure

```
experiment_1/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── global_variability.py              # Experiment 1: Basic global variability
├── global_variability_combinations.py # Experiment 1: Variability with combinations
├── analyze_variability.py             # Experiment 2: Persona-level similarity
├── Personas/                          # Data directory
│   ├── Ann_1.xlsx ... Ann_5.xlsx     # Human persona annotations
│   ├── gpt-4o-1-annotations.xlsx     # GPT-4o without persona (run 1)
│   ├── gpt-4o-2-annotations.xlsx     # GPT-4o without persona (run 2)
│   ├── gpt-4o-3-annotations.xlsx     # GPT-4o without persona (run 3)
│   ├── gpt-4o-Ann_1-annotations.xlsx # GPT-4o with Ann_1 persona
│   ├── gpt-4o-Ann_2-annotations.xlsx # GPT-4o with Ann_2 persona
│   ├── gpt-4o-Ann_3-annotations.xlsx # GPT-4o with Ann_3 persona
│   ├── gpt-4o-Ann_4-annotations.xlsx # GPT-4o with Ann_4 persona
│   ├── gpt-4o-Ann_5-annotations.xlsx # GPT-4o with Ann_5 persona
│   ├── persona-pattern_Ann_1.json   # Persona pattern definitions
│   ├── persona-pattern_Ann_2.json
│   ├── persona-pattern_Ann_3.json
│   ├── persona-pattern_Ann_4.json
│   ├── persona-pattern_Ann_5.json
│   └── iteration-persona.xlsx        # Persona-iteration mapping
├── global_variability_results.json    # Experiment 1 results
├── global_variability_combinations_results.json # Experiment 1 (combinations) results
└── persona_similarity_results.json   # Experiment 2 results
```

---

## Usage Examples

### Run all analyses:
```bash
python global_variability.py
python global_variability_combinations.py
python analyze_variability.py
```

### View results:
Results are saved as JSON files and can be loaded in Python:
```python
import json
with open('global_variability_results.json', 'r') as f:
    results = json.load(f)
```

---

## Notes

- All analyses use Jaccard similarity as the agreement metric
- Reviews with duplicate `reviewId`s are automatically skipped
- Only reviews present in all compared files are analyzed
- The scripts handle missing files gracefully with error messages
