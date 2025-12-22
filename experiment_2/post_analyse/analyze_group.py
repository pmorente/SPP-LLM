#!/usr/bin/env python3
"""
Script to analyze group variable impact by comparing responses with and without a variable group.

This script:
1. Reads responses_full_group_X.csv and responses_without_group_X.csv
2. Generates embeddings using three different models (for three dimensions)
3. Calculates euclidean distance, cosine similarity, and pearson correlation
4. Prints results to screen and saves to file
"""

import argparse
import csv
import struct
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict
from scipy.spatial.distance import euclidean
from scipy.stats import pearsonr
from sklearn.metrics.pairwise import cosine_similarity
import sys

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))

from tools.embeddingGenerator import EmbeddingGenerator


# Model configurations for three dimensions
MODELS = {
    'dim_384': {
        'name': 'sentence-transformers/all-MiniLM-L6-v2',
        'dimension': 384
    },
    'dim_768': {
        'name': 'sentence-transformers/all-mpnet-base-v2',
        'dimension': 768
    },
    'dim_1024': {
        'name': 'sentence-transformers/all-roberta-large-v1',
        'dimension': 1024
    }
}


def read_csv_file(file_path: Path) -> Tuple[List[str], List[str]]:
    """Read CSV file with id,text columns and return lists of ids and texts."""
    ids = []
    texts = []
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if 'id' not in reader.fieldnames or 'text' not in reader.fieldnames:
            raise ValueError(f"CSV must have 'id' and 'text' columns. Found: {reader.fieldnames}")
        
        for row in reader:
            if row['id'] and row['text']:
                ids.append(row['id'].strip())
                texts.append(row['text'].strip())
    
    return ids, texts


def save_embeddings_binary(ids: List[str], embeddings: np.ndarray, output_path: Path):
    """Save embeddings to binary file."""
    num_records = len(ids)
    embedding_dim = embeddings.shape[1]
    
    if num_records != embeddings.shape[0]:
        raise ValueError(f"Mismatch: {num_records} IDs but {embeddings.shape[0]} embeddings")
    
    with open(output_path, 'wb') as f:
        # Header
        f.write(b'EMBD')  # Magic number
        f.write(struct.pack('B', 1))  # Version
        f.write(struct.pack('i', num_records))  # Number of records
        f.write(struct.pack('i', embedding_dim))  # Embedding dimension
        
        # Records
        for id_str, embedding in zip(ids, embeddings):
            id_bytes = id_str.encode('utf-8')
            f.write(struct.pack('i', len(id_bytes)))  # ID length
            f.write(id_bytes)  # ID
            f.write(embedding.astype(np.float32).tobytes())  # Embedding


def load_embeddings_binary(file_path: Path) -> Tuple[List[str], np.ndarray]:
    """Load embeddings from binary file."""
    ids = []
    embeddings_list = []
    
    with open(file_path, 'rb') as f:
        # Read header
        magic = f.read(4)
        if magic != b'EMBD':
            raise ValueError("Invalid binary file format")
        
        version = struct.unpack('B', f.read(1))[0]
        num_records = struct.unpack('i', f.read(4))[0]
        embedding_dim = struct.unpack('i', f.read(4))[0]
        
        # Read records
        for _ in range(num_records):
            id_length = struct.unpack('i', f.read(4))[0]
            id_str = f.read(id_length).decode('utf-8')
            embedding = np.frombuffer(f.read(embedding_dim * 4), dtype=np.float32)
            
            ids.append(id_str)
            embeddings_list.append(embedding)
    
    embeddings = np.array(embeddings_list)
    return ids, embeddings


