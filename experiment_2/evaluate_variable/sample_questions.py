"""
Script to randomly sample X questions from the input.csv dataset.

Usage:
    python sample_questions.py --count 100
    python sample_questions.py --count 50 --output sampled_questions.csv
"""

import csv
import argparse
import random
from pathlib import Path


def sample_questions(input_file, output_file, count, seed=None):
    """Randomly sample count questions from input_file and save to output_file."""
    
    if seed is not None:
        random.seed(seed)
        print(f"Using random seed: {seed}")
    
    # Read all questions
    questions = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'id' in row and 'text' in row:
                questions.append(row)
    
    total_questions = len(questions)
    print(f"Total questions in dataset: {total_questions}")
    
    if count > total_questions:
        print(f"Warning: Requested {count} questions but only {total_questions} available. Using all questions.")
        count = total_questions
    
    # Randomly sample
    sampled = random.sample(questions, count)
    
    # Sort by id to maintain some order
    sampled.sort(key=lambda x: int(x['id']))
    
    # Write sampled questions
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'text'])
        for q in sampled:
            writer.writerow([q['id'], q['text']])
    
    print(f"Sampled {len(sampled)} questions and saved to {output_file}")
    print(f"Question IDs: {', '.join([q['id'] for q in sampled[:10]])}{'...' if len(sampled) > 10 else ''}")


def main():
    parser = argparse.ArgumentParser(
        description="Randomly sample X questions from input.csv"
    )
    parser.add_argument(
        "--count",
        type=int,
        required=True,
        help="Number of questions to sample"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="input.csv",
        help="Input CSV file (default: input.csv)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output CSV file (default: input_sampled_{count}.csv)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility (optional)"
    )
    
    args = parser.parse_args()
    
    script_dir = Path(__file__).parent
    input_path = script_dir / args.input
    
    if not input_path.exists():
        print(f"Error: {input_path} not found")
        return
    
    if args.output:
        output_path = script_dir / args.output
    else:
        output_path = script_dir / f"input_sampled_{args.count}.csv"
    
    sample_questions(input_path, output_path, args.count, args.seed)


if __name__ == "__main__":
    main()
