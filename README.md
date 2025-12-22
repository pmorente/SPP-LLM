# I2R Experiments: Persona Variable Impact Analysis

<div align="center">
  <img src="logo.png" alt="Logo" width="300"/>
</div>

This repository contains a series of experiments investigating how different persona variables and variable groups affect Large Language Model (LLM) behavior, both in terms of output responses and internal neural activations.

## Project Overview

The experiments use a comprehensive persona profile system (SPP - Structured Persona Profile) with 66 variables organized into 13 groups (A-M), plus Big Five personality traits. Each experiment examines different aspects of how these variables influence LLM behavior.

## Repository Structure

```
I2R Experiments/
├── persona_preprocessing/     # Persona preprocessing and Big Five analysis
├── experiment_1/             # Persona pattern variability analysis
├── experiment_2/             # Variable impact on output responses
│   ├── evaluate_variable/    # Variable evaluation experiments
│   └── post_analyse/         # Post-analysis and embedding comparison
└── experiment_3/              # Internal layer activation analysis
```

---

## 📁 persona_preprocessing/

**Purpose**: Preprocessing and analysis of persona data, including Big Five personality trait interpretation.

**Key Files**:
- `bigFive_Interpretability.py`: Analyzes and interprets Big Five personality traits from persona data
- `answers.json`: Persona answer data for analysis

**Usage**:
```bash
cd persona_preprocessing
python3 bigFive_Interpretability.py answers.json
```

**What it does**: Processes persona data to extract and interpret Big Five personality dimensions (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism) from structured persona profiles.

---

## 📁 experiment_1/

**Purpose**: Analyzes the impact of persona patterns on GPT-4o annotation behavior and variability.

**Key Components**:
- **Global Variability Analysis**: Compares variability among GPT-4o annotations with and without persona patterns
- **Persona Similarity Analysis**: Measures similarity between different persona patterns

**Key Files**:
- `global_variability.py`: Compares variability between without-persona and with-persona annotations
- `global_variability_combinations.py`: Analyzes all combinations of personas
- `Personas/`: Contains persona pattern JSON files and annotation Excel files

**Methodology**:
1. Loads annotations from Excel files (human and GPT-4o annotations)
2. Extracts emotion annotations per review
3. Calculates variability metrics (Jaccard distance, emotion distribution differences)
4. Compares groups with and without persona patterns

**Results**: Saved in `results/` folder as JSON files with variability metrics and statistical comparisons.

**Usage**:
```bash
cd experiment_1
pip install -r requirements.txt
python global_variability.py
python global_variability_combinations.py
```

---

## 📁 experiment_2/

**Purpose**: Evaluates the impact of individual variables and variable groups on LLM output responses using a local Llama 3.2 3B model.

### experiment_2/evaluate_variable/

**What it does**: 
- Generates persona responses with full variable set vs. with specific variable/group removed
- Compares responses to measure variable impact on output

**Key Files**:
- `SPP_example.json`: Complete persona profile with 66 variables
- `input.csv`: 1000 questions to test persona responses
- `run_experiment.py`: Individual variable evaluation
- `run_group_experiment.py`: Variable group (A-M) evaluation
- `sample_questions.py`: Utility to randomly sample questions

**Variable Groups (A-M)**:
- **A**: Personal identifiers & representation (6 variables)
- **B**: Core demographics (6 variables)
- **C**: Language & communication attributes (6 variables)
- **D**: Lifestyle, routines & time patterns (11 variables)
- **E**: Education & academic profile (3 variables)
- **F**: Employment, career (8 variables)
- **G**: Household, family & domestic context (7 variables)
- **H**: Financial & consumer behavior (3 variables)
- **I**: Mobility (5 variables)
- **J**: Health & accessibility (4 variables)
- **K**: Goals, priorities (2 variables)
- **L**: Digital identity, platform & trust posture (8 variables)
- **M**: Skills (5 variables)

**Usage**:
```bash
cd experiment_2/evaluate_variable
pip install -r ../requirements.txt

# Individual variable
python run_experiment.py --variable age --sample 100 --seed-time

# Single group
python run_group_experiment.py --group K --sample 100

# All groups sequentially
python run_group_experiment.py --all-groups --sample 50 --seed 42
```

**Output**: 
- `responses_full_{variable}.csv` / `responses_without_{variable}.csv`
- `responses_full_group_{letter}.csv` / `responses_without_group_{letter}.csv`

### experiment_2/post_analyse/

**What it does**: 
- Generates embeddings from response files using multiple models (384, 768, 1024 dimensions)
- Calculates similarity metrics (Euclidean distance, Cosine similarity, Pearson correlation)
- Compares responses with vs. without variable groups

**Key Files**:
- `analyze_group.py`: Main analysis script for group comparisons
- `generateEmbeddings.py`: Standalone embedding generation utility
- `tools/embeddingGenerator.py`: Embedding generation module
- `CPU/`: C++ implementations of metrics (alternative, not used by analyze_group.py)

