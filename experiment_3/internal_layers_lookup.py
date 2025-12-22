#!/usr/bin/env python3
"""
Internal Layers Lookup Experiment - Group Variable Analysis

This script:
1. Loads persona variables from SPP_example.json
2. Uses variable groups (A-M) from experiment_2
3. Captures internal layer activations for:
   - Full prompt (all variables)
   - Ablated prompt (without a specific group)
4. Compares activations using L2 distance
5. Generates visualizations and summaries
"""

import os
import json
import argparse
import numpy as np
import torch
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib import ticker

# System prompt template (same as experiment_2)
SYSTEM_PROMPT = """You are this person. Answer questions naturally as they would.

Person details:
{variables}

Remember: Answer ONLY as this person would. No explanations, no variable lists, just their answer."""

# Variable to group mapping (from experiment_2)
VARIABLE_GROUPS = {
    'A': ['fullName', 'pronouns', 'preferredName', 'signatureQuote', 'imageStyle', 'privacyPreference'],
    'B': ['age', 'genderIdentity', 'ethnicity', 'nationality', 'legalStatus', 'politicalOrientation'],
    'C': ['primaryLanguages', 'communicationStyle', 'tonePreference', 'languageRegister', 'secondaryLanguage', 'channelPreferences'],
    'D': ['chronotype', 'peakProductivity', 'sleepSchedule', 'energyFluctuations', 'preferredMeetingTime', 'primaryHobbies', 'secondaryInterests', 'mediaConsumption', 'activityPreference', 'lifestyleOrientation', 'hobbyTime'],
    'E': ['educationLevel', 'academicPerformance', 'fieldOfStudy'],
    'F': ['currentJob', 'previousJobs', 'roleAuthority', 'workExperience', 'industrySector', 'incomeLevel', 'employmentStatus', 'workSchedule'],
    'G': ['relationshipStatus', 'householdComposition', 'numDependents', 'dependentsAge', 'housingType', 'homeOwnership', 'homeEnvironment'],
    'H': ['financialHabits', 'longTermGoals', 'nextPurchase'],
    'I': ['primaryTransport', 'mobilityFrequency', 'mobilityPurpose', 'accessibilityConsiderations', 'mobilityRange'],
    'J': ['healthStatus', 'chronicConditions', 'disabilityStatus', 'accessibilityNeeds'],
    'K': ['shortTermPriorities', 'longTermGoalsPriorities'],
    'L': ['deviceOwnership', 'primaryDevice', 'operatingSystem', 'digitalLiteracy', 'securityPractices', 'trustPropensity', 'digitalActivityFrequency', 'techAttitude'],
    'M': ['professionalSkills', 'softSkills', 'learningAgility', 'skillMotivation', 'certifications']
}

BIG_FIVE_TRAITS = ['extroversion', 'agreeableness', 'conscientiousness', 'neuroticism', 'openness']


def format_variables(variables_dict):
    """Format variables dictionary into a readable string for the prompt."""
    formatted = []
    for key, value in variables_dict.items():
        formatted.append(f"{key}: {value}")
    return "\n".join(formatted)


def get_variables_for_group(group_letter):
    """Get list of variable names for a given group letter."""
    group_letter = group_letter.upper()
    if group_letter not in VARIABLE_GROUPS:
        return None
    return VARIABLE_GROUPS[group_letter]


def build_prompt(variables_dict, question="Explain what you would do in a stressful work situation."):
    """Build prompt with system prompt and variables."""
    variables_str = format_variables(variables_dict)
    system_prompt = SYSTEM_PROMPT.format(variables=variables_str)
    
    # Format for Llama 3.2 Instruct
    prompt = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{question}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    return prompt


class ActivationCapture:
    """Class to capture activations from model layers."""
    
    def __init__(self):
        self.activations = {}
        self.hooks = []
    
    def save_activation(self, name):
        """Create a hook function to save activations."""
        def hook(module, inp, out):
            if isinstance(out, tuple):
                self.activations[name] = out[0].detach().to("cpu")
            else:
                self.activations[name] = out.detach().to("cpu")
        return hook
    
    def register_hooks(self, model):
        """Register forward hooks on model layers."""
        self.hooks = []
        for name, module in model.named_modules():
            if "self_attn" in name or "mlp" in name:
                hook = module.register_forward_hook(self.save_activation(name))
                self.hooks.append(hook)
    
    def clear(self):
        """Clear captured activations."""
        self.activations.clear()
    
    def remove_hooks(self):
        """Remove all registered hooks."""
        for hook in self.hooks:
            hook.remove()
        self.hooks = []


