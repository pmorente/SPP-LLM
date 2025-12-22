#!/usr/bin/env python3
"""
Global Variability Analysis with Persona Combinations

This script compares variability among gpt-4o-Y-annotations files (without persona)
vs all possible combinations of 3 personas from the 5 available personas.

Since it doesn't make sense to compare 3 runs without persona pattern against 
5 runs with persona pattern, we create all possible groups of 3 personas 
(C(5,3) = 10 combinations) and calculate variability for each group.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from itertools import combinations
import json
from typing import Dict, Set, List, Tuple

def jaccard_similarity(set1: Set, set2: Set) -> float:
    """
    Calculate Jaccard similarity between two sets.
    
    Jaccard similarity = |A ∩ B| / |A ∪ B|
    """
    if len(set1) == 0 and len(set2) == 0:
        return 1.0
    if len(set1) == 0 or len(set2) == 0:
        return 0.0
    
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    return intersection / union if union > 0 else 0.0


def load_annotations(file_path: Path) -> pd.DataFrame:
    """Load annotations from Excel file."""
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None


def extract_annotations_by_review(df: pd.DataFrame, skip_duplicates: bool = True) -> Dict[str, Set]:
    """
    Extract annotations grouped by reviewId.
    
    For each reviewId, collect all emotions from all sentences in that review.
    Skips reviews that have multiple rows with the same reviewId if skip_duplicates=True.
    """
    # Emotion/label columns
    emotion_columns = ['Joy', 'Trust', 'Fear', 'Surprise', 'Sadness', 
                      'Disgust', 'Anger', 'Anticipation', 'Neutral', 'Reject']
    
    # Find which emotion columns exist in the dataframe
    available_emotions = [col for col in emotion_columns if col in df.columns]
    
    if len(available_emotions) == 0:
        raise ValueError(f"No emotion columns found. Available columns: {df.columns.tolist()}")
    
    if 'reviewId' not in df.columns:
        raise ValueError(f"reviewId column not found. Available columns: {df.columns.tolist()}")
    
    # Create dictionary mapping reviewId to set of all emotions in that review
    annotations = {}
    
    # Group by reviewId
    for review_id, group in df.groupby('reviewId'):
        # Skip reviews with multiple rows (duplicate reviewIds)
        if skip_duplicates and len(group) > 1:
            continue
        
        review_id_str = str(review_id)
        
        # Collect all emotions that are set to 1
        labels = set()
        for _, row in group.iterrows():
            for emotion in available_emotions:
                if emotion in row and pd.notna(row[emotion]):
                    # Check if value is 1 (or True, or '1', etc.)
                    val = row[emotion]
                    if val == 1 or val == '1' or val is True or (isinstance(val, str) and val.lower() == 'true'):
                        labels.add(emotion)
        
        annotations[review_id_str] = labels
    
    return annotations


def calculate_variability_for_group(group_annotations: Dict[str, Dict[str, Set]], group_name: str) -> Dict:
    """
    Calculate variability for a group of annotation files.
    
    Args:
        group_annotations: Dictionary mapping file names to their annotations
        group_name: Name of the group for display
    
    Returns:
        Dictionary with variability statistics
    """
    # Get common review IDs across all files in the group
    common_ids = set.intersection(*[set(ann.keys()) for ann in group_annotations.values()])
    
    if len(common_ids) == 0:
        return None
    
    # Calculate pairwise similarities between files for each review
    similarities = []
    for review_id in common_ids:
        annotation_sets = [ann[review_id] for ann in group_annotations.values()]
        # Calculate pairwise similarities between all files for this review
        for i, j in combinations(range(len(annotation_sets)), 2):
            sim = jaccard_similarity(annotation_sets[i], annotation_sets[j])
            similarities.append(sim)
    
    if len(similarities) == 0:
        return None
    
    # Calculate statistics
    mean_sim = np.mean(similarities)
    variability = 1 - mean_sim
    
    return {
        'mean_similarity': float(mean_sim),
        'std': float(np.std(similarities)),
        'min': float(np.min(similarities)),
        'max': float(np.max(similarities)),
        'count': int(len(similarities)),
        'variability': float(variability),
        'num_reviews': int(len(common_ids)),
        'group_name': group_name
    }


def analyze_global_variability_with_combinations(personas_dir: Path) -> Dict:
    """
    Analysis: Global variability comparing:
    - gpt-4o-1, gpt-4o-2, gpt-4o-3 (without persona) - 1 group of 3
    - All combinations of 3 personas from 5 available - 10 groups of 3
    """
    print("="*80)
    print("GLOBAL VARIABILITY ANALYSIS WITH PERSONA COMBINATIONS")
    print("="*80)
    print("\nComparing variability:")
    print("  - gpt-4o-Y-annotations (without persona pattern): 1 group of 3 files")
    print("  - gpt-4o-Ann_X-annotations (with persona pattern): all combinations of 3 from 5 personas")
    print("="*80)
    
    # Load GPT-4o without persona files
    gpt_no_persona_files = [
        personas_dir / 'gpt-4o-1-annotations.xlsx',
        personas_dir / 'gpt-4o-2-annotations.xlsx',
        personas_dir / 'gpt-4o-3-annotations.xlsx'
    ]
    
    # Load GPT-4o with persona files
    persona_numbers = list(range(1, 6))
    gpt_with_persona_files = {
        f'Ann_{i}': personas_dir / f'gpt-4o-Ann_{i}-annotations.xlsx'
        for i in persona_numbers
    }
    
    # Load all annotations
    print("\nLoading files...")
    gpt_no_persona_annotations = {}
    for file_path in gpt_no_persona_files:
        if file_path.exists():
            df = load_annotations(file_path)
            if df is not None:
                name = file_path.stem
                gpt_no_persona_annotations[name] = extract_annotations_by_review(df, skip_duplicates=True)
                print(f"  Loaded {name}: {len(gpt_no_persona_annotations[name])} reviews")
    
    gpt_with_persona_annotations = {}
    for persona_name, file_path in gpt_with_persona_files.items():
        if file_path.exists():
            df = load_annotations(file_path)
            if df is not None:
                gpt_with_persona_annotations[persona_name] = extract_annotations_by_review(df, skip_duplicates=True)
                print(f"  Loaded gpt-4o-{persona_name}: {len(gpt_with_persona_annotations[persona_name])} reviews")
    
    if len(gpt_no_persona_annotations) == 0:
        print("Error: No GPT-4o without persona files found!")
        return None
    
    if len(gpt_with_persona_annotations) < 3:
        print("Error: Need at least 3 persona files to create combinations!")
        return None
    
    # Calculate variability for without-persona group
    print("\n" + "-"*80)
    print("Calculating variability for WITHOUT persona pattern...")
    print("-"*80)
    no_persona_stats = calculate_variability_for_group(
        gpt_no_persona_annotations, 
        "Without Persona (gpt-4o-1, gpt-4o-2, gpt-4o-3)"
    )
    
    if no_persona_stats is None:
        print("Error: Could not calculate variability for without-persona group!")
        return None
    
    print(f"  Group: {no_persona_stats['group_name']}")
    print(f"  Common reviewIds: {no_persona_stats['num_reviews']}")
    print(f"  Mean similarity: {no_persona_stats['mean_similarity']:.4f}")
    print(f"  Variability: {no_persona_stats['variability']:.4f}")
    
    # Calculate variability for all combinations of 3 personas
    print("\n" + "-"*80)
    print("Calculating variability for WITH persona pattern (all combinations of 3)...")
    print("-"*80)
    
    persona_combinations = list(combinations(persona_numbers, 3))
    print(f"  Total combinations: {len(persona_combinations)}")
    
    combination_results = []
    for combo in persona_combinations:
        # Create group name
        persona_names = [f'Ann_{i}' for i in combo]
        group_name = f"Personas: {', '.join(persona_names)}"
        
        # Get annotations for this combination
        combo_annotations = {
            persona_name: gpt_with_persona_annotations[persona_name]
            for persona_name in persona_names
        }
        
        # Calculate variability for this combination
        combo_stats = calculate_variability_for_group(combo_annotations, group_name)
        
        if combo_stats is not None:
            combination_results.append(combo_stats)
            print(f"  {group_name}: variability = {combo_stats['variability']:.4f} (reviews: {combo_stats['num_reviews']})")
    
    if len(combination_results) == 0:
        print("Error: Could not calculate variability for any persona combination!")
        return None
    
    # Calculate overall statistics for persona combinations
    persona_variabilities = [r['variability'] for r in combination_results]
    persona_similarities = [r['mean_similarity'] for r in combination_results]
    persona_stds = [r['std'] for r in combination_results]  # Std within each combination
    
    overall_persona_stats = {
        'mean_variability': float(np.mean(persona_variabilities)),
        'std_variability': float(np.std(persona_variabilities)),
        'min_variability': float(np.min(persona_variabilities)),
        'max_variability': float(np.max(persona_variabilities)),
        'mean_similarity': float(np.mean(persona_similarities)),
        'std_similarity': float(np.std(persona_similarities)),  # Std across combinations
        'mean_std_within_combinations': float(np.mean(persona_stds)),  # Average std within combinations
        'num_combinations': len(combination_results)
    }
    
    # Print results table
    print("\n" + "="*80)
    print("RESULTS")
    print("="*80)
    
    # Individual combination results table
    print("\n" + "-"*80)
    print("VARIABILITY BY PERSONA COMBINATION")
    print("-"*80)
    print(f"{'Combination':<40} {'Variability':<15} {'Mean Sim':<15} {'# Reviews':<12}")
    print("-"*80)
    for result in sorted(combination_results, key=lambda x: x['variability']):
        combo_name = result['group_name'].replace('Personas: ', '')
        print(f"{combo_name:<40} {result['variability']:<15.4f} {result['mean_similarity']:<15.4f} {result['num_reviews']:<12}")
    
    # Calculate variability statistics for without-persona from pairwise similarities
    # Variability = 1 - similarity, so:
    # - Std of variability = std of similarity (same value)
    # - Min variability = 1 - max_similarity
    # - Max variability = 1 - min_similarity
    no_persona_min_variability = 1 - no_persona_stats['max']
    no_persona_max_variability = 1 - no_persona_stats['min']
    
    # Overall comparison table
    print("\n" + "-"*80)
    print("OVERALL COMPARISON")
    print("-"*80)
    print(f"{'Metric':<35} {'Without Persona':<20} {'With Persona (Avg)':<20}")
    print("-"*80)
    print(f"{'Mean Variability':<35} {no_persona_stats['variability']:<20.4f} {overall_persona_stats['mean_variability']:<20.4f}")
    print(f"{'Std Deviation (Variability)':<35} {no_persona_stats['std']:<20.4f} {overall_persona_stats['std_variability']:<20.4f}")
    print(f"{'Min Variability':<35} {no_persona_min_variability:<20.4f} {overall_persona_stats['min_variability']:<20.4f}")
    print(f"{'Max Variability':<35} {no_persona_max_variability:<20.4f} {overall_persona_stats['max_variability']:<20.4f}")
    print(f"{'Mean Similarity':<35} {no_persona_stats['mean_similarity']:<20.4f} {overall_persona_stats['mean_similarity']:<20.4f}")
    print(f"{'Std Deviation (Similarity)':<35} {no_persona_stats['std']:<20.4f} {overall_persona_stats['mean_std_within_combinations']:<20.4f}")
    print("-"*80)
    diff = overall_persona_stats['mean_variability'] - no_persona_stats['variability']
    print(f"{'Difference (with - without)':<35} {'':<20} {diff:<20.4f}")
    print("="*80)
    
    return {
        'without_persona': no_persona_stats,
        'persona_combinations': combination_results,
        'overall_persona_stats': overall_persona_stats,
        'difference': float(diff)
    }


def main():
    """Main function to run the global variability analysis with combinations."""
    # Set up paths
    script_dir = Path(__file__).parent
    personas_dir = script_dir / 'Personas'
    
    if not personas_dir.exists():
        print(f"Error: Personas directory not found at {personas_dir}")
        return
    
    print(f"Working directory: {script_dir}")
    print(f"Personas directory: {personas_dir}\n")
    
    # Run analysis
    results = analyze_global_variability_with_combinations(personas_dir)
    
    if results is None:
        return
    
    # Save results to JSON
    output_file = script_dir / 'global_variability_combinations_results.json'
    
    # Convert to JSON-serializable format
    def convert_to_native(obj):
        if isinstance(obj, (np.integer, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float16, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: convert_to_native(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_native(item) for item in obj]
        elif isinstance(obj, (bool, int, float, str)) or obj is None:
            return obj
        else:
            return str(obj)
    
    with open(output_file, 'w') as f:
        json.dump(convert_to_native(results), f, indent=2)
    
    print(f"\n" + "="*80)
    print(f"Results saved to: {output_file}")
    print("="*80)


if __name__ == '__main__':
    main()