def calculate_metrics(embeddings_full: np.ndarray, embeddings_without: np.ndarray) -> Dict[str, float]:
    """Calculate euclidean, cosine, and pearson metrics between two embedding sets."""
    if embeddings_full.shape != embeddings_without.shape:
        raise ValueError(f"Shape mismatch: {embeddings_full.shape} vs {embeddings_without.shape}")
    
    num_pairs = embeddings_full.shape[0]
    
    # Calculate metrics for each pair
    euclidean_distances = []
    cosine_similarities = []
    pearson_correlations = []
    
    for i in range(num_pairs):
        emb_full = embeddings_full[i]
        emb_without = embeddings_without[i]
        
        # Euclidean distance
        euc_dist = euclidean(emb_full, emb_without)
        euclidean_distances.append(euc_dist)
        
        # Cosine similarity
        cos_sim = cosine_similarity([emb_full], [emb_without])[0][0]
        cosine_similarities.append(cos_sim)
        
        # Pearson correlation
        pearson_corr, _ = pearsonr(emb_full, emb_without)
        pearson_correlations.append(pearson_corr)
    
    # Calculate statistics
    metrics = {
        'euclidean_mean': np.mean(euclidean_distances),
        'euclidean_std': np.std(euclidean_distances),
        'euclidean_min': np.min(euclidean_distances),
        'euclidean_max': np.max(euclidean_distances),
        'cosine_mean': np.mean(cosine_similarities),
        'cosine_std': np.std(cosine_similarities),
        'cosine_min': np.min(cosine_similarities),
        'cosine_max': np.max(cosine_similarities),
        'pearson_mean': np.mean(pearson_correlations),
        'pearson_std': np.std(pearson_correlations),
        'pearson_min': np.min(pearson_correlations),
        'pearson_max': np.max(pearson_correlations),
        'num_pairs': num_pairs
    }
    
    return metrics, {
        'euclidean': euclidean_distances,
        'cosine': cosine_similarities,
        'pearson': pearson_correlations
    }


