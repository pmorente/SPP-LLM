"""
Experiment script to evaluate variable impact on LLM persona responses.

This script:
1. Loads persona variables from SPP_example.json
2. Uses Hugging Face to load Llama 3.2 3B model locally
3. Processes all questions from input.csv
4. Generates responses with full variable set and with one variable removed
5. Saves results to separate output files
"""

import json
import csv
import argparse
import os
import re
import time
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# System prompt template (ultra-simple for small Llama 3.2 3B)
SYSTEM_PROMPT = """You are this person. Answer questions naturally as they would.

Person details:
{variables}

Remember: Answer ONLY as this person would. No explanations, no variable lists, just their answer."""


def format_variables(variables_dict):
    """Format variables dictionary into a readable string for the prompt."""
    formatted = []
    for key, value in variables_dict.items():
        formatted.append(f"{key}: {value}")
    return "\n".join(formatted)


def load_model(model_name="meta-llama/Llama-3.2-3B-Instruct"):
    """Load the Llama 3.2 3B model and tokenizer."""
    print(f"Loading model: {model_name}")
    print("This may take a few minutes on first run...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None,
        low_cpu_mem_usage=True
    )
    
    if not torch.cuda.is_available():
        model = model.to("cpu")
    
    print("Model loaded successfully!")
    return model, tokenizer


def clean_response(text):
    """Aggressively clean the response to extract only the persona's answer."""
    # Remove common artifacts
    text = text.strip()
    
    # Remove variable tags and content between them
    text = re.sub(r'</?variables>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'</?system_prompt>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'</?answer>', '', text, flags=re.IGNORECASE)
    
    # Remove lines that look like variable definitions (key: value patterns at start)
    lines = text.split('\n')
    cleaned_lines = []
    skip_next = False
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        
        # Skip lines that are clearly variable definitions
        if ':' in line and any(keyword in line.lower() for keyword in [
            'personality', 'traits', 'big five', 'openness', 'conscientiousness',
            'extraversion', 'agreeableness', 'neuroticism', 'variables', 'personalitytype',
            'personalitytraits', 'cooperation', 'temperament', 'emotional intelligence'
        ]):
            continue
        
        # Skip meta-commentary
        if any(phrase in line.lower() for phrase in [
            'note:', '(note:', 'please,', 'please help', 'i am', 'i\'m sitting',
            'the variables are', 'internalized', 'respond as', 'as margaret'
        ]):
            # But keep if it's clearly part of the answer
            if not any(meta in line.lower() for meta in ['variables', 'internalized', 'respond as margaret']):
                cleaned_lines.append(line)
            continue
        
        # Skip incomplete fragments (single words or very short phrases that look like artifacts)
        if len(line.split()) <= 2 and line.endswith('.') and not any(char.isupper() for char in line):
            # Might be an artifact like "comforting." or "too restrictive."
            if not line[0].isupper():
                continue
        
        cleaned_lines.append(line)
    
    result = ' '.join(cleaned_lines).strip()
    
    # Remove trailing incomplete sentences/fragments
    if result.endswith('>') or result.endswith('</'):
        result = result.rstrip('>').rstrip('</').strip()
    
    # If result is too short or looks like artifacts, return empty
    if len(result.split()) < 3:
        return ""
    
    return result


def generate_response(model, tokenizer, system_prompt, user_question, max_new_tokens=256):
    """Generate a response from the model - ultra-simple approach for small models."""
    # Just the question, nothing else
    user_content = user_question.strip()

    # Use the tokenizer's chat template if available (for Llama 3.2)
    if hasattr(tokenizer, "apply_chat_template") and tokenizer.chat_template is not None:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ]
        formatted_prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
    else:
        # Fallback formatting for Llama 3.2 Instruct
        formatted_prompt = (
            f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
            f"{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
            f"{user_content}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        )
    
    inputs = tokenizer(formatted_prompt, return_tensors="pt", truncation=True, max_length=2048)
    
    if torch.cuda.is_available():
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
    else:
        inputs = {k: v.to("cpu") for k, v in inputs.items()}
    
    # Set pad token if not set
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # Stop sequences to prevent unwanted continuation
    stop_sequences = ["</variables>", "</system_prompt>", "<variables>", "PersonalityType:", 
                      "Big Five", "PersonalityTraits:", "Note:", "(Note:"]
    stop_ids = []
    for seq in stop_sequences:
        ids = tokenizer.encode(seq, add_special_tokens=False)
        if ids:
            stop_ids.extend(ids)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
            # Try to stop early on unwanted patterns
            repetition_penalty=1.2,
        )
    
    # Decode only the generated tokens (not the input)
    generated_tokens = outputs[0][inputs["input_ids"].shape[1] :]
    response = tokenizer.decode(generated_tokens, skip_special_tokens=True)
    
    # Clean the response aggressively
    cleaned = clean_response(response)
    return cleaned


