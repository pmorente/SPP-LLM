# Experiment 3: Internal Layers Lookup

This experiment analyzes how removing variable groups affects internal layer activations in the LLM.

## Overview

The script captures internal layer activations (self-attention and MLP layers) when processing:
1. **Full prompt**: All persona variables included
2. **Ablated prompt**: A specific variable group (A-M) removed

It then compares these activations using L2 distance to identify which layers are most affected by the removed group.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set Hugging Face token (if needed):
```bash
export HF_TOKEN="your_token_here"
```

Or pass it via `--hf-token` argument.

## Usage

### Basic Usage

```bash
# Analyze group K (Goals & Priorities)
python internal_layers_lookup.py --group K
```

### Options

```bash
# Specify custom variables file
python internal_layers_lookup.py --group K --variables /path/to/SPP_example.json

# Use different model
python internal_layers_lookup.py --group K --model meta-llama/Llama-3.2-3B-Instruct

# Custom question
python internal_layers_lookup.py --group K --question "What are your hobbies?"

# Specify device
python internal_layers_lookup.py --group K --device cuda

# Custom output path
python internal_layers_lookup.py --group K --output my_heatmap.png
```

## Output

The script generates:

1. **Console output**: Summary statistics and top layers with highest differences
2. **Heatmap**: `group_{letter}_heatmap.png` - Visualization of activation differences across layers
3. **JSON results**: `group_{letter}_results.json` - Detailed results including:
   - Group information
   - Summary statistics (mean, std, min, max)
   - Per-layer L2 differences

## Variable Groups

Same groups as experiment_2:
- **A**: Personal identifiers & representation
- **B**: Core demographics
- **C**: Language & communication attributes
- **D**: Lifestyle, routines & time patterns
- **E**: Education & academic profile
- **F**: Employment, career
- **G**: Household, family & domestic context
- **H**: Financial & consumer behavior
- **I**: Mobility
- **J**: Health & accessibility
- **K**: Goals, priorities
- **L**: Digital identity, platform & trust posture
- **M**: Skills

## Notes

- The script captures activations from `self_attn` and `mlp` modules
- L2 distance is calculated between corresponding layers
- Results are normalized (z-score) for visualization
- Requires GPU for reasonable performance (CPU is very slow)