def analyze_group(group_letter: str, responses_dir: Path, output_dir: Path, 
                  regenerate_embeddings: bool = False, model_key: str = None):
    """Analyze a specific group by comparing full vs without group responses."""
    
    group_letter = group_letter.upper()
    
    # File paths
    full_file = responses_dir / f"responses_full_group_{group_letter}.csv"
    without_file = responses_dir / f"responses_without_group_{group_letter}.csv"
    
    if not full_file.exists():
        raise FileNotFoundError(f"File not found: {full_file}")
    if not without_file.exists():
        raise FileNotFoundError(f"File not found: {without_file}")
    
    print(f"\n{'='*80}")
    print(f"ANALYZING GROUP {group_letter}")
    print(f"{'='*80}")
    
    # Read CSV files
    print(f"\n[1/5] Reading CSV files...")
    ids_full, texts_full = read_csv_file(full_file)
    ids_without, texts_without = read_csv_file(without_file)
    
    print(f"  Full responses: {len(texts_full)} records")
    print(f"  Without group responses: {len(texts_without)} records")
    
    # Match IDs (they should be the same, but verify)
    if ids_full != ids_without:
        print("  Warning: ID lists don't match. Using intersection.")
        common_ids = sorted(set(ids_full) & set(ids_without))
        full_dict = dict(zip(ids_full, texts_full))
        without_dict = dict(zip(ids_without, texts_without))
        ids_full = ids_without = common_ids
        texts_full = [full_dict[id] for id in common_ids]
        texts_without = [without_dict[id] for id in common_ids]
        print(f"  Using {len(common_ids)} common records")
    
    all_results = {}
    
    # Process each dimension/model
    models_to_process = [model_key] if model_key else MODELS.keys()
    
    for model_key_iter in models_to_process:
        model_config = MODELS[model_key_iter]
        dimension = model_config['dimension']
        model_name = model_config['name']
        
        print(f"\n[2/5] Processing dimension {dimension} ({model_key_iter})...")
        print(f"  Model: {model_name}")
        
        # Embeddings directory
        embeddings_dir = output_dir / 'embeddings' / f'dimension_{dimension}'
        embeddings_dir.mkdir(parents=True, exist_ok=True)
        
        full_emb_file = embeddings_dir / f"full_group_{group_letter}.bin"
        without_emb_file = embeddings_dir / f"without_group_{group_letter}.bin"
        
        # Generate or load embeddings
        if regenerate_embeddings or not full_emb_file.exists():
            print(f"  Generating embeddings for full responses...")
            generator = EmbeddingGenerator(model_name)
            embeddings_full, _ = generator.encode(texts_full, mode='batch', batch_size=32)
            save_embeddings_binary(ids_full, embeddings_full, full_emb_file)
            print(f"  Saved to: {full_emb_file}")
        else:
            print(f"  Loading embeddings from: {full_emb_file}")
            ids_loaded, embeddings_full = load_embeddings_binary(full_emb_file)
            if ids_loaded != ids_full:
                print(f"  Warning: ID mismatch, regenerating...")
                generator = EmbeddingGenerator(model_name)
                embeddings_full, _ = generator.encode(texts_full, mode='batch', batch_size=32)
                save_embeddings_binary(ids_full, embeddings_full, full_emb_file)
        
        if regenerate_embeddings or not without_emb_file.exists():
            print(f"  Generating embeddings for without group responses...")
            generator = EmbeddingGenerator(model_name)
            embeddings_without, _ = generator.encode(texts_without, mode='batch', batch_size=32)
            save_embeddings_binary(ids_without, embeddings_without, without_emb_file)
            print(f"  Saved to: {without_emb_file}")
        else:
            print(f"  Loading embeddings from: {without_emb_file}")
            ids_loaded, embeddings_without = load_embeddings_binary(without_emb_file)
            if ids_loaded != ids_without:
                print(f"  Warning: ID mismatch, regenerating...")
                generator = EmbeddingGenerator(model_name)
                embeddings_without, _ = generator.encode(texts_without, mode='batch', batch_size=32)
                save_embeddings_binary(ids_without, embeddings_without, without_emb_file)
        
        # Calculate metrics
        print(f"\n[3/5] Calculating metrics for dimension {dimension}...")
        metrics, detailed_metrics = calculate_metrics(embeddings_full, embeddings_without)
        all_results[model_key_iter] = {
            'metrics': metrics,
            'detailed': detailed_metrics,
            'dimension': dimension
        }
        
        print(f"  Euclidean distance: {metrics['euclidean_mean']:.6f} ± {metrics['euclidean_std']:.6f}")
        print(f"  Cosine similarity: {metrics['cosine_mean']:.6f} ± {metrics['cosine_std']:.6f}")
        print(f"  Pearson correlation: {metrics['pearson_mean']:.6f} ± {metrics['pearson_std']:.6f}")
    
    # Print summary
    print(f"\n[4/5] Summary Results for Group {group_letter}")
    print(f"{'='*80}")
    
    # Create table format
    num_pairs = all_results[list(all_results.keys())[0]]['metrics']['num_pairs']
    
    # Print table to screen
    print(f"\n{'='*120}")
    print(f"RESULTS TABLE - Group {group_letter} (N = {num_pairs})")
    print(f"{'='*120}")
    print(f"{'Dimension':<12} {'Metric':<25} {'Mean ± SD':<20} {'Min':<12} {'Max':<12}")
    print(f"{'-'*120}")
    
    # Table data for saving
    table_lines = [
        f"RESULTS TABLE - Group {group_letter} (N = {num_pairs})",
        "="*120,
        f"{'Dimension':<12} {'Metric':<25} {'Mean ± SD':<20} {'Min':<12} {'Max':<12}",
        "-"*120
    ]
    
    for model_key_iter in sorted(all_results.keys()):
        dim = all_results[model_key_iter]['dimension']
        m = all_results[model_key_iter]['metrics']
        
        # Euclidean Distance row
        mean_sd_str = f"{m['euclidean_mean']:.6f} ± {m['euclidean_std']:.6f}"
        euclidean_row = f"{dim:<12} {'Euclidean Distance':<25} {mean_sd_str:<20} {m['euclidean_min']:>12.6f} {m['euclidean_max']:>12.6f}"
        print(euclidean_row)
        table_lines.append(euclidean_row)
        
        # Cosine Similarity row
        mean_sd_str = f"{m['cosine_mean']:.6f} ± {m['cosine_std']:.6f}"
        cosine_row = f"{'':<12} {'Cosine Similarity':<25} {mean_sd_str:<20} {m['cosine_min']:>12.6f} {m['cosine_max']:>12.6f}"
        print(cosine_row)
        table_lines.append(cosine_row)
        
        # Pearson Correlation row
        mean_sd_str = f"{m['pearson_mean']:.6f} ± {m['pearson_std']:.6f}"
        pearson_row = f"{'':<12} {'Pearson Correlation':<25} {mean_sd_str:<20} {m['pearson_min']:>12.6f} {m['pearson_max']:>12.6f}"
        print(pearson_row)
        table_lines.append(pearson_row)
        
        # Empty row between dimensions
        if model_key_iter != sorted(all_results.keys())[-1]:
            print()
            table_lines.append("")
    
    print(f"{'='*120}\n")
    table_lines.append("="*120)
    table_lines.append("")
    
    # Summary lines for text file
    summary_lines = [
        f"Group: {group_letter}",
        f"Number of pairs: {num_pairs}",
        "",
        "="*120,
        "RESULTS TABLE",
        "="*120,
        ""
    ]
    summary_lines.extend(table_lines)
    
    # Save results to file
    print(f"\n[5/5] Saving results to file...")
    results_dir = output_dir / 'results'
    results_dir.mkdir(parents=True, exist_ok=True)
    results_file = results_dir / f"group_{group_letter}_analysis.txt"
    
    with open(results_file, 'w', encoding='utf-8') as f:
        f.write("="*120 + "\n")
        f.write(f"GROUP {group_letter} ANALYSIS RESULTS\n")
        f.write("="*120 + "\n\n")
        f.write("\n".join(summary_lines))
        f.write("\n" + "="*120 + "\n")
        f.write("Detailed per-pair metrics saved in embeddings directory\n")
        f.write("="*120 + "\n")
    
    print(f"  Results saved to: {results_file}")
    print(f"\n{'='*80}")
    print(f"Analysis complete for Group {group_letter}!")
    print(f"{'='*80}\n")
    
    return all_results


