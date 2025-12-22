#!/usr/bin/env python3
"""
Persona-level Similarity Analysis

This experiment investigates whether conditioning GPT-4o with a specific persona 
pattern increases its alignment with the corresponding human annotator. 

For each persona Ann_X, we compare the similarity between Ann_X's human annotations 
and GPT-4o annotations generated with the matching persona pattern, against the 
similarity between Ann_X and GPT-4o annotations produced without any persona pattern. 

All comparisons are performed on identical reviews and emotion labels using 
agreement-based similarity metrics such as Jaccard similarity. This analysis directly 
tests whether persona conditioning leads the LLM to replicate individual human 
annotation tendencies more closely.

Dataset structure:
- 12 iterations (iteration_3 to iteration_14), each with 100 reviews (except the last)
- In each iteration, 3 humans participated, while LLMs participated in all
- Files:
  - persona-pattern_Ann_X.json: JSON files with personas (Ann_1 → Ann_5)
  - iteration-persona.xlsx: Relationship between personas and iterations
  - Ann_X.xlsx: Reviews annotated by persona Ann_X
  - gpt-4o-Y-annotations.xlsx: Reviews annotated by GPT-4o without persona (3 executions)
  - gpt-4o-Ann_X-annotations.xlsx: Reviews annotated by GPT-4o with persona Ann_X
"""

import pandas as pd
import numpy as np
from pathlib import Path
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


def analyze_persona_similarity(personas_dir: Path) -> Dict:
    """
    Persona-level Similarity Analysis.
    
    For each persona Ann_X:
    - Compare similarity between Ann_X and gpt-4o-Ann_X-annotations (with persona)
    - Compare similarity between Ann_X and gpt-4o-Y-annotations (without persona)
    
    All comparisons are performed on identical reviews using Jaccard similarity.
    """
    print("="*80)
    print("PERSONA-LEVEL SIMILARITY ANALYSIS")
    print("="*80)
    print("\nThis analysis tests whether persona conditioning leads the LLM")
    print("to replicate individual human annotation tendencies more closely.")
    print("\nFor each persona Ann_X, comparing:")
    print("  - Similarity: Ann_X vs gpt-4o-Ann_X-annotations (WITH persona pattern)")
    print("  - Similarity: Ann_X vs gpt-4o-Y-annotations (WITHOUT persona pattern)")
    print("="*80)
    
    results = {}
    
    # Load GPT-4o without persona files (we'll average across them)
    gpt_no_persona_files = [
        personas_dir / 'gpt-4o-1-annotations.xlsx',
        personas_dir / 'gpt-4o-2-annotations.xlsx',
        personas_dir / 'gpt-4o-3-annotations.xlsx'
    ]
    
    # Load all GPT-4o without persona annotations
    print("\nLoading GPT-4o without persona files...")
    gpt_no_persona_all = []
    for file_path in gpt_no_persona_files:
        if file_path.exists():
            df = load_annotations(file_path)
            if df is not None:
                gpt_no_persona_all.append(extract_annotations_by_review(df, skip_duplicates=True))
                print(f"  Loaded {file_path.name}: {len(gpt_no_persona_all[-1])} reviews")
    
    if len(gpt_no_persona_all) == 0:
        print("Error: No GPT-4o without persona files found!")
        return None
    
    # For each persona
    for persona_num in range(1, 6):
        persona_name = f'Ann_{persona_num}'
        print(f"\n" + "="*80)
        print(f"PERSONA: {persona_name}")
        print("="*80)
        
        # Load human persona annotations
        persona_file = personas_dir / f'{persona_name}.xlsx'
        if not persona_file.exists():
            print(f"  Warning: {persona_file} not found, skipping...")
            continue
        
        df_persona = load_annotations(persona_file)
        if df_persona is None:
            continue
        
        persona_annotations = extract_annotations_by_review(df_persona, skip_duplicates=True)
        print(f"  Loaded {persona_name}: {len(persona_annotations)} reviews")
        
        # Load GPT-4o with persona annotations
        gpt_with_persona_file = personas_dir / f'gpt-4o-{persona_name}-annotations.xlsx'
        if not gpt_with_persona_file.exists():
            print(f"  Warning: {gpt_with_persona_file} not found, skipping...")
            continue
        
        df_gpt_with = load_annotations(gpt_with_persona_file)
        if df_gpt_with is None:
            continue
        
        gpt_with_persona_annotations = extract_annotations_by_review(df_gpt_with, skip_duplicates=True)
        print(f"  Loaded gpt-4o-{persona_name}: {len(gpt_with_persona_annotations)} reviews")
        
        # Find common review IDs (identical reviews across all files)
        common_ids = set(persona_annotations.keys())
        common_ids = common_ids.intersection(set(gpt_with_persona_annotations.keys()))
        
        # Also intersect with GPT without persona IDs
        for gpt_ann in gpt_no_persona_all:
            common_ids = common_ids.intersection(set(gpt_ann.keys()))
        
        if len(common_ids) == 0:
            print(f"  Warning: No common review IDs found, skipping...")
            continue
        
        print(f"  Common review IDs (identical reviews): {len(common_ids)}")
        print(f"  Note: Only using reviewIds that match across all files (persona, gpt-with-persona, and all gpt-without-persona)")
        
        # Calculate similarity: Persona vs GPT-with-persona
        print(f"\n  Calculating similarities...")
        similarities_with = []
        for review_id in common_ids:
            sim = jaccard_similarity(
                persona_annotations[review_id],
                gpt_with_persona_annotations[review_id]
            )
            similarities_with.append(sim)
        
        # Calculate similarity: Persona vs GPT-without-persona (average across all runs)
        similarities_without = []
        for review_id in common_ids:
            # Average similarity across all GPT-no-persona runs
            sims = []
            for gpt_ann in gpt_no_persona_all:
                sim = jaccard_similarity(
                    persona_annotations[review_id],
                    gpt_ann[review_id]
                )
                sims.append(sim)
            avg_sim = np.mean(sims)
            similarities_without.append(avg_sim)
        
        # Calculate statistics
        stats_with = {
            'mean': np.mean(similarities_with),
            'std': np.std(similarities_with),
            'min': np.min(similarities_with),
            'max': np.max(similarities_with)
        }
        
        stats_without = {
            'mean': np.mean(similarities_without),
            'std': np.std(similarities_without),
            'min': np.min(similarities_without),
            'max': np.max(similarities_without)
        }
        
        print(f"\n  " + "-"*76)
        print(f"  RESULTS for {persona_name}:")
        print(f"  " + "-"*76)
        print(f"\n  Similarity: {persona_name} vs GPT-4o WITH persona pattern")
        print(f"    Mean: {stats_with['mean']:.4f} (std: {stats_with['std']:.4f})")
        print(f"    Range: [{stats_with['min']:.4f}, {stats_with['max']:.4f}]")
        
        print(f"\n  Similarity: {persona_name} vs GPT-4o WITHOUT persona pattern")
        print(f"    Mean: {stats_without['mean']:.4f} (std: {stats_without['std']:.4f})")
        print(f"    Range: [{stats_without['min']:.4f}, {stats_without['max']:.4f}]")
        
        difference = stats_with['mean'] - stats_without['mean']
        print(f"\n  Difference (with - without): {difference:.4f}")
        
        results[persona_name] = {
            'with_persona': {
                'mean': float(stats_with['mean']),
                'std': float(stats_with['std']),
                'min': float(stats_with['min']),
                'max': float(stats_with['max'])
            },
            'without_persona': {
                'mean': float(stats_without['mean']),
                'std': float(stats_without['std']),
                'min': float(stats_without['min']),
                'max': float(stats_without['max'])
            },
            'difference': float(difference),
            'num_reviews': int(len(common_ids))
        }
    
    return results