def run_experiment(variable_to_remove=None, model_name="meta-llama/Llama-3.2-3B-Instruct", 
                   input_file="input.csv", sample_count=None, seed=None):
    """Run the experiment comparing responses with and without a variable.
    
    Args:
        variable_to_remove: Variable name to remove (None for baseline)
        model_name: Hugging Face model name or path
        input_file: Input CSV file with questions
        sample_count: If provided, randomly sample this many questions
        seed: Random seed for sampling (for reproducibility)
    """
    
    # Load variables
    script_dir = Path(__file__).parent
    variables_path = script_dir / "SPP_example.json"
    input_path = script_dir / input_file
    
    if not variables_path.exists():
        print(f"Error: {variables_path} not found")
        return
    
    if not input_path.exists():
        print(f"Error: {input_path} not found")
        return
    
    print(f"Loading variables from {variables_path}")
    try:
        with open(variables_path, 'r', encoding='utf-8') as f:
            all_variables = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {variables_path}: {e}")
        return
    
    # Create variables without the specified variable
    if variable_to_remove:
        if variable_to_remove not in all_variables:
            print(f"Error: Variable '{variable_to_remove}' not found in SPP_example.json")
            print(f"Available variables: {', '.join(sorted(all_variables.keys()))}")
            return
        variables_without = {k: v for k, v in all_variables.items() if k != variable_to_remove}
        print(f"Evaluating variable: {variable_to_remove}")
        print(f"Variables with: {len(all_variables)}")
        print(f"Variables without: {len(variables_without)}")
    else:
        variables_without = all_variables
        print("No variable specified for removal - running baseline comparison")
    
    # Load model
    model, tokenizer = load_model(model_name)
    
    # Prepare prompts
    variables_full_str = format_variables(all_variables)
    variables_reduced_str = format_variables(variables_without)
    
    prompt_full = SYSTEM_PROMPT.format(variables=variables_full_str)
    prompt_reduced = SYSTEM_PROMPT.format(variables=variables_reduced_str)
    
    # Read questions
    print(f"Loading questions from {input_path}")
    questions = []
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'id' in row and 'text' in row:
                    questions.append(row)
                else:
                    print(f"Warning: Row missing 'id' or 'text' column: {row}")
    except Exception as e:
        print(f"Error reading {input_path}: {e}")
        return
    
    # Random sampling if requested
    if sample_count is not None:
        import random
        if seed is not None:
            random.seed(seed)
            print(f"Using random seed: {seed}")
        
        total = len(questions)
        if sample_count > total:
            print(f"Warning: Requested {sample_count} questions but only {total} available. Using all questions.")
        else:
            questions = random.sample(questions, sample_count)
            questions.sort(key=lambda x: int(x['id']))  # Sort by ID
            print(f"Randomly sampled {len(questions)} questions from {total} total")
    
    print(f"Processing {len(questions)} questions...")
    
    # Prepare output files
    if variable_to_remove:
        output_full = script_dir / f"responses_full_{variable_to_remove}.csv"
        output_reduced = script_dir / f"responses_without_{variable_to_remove}.csv"
    else:
        output_full = script_dir / "responses_full_baseline.csv"
        output_reduced = script_dir / "responses_reduced_baseline.csv"
    
    # Process questions
    with open(output_full, 'w', newline='', encoding='utf-8') as f_full, \
         open(output_reduced, 'w', newline='', encoding='utf-8') as f_reduced:
        
        writer_full = csv.writer(f_full)
        writer_reduced = csv.writer(f_reduced)
        
        # Write headers: id + text (persona-only response)
        writer_full.writerow(['id', 'text'])
        writer_reduced.writerow(['id', 'text'])
        
        for i, question_row in enumerate(questions, 1):
            question_id = question_row['id']
            question_text = question_row['text']
            
            print(f"Processing question {i}/{len(questions)}: {question_text[:50]}...")
            
            try:
                # Generate response with full variables
                response_full = generate_response(model, tokenizer, prompt_full, question_text)
                writer_full.writerow([question_id, response_full])
                f_full.flush()
                
                # Generate response without the variable
                response_reduced = generate_response(model, tokenizer, prompt_reduced, question_text)
                writer_reduced.writerow([question_id, response_reduced])
                f_reduced.flush()
            except Exception as e:
                print(f"Error processing question {question_id}: {e}")
                # Write error message to both files
                error_msg = f"ERROR: {str(e)}"
                writer_full.writerow([question_id, error_msg])
                writer_reduced.writerow([question_id, error_msg])
                f_full.flush()
                f_reduced.flush()
                continue
            
            if i % 10 == 0:
                print(f"Progress: {i}/{len(questions)} questions completed")
    
    print(f"\nExperiment completed!")
    print(f"Full variable responses saved to: {output_full}")
    print(f"Reduced variable responses saved to: {output_reduced}")


def main():
    parser = argparse.ArgumentParser(
        description="Run variable evaluation experiment on LLM persona responses"
    )
    parser.add_argument(
        "--variable",
        type=str,
        default=None,
        help="Variable name to remove for evaluation (e.g., 'age', 'extroversion')"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="meta-llama/Llama-3.2-3B-Instruct",
        help="Hugging Face model name or path (default: meta-llama/Llama-3.2-3B-Instruct)"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="input.csv",
        help="Input CSV file with questions (default: input.csv)"
    )
    parser.add_argument(
        "--sample",
        type=int,
        default=None,
        help="Randomly sample this many questions instead of using all (optional)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for sampling (for reproducibility, optional)"
    )
    parser.add_argument(
        "--seed-time",
        action="store_true",
        help="Use current timestamp as random seed (ensures different samples each run)"
    )
    
    args = parser.parse_args()
    
    # If seed-time is specified, use current timestamp
    seed = args.seed
    if args.seed_time:
        seed = int(time.time())
        print(f"Using current time as seed: {seed}")
    
    run_experiment(
        variable_to_remove=args.variable, 
        model_name=args.model,
        input_file=args.input,
        sample_count=args.sample,
        seed=seed
    )


if __name__ == "__main__":
    main()