def main():
    parser = argparse.ArgumentParser(
        description="Analyze variable group impact by comparing responses with and without the group",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze_group.py --group K
  python analyze_group.py --group A --regenerate
  python analyze_group.py --group B --model dim_768
        """
    )
    
    parser.add_argument(
        '--group',
        type=str,
        required=True,
        help="Group letter to analyze (A-M)"
    )
    
    parser.add_argument(
        '--responses-dir',
        type=str,
        default=None,
        help="Directory containing response CSV files (default: ./responses)"
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default=None,
        help="Output directory for embeddings and results (default: ./outputs)"
    )
    
    parser.add_argument(
        '--regenerate',
        action='store_true',
        help="Regenerate embeddings even if they exist"
    )
    
    parser.add_argument(
        '--model',
        type=str,
        choices=['dim_384', 'dim_768', 'dim_1024'],
        default=None,
        help="Process only one specific dimension (default: all three)"
    )
    
    args = parser.parse_args()
    
    # Set up directories
    script_dir = Path(__file__).parent
    
    # Default: look for responses in post_analyse/responses, or in evaluate_variable folder
    if args.responses_dir:
        responses_dir = Path(args.responses_dir)
    else:
        # Try post_analyse/responses first, then evaluate_variable folder
        potential_responses = script_dir / 'responses'
        if not potential_responses.exists():
            potential_responses = script_dir.parent / 'evaluate_variable'
        responses_dir = potential_responses
    
    output_dir = Path(args.output_dir) if args.output_dir else script_dir / 'outputs'
    
    if not responses_dir.exists():
        print(f"Error: Responses directory not found: {responses_dir}")
        sys.exit(1)
    
    # Analyze the group
    try:
        analyze_group(
            group_letter=args.group,
            responses_dir=responses_dir,
            output_dir=output_dir,
            regenerate_embeddings=args.regenerate,
            model_key=args.model
        )
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