def l2_distance(a, b):
    """Calculate L2 distance between two activation tensors."""
    min_len = min(a.shape[1], b.shape[1])
    a_sliced = a[:, :min_len, :]
    b_sliced = b[:, :min_len, :]
    return torch.norm(a_sliced - b_sliced).item()


def run_experiment(group_letter, variables_path, model_name="meta-llama/Llama-3.2-3B", 
                   question="Explain what you would do in a stressful work situation.",
                   hf_token=None, device=None):
    """Run the internal layers experiment for a specific group."""
    
    # Load variables
    with open(variables_path, 'r', encoding='utf-8') as f:
        all_variables = json.load(f)
    
    # Get variables for the group
    group_vars = get_variables_for_group(group_letter)
    if group_vars is None:
        raise ValueError(f"Invalid group letter: {group_letter}")
    
    # Check which variables exist
    existing_group_vars = [v for v in group_vars if v in all_variables]
    if not existing_group_vars:
        raise ValueError(f"No variables from group {group_letter} found in data")
    
    # Create variables without the group
    variables_without_group = {k: v for k, v in all_variables.items() if k not in existing_group_vars}
    
    print(f"\n{'='*80}")
    print(f"EXPERIMENT: Group {group_letter}")
    print(f"{'='*80}")
    print(f"Group variables: {existing_group_vars}")
    print(f"Variables with group: {len(all_variables)}")
    print(f"Variables without group: {len(variables_without_group)}")
    
    # Setup device
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Load model
    print(f"\nLoading model: {model_name}")
    model_kwargs = {
        "torch_dtype": torch.float16 if device == "cuda" else torch.float32,
        "device_map": "auto" if device == "cuda" else None,
    }
    
    if hf_token:
        model_kwargs["token"] = hf_token
        os.environ["HF_TOKEN"] = hf_token
    
    model = AutoModelForCausalLM.from_pretrained(model_name, **model_kwargs)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    if device == "cpu":
        model = model.to("cpu")
    
    print("Model loaded.")
    
    # Register hooks
    activation_capture = ActivationCapture()
    activation_capture.register_hooks(model)
    print(f"Registered hooks on {len(activation_capture.hooks)} modules")
    
    # Build prompts
    full_prompt = build_prompt(all_variables, question)
    ablated_prompt = build_prompt(variables_without_group, question)
    
    print(f"\nFull prompt length: {len(full_prompt)} chars")
    print(f"Ablated prompt length: {len(ablated_prompt)} chars")
    
    # Capture activations for full prompt
    print("\nCapturing activations for FULL prompt...")
    activation_capture.clear()
    inputs_full = tokenizer(full_prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        _ = model(**inputs_full)
    acts_full = activation_capture.activations.copy()
    
    print(f"Captured {len(acts_full)} layer activations")
    
    # Capture activations for ablated prompt
    print("\nCapturing activations for ABLATED prompt (without group)...")
    activation_capture.clear()
    inputs_abl = tokenizer(ablated_prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        _ = model(**inputs_abl)
    acts_abl = activation_capture.activations.copy()
    
    print(f"Captured {len(acts_abl)} layer activations")
    
    # Calculate differences
    print("\nCalculating L2 differences...")
    layer_diffs = {}
    
    for layer_name in acts_full.keys():
        if layer_name in acts_abl:
            A = acts_full[layer_name]
            B = acts_abl[layer_name]
            diff = l2_distance(A, B)
            layer_diffs[layer_name] = diff
        else:
            print(f"Warning: Layer {layer_name} missing in ablated activations")
    
    # Calculate summary statistics
    diffs_values = list(layer_diffs.values())
    mean_diff = np.mean(diffs_values)
    std_diff = np.std(diffs_values)
    max_diff = np.max(diffs_values)
    min_diff = np.min(diffs_values)
    
    print(f"\n{'='*80}")
    print(f"RESULTS SUMMARY - Group {group_letter}")
    print(f"{'='*80}")
    print(f"Mean activation shift: {mean_diff:.6f}")
    print(f"Std activation shift: {std_diff:.6f}")
    print(f"Min activation shift: {min_diff:.6f}")
    print(f"Max activation shift: {max_diff:.6f}")
    print(f"Number of layers compared: {len(layer_diffs)}")
    
    # Top layers with highest differences
    sorted_layers = sorted(layer_diffs.items(), key=lambda x: x[1], reverse=True)
    print(f"\nTop 10 layers with highest activation differences:")
    for layer_name, diff_value in sorted_layers[:10]:
        print(f"  {layer_name}: {diff_value:.6f}")
    
    # Cleanup
    activation_capture.remove_hooks()
    
    return {
        'group': group_letter,
        'group_variables': existing_group_vars,
        'layer_diffs': layer_diffs,
        'summary': {
            'mean': mean_diff,
            'std': std_diff,
            'min': min_diff,
            'max': max_diff,
            'num_layers': len(layer_diffs)
        },
        'acts_full': acts_full,
        'acts_abl': acts_abl
    }


def create_heatmap(results, output_path=None):
    """Create heatmap visualization of layer differences."""
    layer_diffs = results['layer_diffs']
    group_letter = results['group']
    
    # Sort layers by name for consistent ordering
    layer_names = sorted(layer_diffs.keys())
    diff_values = [layer_diffs[name] for name in layer_names]
    
    # Normalize (z-score)
    diff_array = np.array(diff_values)
    mean = diff_array.mean()
    std = diff_array.std() if diff_array.std() > 0 else 1.0
    normalized = (diff_array - mean) / std
    
    # Create figure
    fig, ax = plt.subplots(figsize=(max(12, len(layer_names) * 0.3), 6), dpi=120)
    
    # Plot
    im = ax.imshow(normalized.reshape(1, -1), aspect='auto', cmap='viridis', interpolation='nearest')
    
    # Labels
    ax.set_xticks(np.arange(len(layer_names)))
    short_names = [ln.split('.')[-1] if len(ln) > 30 else ln for ln in layer_names]
    ax.set_xticklabels(short_names, fontsize=8, rotation=90)
    ax.set_yticks([0])
    ax.set_yticklabels([f"Group {group_letter}"], fontsize=10)
    
    ax.set_xlabel("Model layers / modules", fontsize=10)
    ax.set_title(f"Activation Differences: Full vs Without Group {group_letter}", fontsize=12)
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Normalized L2 Difference (z-score)', fontsize=9)
    
    # Annotate top values
    top_k = min(10, len(layer_names))
    top_indices = np.argsort(-diff_array)[:top_k]
    for idx in top_indices:
        val = diff_values[idx]
        ax.text(idx, 0, f"{val:.2f}", ha='center', va='center', 
                fontsize=7, color='white', weight='bold')
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        print(f"\nHeatmap saved to: {output_path}")
    else:
        plt.show()
    
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description="Internal layers lookup experiment for group variable analysis"
    )
    parser.add_argument(
        '--group',
        type=str,
        required=True,
        help="Group letter to analyze (A-M)"
    )
    parser.add_argument(
        '--variables',
        type=str,
        default=None,
        help="Path to SPP_example.json (default: ../evaluate_variable/SPP_example.json)"
    )
    parser.add_argument(
        '--model',
        type=str,
        default="meta-llama/Llama-3.2-3B",
        help="Model name (default: meta-llama/Llama-3.2-3B)"
    )
    parser.add_argument(
        '--question',
        type=str,
        default="Explain what you would do in a stressful work situation.",
        help="Question to ask the persona"
    )
    parser.add_argument(
        '--hf-token',
        type=str,
        default=None,
        help="Hugging Face token (or set HF_TOKEN env var)"
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help="Output path for heatmap (default: group_{group}_heatmap.png)"
    )
    parser.add_argument(
        '--device',
        type=str,
        default=None,
        choices=['cuda', 'cpu'],
        help="Device to use (default: auto-detect)"
    )
    
    args = parser.parse_args()
    
    # Set up paths
    script_dir = Path(__file__).parent
    if args.variables:
        variables_path = Path(args.variables)
    else:
        variables_path = script_dir.parent / 'evaluate_variable' / 'SPP_example.json'
    
    if not variables_path.exists():
        print(f"Error: Variables file not found: {variables_path}")
        return
    
    # Get HF token
    hf_token = args.hf_token or os.environ.get("HF_TOKEN")
    
    # Run experiment
    try:
        results = run_experiment(
            group_letter=args.group,
            variables_path=variables_path,
            model_name=args.model,
            question=args.question,
            hf_token=hf_token,
            device=args.device
        )
        
        # Create visualization
        output_path = args.output or f"group_{args.group}_heatmap.png"
        create_heatmap(results, output_path)
        
        # Save results to JSON
        results_json = {
            'group': results['group'],
            'group_variables': results['group_variables'],
            'summary': results['summary'],
            'layer_diffs': {k: float(v) for k, v in results['layer_diffs'].items()}
        }
        
        json_path = f"group_{args.group}_results.json"
        with open(json_path, 'w') as f:
            json.dump(results_json, f, indent=2)
        print(f"\nResults saved to: {json_path}")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