**Usage**:
```bash
cd experiment_2/post_analyse
pip install -r requirements.txt

# Analyze a specific group
python analyze_group.py --group K

# Analyze with regeneration of embeddings
python analyze_group.py --group K --regenerate

# Analyze only one dimension
python analyze_group.py --group K --model dim_768
```

**Output**:
- `outputs/embeddings/dimension_{dim}/`: Binary embedding files
- `outputs/results/group_{letter}_analysis.txt`: Detailed metrics table
- Console output with formatted results table

**Metrics Calculated**:
- **Euclidean Distance**: Straight-line distance between embeddings (range: [0, ∞))
- **Cosine Similarity**: Angle-based similarity (range: [-1, 1] or [0, 1])
- **Pearson Correlation**: Linear correlation (range: [-1, 1])

---

## 📁 experiment_3/

**Purpose**: Analyzes how removing variable groups affects **internal neural layer activations** in the LLM, not just output responses.

**What it does**:
- Captures activations from `self_attn` and `mlp` layers
- Compares activations between full prompt (all variables) vs. ablated prompt (group removed)
- Identifies which internal layers are most affected by variable removal

**Key Files**:
- `internal_layers_lookup.py`: Main script for activation analysis

**Usage**:
```bash
cd experiment_3
pip install -r requirements.txt

# Analyze group K
python internal_layers_lookup.py --group K

# With custom question
python internal_layers_lookup.py --group K --question "What do you do on weekends?"

# Specify device
python internal_layers_lookup.py --group K --device cuda
```

**Output**:
- `group_{letter}_results.json`: Detailed activation differences per layer
- `group_{letter}_heatmap.png`: Visualization of layer activation differences
- Console output with summary statistics and top affected layers

**Key Insight**: This experiment reveals **where** in the neural network the variable information is processed, not just how it affects the final output.

---

## 🔗 How Experiments Relate

1. **experiment_1**: Establishes that persona patterns affect LLM variability (using GPT-4o)
2. **experiment_2**: Quantifies impact of specific variables/groups on output responses (using Llama 3.2 3B)
3. **experiment_3**: Identifies which internal layers process variable information (using Llama 3.2 3B)

Together, they provide:
- **Behavioral evidence** (experiment_1): Personas change LLM behavior
- **Quantitative measurement** (experiment_2): How much each variable/group matters
- **Mechanistic understanding** (experiment_3): Where in the network variables are processed

---

## 📊 Common Data Structures

### SPP (Structured Persona Profile)

All experiments use the same persona structure from `SPP_example.json`:
- **66 variables** organized into 13 groups (A-M)
- **Big Five personality traits**: extroversion, agreeableness, conscientiousness, neuroticism, openness
- Variables cover: demographics, lifestyle, skills, goals, digital identity, etc.

### Variable Groups

The same 13 groups (A-M) are used consistently across experiments 2 and 3, allowing for cross-experiment comparison.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- CUDA-capable GPU (recommended for experiments 2 & 3)
- Hugging Face account and token (for model access)

### Setup

1. **Clone the repository** (if using git)

2. **Install dependencies** for each experiment:
```bash
# Experiment 1
cd experiment_1
pip install -r requirements.txt

# Experiment 2
cd ../experiment_2
pip install -r requirements.txt

# Experiment 3
cd ../experiment_3
pip install -r requirements.txt
```

3. **Set up Hugging Face token** (for experiments 2 & 3):
```bash
export HF_TOKEN="your_token_here"
```

### Running Experiments

See individual README files in each experiment folder for detailed usage instructions.

---

## 📝 Output Files

All experiments save results in organized folders:

- **experiment_1/results/**: JSON files with variability metrics
- **experiment_2/evaluate_variable/**: CSV files with persona responses
- **experiment_2/post_analyse/outputs/**: Embeddings and analysis results
- **experiment_3/**: JSON results and heatmap visualizations

**Note**: The `.gitignore` is configured to track `results/` and `outputs/` folders, so these will be included in git.

---

## 🔬 Research Questions

These experiments address:

1. **Do persona variables affect LLM behavior?** (experiment_1)
2. **Which variables/groups have the most impact?** (experiment_2)
3. **Where in the neural network is variable information processed?** (experiment_3)
4. **How do different embedding dimensions affect similarity measurements?** (experiment_2/post_analyse)

---

## 📚 References

- **SPP Framework**: Structured Persona Profile with 66 variables across 13 groups
- **Models Used**: 
  - GPT-4o (experiment_1)
  - Llama 3.2 3B (experiments 2 & 3)
- **Embedding Models**: 
  - all-MiniLM-L6-v2 (384 dim)
  - all-mpnet-base-v2 (768 dim)
  - all-roberta-large-v1 (1024 dim)

---

## 📧 Contact & Support

For questions about specific experiments, refer to the individual README files in each experiment folder.

---

## 📄 License

[Add your license information here]
