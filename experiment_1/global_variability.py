#!/usr/bin/env python3
"""
Global Variability Analysis: Compare variability among gpt-4o-Y-annotations files 
vs gpt-4o-Ann_X-annotations files.

This analysis shows whether applying different personas has a real impact on the 
variability of the LLM's behavior.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from itertools import combinations
import json
from typing import Dict, Set

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
    
    The DataFrame has emotion columns: 'Joy', 'Trust', 'Fear', 'Surprise', 
    'Sadness', 'Disgust', 'Anger', 'Anticipation', 'Neutral', 'Reject'
    Each row represents a sentence annotation with binary (0/1) values.
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


def analyze_global_variability(personas_dir: Path) -> Dict:
    """
    Analysis: Global variability with and without persona pattern.
    
    Compare variability among:
    - gpt-4o-1, gpt-4o-2, gpt-4o-3 (without persona)
    - gpt-4o-Ann_1, gpt-4o-Ann_2, ..., gpt-4o-Ann_5 (with persona)
    """
    print("="*80)
    print("GLOBAL VARIABILITY ANALYSIS")
    print("="*80)
    print("\nComparing variability among:")
    print("  - gpt-4o-Y-annotations (without persona pattern)")
    print("  - gpt-4o-Ann_X-annotations (with persona pattern)")
    print("="*80)
    
    # Load GPT-4o without persona files
    gpt_no_persona_files = [
        personas_dir / 'gpt-4o-1-annotations.xlsx',
        personas_dir / 'gpt-4o-2-annotations.xlsx',
        personas_dir / 'gpt-4o-3-annotations.xlsx'
    ]
    
    # Load GPT-4o with persona files
    gpt_with_persona_files = [
        personas_dir / f'gpt-4o-Ann_{i}-annotations.xlsx'
        for i in range(1, 6)
    ]
    
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
    for file_path in gpt_with_persona_files:
        if file_path.exists():
            df = load_annotations(file_path)
            if df is not None:
                name = file_path.stem
                gpt_with_persona_annotations[name] = extract_annotations_by_review(df, skip_duplicates=True)
                print(f"  Loaded {name}: {len(gpt_with_persona_annotations[name])} reviews")
    
    if len(gpt_no_persona_annotations) == 0:
        print("Error: No GPT-4o without persona files found!")
        return None
    
    if len(gpt_with_persona_annotations) == 0:
        print("Error: No GPT-4o with persona files found!")
        return None
    
    # Calculate variability within each group
    print("\n" + "-"*80)
    print("Variability Analysis")
    print("-"*80)
    
    # For gpt-4o-X-annotations: calculate variability among all files
    print("\nCalculating variability for gpt-4o-X-annotations (without persona)...")
    common_ids_no_persona = set.intersection(*[set(ann.keys()) for ann in gpt_no_persona_annotations.values()])
    print(f"  Common reviewIds across all files: {len(common_ids_no_persona)}")
    
    no_persona_similarities = []
    for review_id in common_ids_no_persona:
        annotation_sets = [ann[review_id] for ann in gpt_no_persona_annotations.values()]
        # Calculate pairwise similarities between all files for this review
        for i, j in combinations(range(len(annotation_sets)), 2):
            sim = jaccard_similarity(annotation_sets[i], annotation_sets[j])
            no_persona_similarities.append(sim)
    
    # For gpt-4o-Ann_X-annotations: find common reviewIds across all of them, then calculate variability
    print("\nCalculating variability for gpt-4o-Ann_X-annotations (with persona)...")
    common_ids_with_persona = set.intersection(*[set(ann.keys()) for ann in gpt_with_persona_annotations.values()])
    print(f"  Common reviewIds across all files: {len(common_ids_with_persona)}")
    
    with_persona_similarities = []
    for review_id in common_ids_with_persona:
        annotation_sets = [ann[review_id] for ann in gpt_with_persona_annotations.values()]
        # Calculate pairwise similarities between all files for this review
        for i, j in combinations(range(len(annotation_sets)), 2):
            sim = jaccard_similarity(annotation_sets[i], annotation_sets[j])
            with_persona_similarities.append(sim)
    
    # Calculate statistics
    no_persona_stats = {
        'mean': np.mean(no_persona_similarities) if no_persona_similarities else 0.0,
        'std': np.std(no_persona_similarities) if no_persona_similarities else 0.0,
        'min': np.min(no_persona_similarities) if no_persona_similarities else 0.0,
        'max': np.max(no_persona_similarities) if no_persona_similarities else 0.0,
        'count': len(no_persona_similarities)
    }
    
    with_persona_stats = {
        'mean': np.mean(with_persona_similarities) if with_persona_similarities else 0.0,
        'std': np.std(with_persona_similarities) if with_persona_similarities else 0.0,
        'min': np.min(with_persona_similarities) if with_persona_similarities else 0.0,
        'max': np.max(with_persona_similarities) if with_persona_similarities else 0.0,
        'count': len(with_persona_similarities)
    }
    
    # Variability = 1 - similarity (lower similarity = higher variability)
    no_persona_variability = 1 - no_persona_stats['mean']
    with_persona_variability = 1 - with_persona_stats['mean']
    
    print("\n" + "="*80)
    print("RESULTS")
    print("="*80)
    
    # Print formatted table
    print("\n" + "-"*80)
    print("RESULTS TABLE")
    print("-"*80)
    print(f"{'Metric':<35} {'Without Persona':<20} {'With Persona':<20}")
    print("-"*80)
    print(f"{'Mean Jaccard Similarity':<35} {no_persona_stats['mean']:<20.4f} {with_persona_stats['mean']:<20.4f}")
    print(f"{'Std Deviation':<35} {no_persona_stats['std']:<20.4f} {with_persona_stats['std']:<20.4f}")
    print(f"{'Min Similarity':<35} {no_persona_stats['min']:<20.4f} {with_persona_stats['min']:<20.4f}")
    print(f"{'Max Similarity':<35} {no_persona_stats['max']:<20.4f} {with_persona_stats['max']:<20.4f}")
    print(f"{'Number of Comparisons':<35} {no_persona_stats['count']:<20} {with_persona_stats['count']:<20}")
    print(f"{'Number of Reviews':<35} {len(common_ids_no_persona):<20} {len(common_ids_with_persona):<20}")
    print(f"{'Variability (1 - similarity)':<35} {no_persona_variability:<20.4f} {with_persona_variability:<20.4f}")
    print("-"*80)
    print(f"{'Difference (with - without)':<35} {'':<20} {with_persona_variability - no_persona_variability:<20.4f}")
    print("="*80)
    
    return {
        'no_persona': {
            'mean_similarity': float(no_persona_stats['mean']),
            'std': float(no_persona_stats['std']),
            'min': float(no_persona_stats['min']),
            'max': float(no_persona_stats['max']),
            'count': int(no_persona_stats['count']),
            'variability': float(no_persona_variability),
            'num_reviews': int(len(common_ids_no_persona))
        },
        'with_persona': {
            'mean_similarity': float(with_persona_stats['mean']),
            'std': float(with_persona_stats['std']),
            'min': float(with_persona_stats['min']),
            'max': float(with_persona_stats['max']),
            'count': int(with_persona_stats['count']),
            'variability': float(with_persona_variability),
            'num_reviews': int(len(common_ids_with_persona))
        },
        'difference': float(with_persona_variability - no_persona_variability)
    }


def main():
    """Main function to run the global variability analysis."""
    # Set up paths
    script_dir = Path(__file__).parent
    personas_dir = script_dir / 'Personas'
    
    if not personas_dir.exists():
        print(f"Error: Personas directory not found at {personas_dir}")
        return
    
    print(f"Working directory: {script_dir}")
    print(f"Personas directory: {personas_dir}\n")
    
    # Run analysis
    results = analyze_global_variability(personas_dir)
    
    if results is None:
        return
    
    # Save results to JSON
    output_file = script_dir / 'global_variability_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n" + "="*80)
    print(f"Results saved to: {output_file}")
    print("="*80)


if __name__ == '__main__':
    main()