def main():
    """Main function to run the persona-level similarity analysis."""
    # Set up paths
    script_dir = Path(__file__).parent
    personas_dir = script_dir / 'Personas'
    
    if not personas_dir.exists():
        print(f"Error: Personas directory not found at {personas_dir}")
        return
    
    print(f"Working directory: {script_dir}")
    print(f"Personas directory: {personas_dir}\n")
    
    # Run analysis
    results = analyze_persona_similarity(personas_dir)
    
    if results is None or len(results) == 0:
        print("\nNo results to save.")
        return
    
    # Summary with table
    print("\n" + "="*80)
    print("SUMMARY TABLE")
    print("="*80)
    print(f"{'Persona':<10} {'With Persona':<15} {'Without Persona':<18} {'Difference':<15} {'# Reviews':<12}")
    print("-"*80)
    for persona_name, result in results.items():
        print(f"{persona_name:<10} {result['with_persona']['mean']:<15.4f} {result['without_persona']['mean']:<18.4f} {result['difference']:<15.4f} {result['num_reviews']:<12}")
    print("="*80)
    
    # Detailed summary
    print("\n" + "="*80)
    print("DETAILED SUMMARY")
    print("="*80)
    for persona_name, result in results.items():
        print(f"\n{persona_name}:")
        print(f"  Similarity with persona: {result['with_persona']['mean']:.4f} (std: {result['with_persona']['std']:.4f})")
        print(f"  Similarity without persona: {result['without_persona']['mean']:.4f} (std: {result['without_persona']['std']:.4f})")
        print(f"  Difference: {result['difference']:.4f}")
        print(f"  Number of reviews analyzed: {result['num_reviews']}")
    
    # Save results to JSON
    output_file = script_dir / 'persona_similarity_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n" + "="*80)
    print(f"Results saved to: {output_file}")
    print("="*80)


if __name__ == '__main__':
    main()
