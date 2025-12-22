# Variable Evaluation Experiment

This folder contains two experiment scripts:
1. **Individual Variable Evaluation** (`run_experiment.py`): Evaluates the impact of individual variables
2. **Variable Group Evaluation** (`run_group_experiment.py`): Evaluates the impact of variable groups (A-M)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure you have access to Llama 3.2 3B model. You can either:
   - Use the Hugging Face model directly (requires authentication if gated)
   - Download the model locally and provide the local path

## Usage

### Individual Variable Evaluation

Run the experiment for a specific variable:
```bash
python run_experiment.py --variable age
```

This will:
- Load all variables from `SPP_example.json`
- Process all questions from `input.csv`
- Generate responses with all variables → `responses_full_age.csv`
- Generate responses without the `age` variable → `responses_without_age.csv`

### Variable Group Evaluation

Run the experiment for a specific variable group (A-M):
```bash
python run_group_experiment.py --group K
```

This will:
- Load all variables from `SPP_example.json`
- Process all questions from `input.csv`
- Generate responses with all variables → `responses_full_group_K.csv`
- Generate responses without group K variables → `responses_without_group_K.csv`

**Run all groups sequentially:**
```bash
python run_group_experiment.py --all-groups
```

This will automatically run experiments for groups A through M, creating separate output files for each group. The model is loaded once and reused for efficiency.

To see all available groups:
```bash
python run_group_experiment.py --list
```

**Available Groups:**
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

### Random Sampling

Instead of processing all 1000 questions, you can randomly sample a subset directly in the experiment scripts:

```bash
# Sample 100 questions randomly (sampling done automatically)
python run_experiment.py --variable age --sample 100

# Sample 50 questions with a fixed seed (for reproducibility)
python run_experiment.py --variable age --sample 50 --seed 42

# Use current timestamp as seed (different sample each run)
python run_experiment.py --variable age --sample 100 --seed-time

# Group experiments with sampling
python run_group_experiment.py --group K --sample 100 --seed 42
python run_group_experiment.py --all-groups --sample 50 --seed-time
```

**Seed options:**
- `--seed <number>`: Use a specific seed for reproducibility
- `--seed-time`: Use current timestamp as seed (ensures different samples each run)
- No seed: Random sampling without a fixed seed (non-reproducible)

**Note:** The `--sample` option automatically samples questions from the input file. You don't need to use `sample_questions.py` first - the sampling is done internally. The `sample_questions.py` script is optional and mainly useful if you want to create a reusable sampled dataset file.

### Using a Local Model

If you have the model downloaded locally:
```bash
python run_experiment.py --variable age --model /path/to/local/llama-3.2-3b
python run_group_experiment.py --group K --model /path/to/local/llama-3.2-3b
```

### Question Sampling Script (Optional)

The `sample_questions.py` script is optional - you can use `--sample` directly in the experiment scripts. However, if you want to create a reusable sampled dataset file:

```bash
# Sample 100 questions to a file
python sample_questions.py --count 100

# Sample with custom output file and seed
python sample_questions.py --count 50 --output my_sample.csv --seed 42

# Then use the sampled file
python run_experiment.py --variable age --input my_sample.csv
```

### Available Variables

Variables that can be evaluated (from `SPP_example.json`):
- Personal identifiers: `fullName`, `pronouns`, `preferredName`, `signatureQuote`, `imageStyle`, `privacyPreference`
- Demographics: `age`, `genderIdentity`, `ethnicity`, `nationality`, `legalStatus`, `politicalOrientation`
- Language: `primaryLanguages`, `communicationStyle`, `tonePreference`, `languageRegister`, `secondaryLanguage`, `channelPreferences`
- Lifestyle: `chronotype`, `peakProductivity`, `sleepSchedule`, `energyFluctuations`, `preferredMeetingTime`, `primaryHobbies`, etc.
- Education: `educationLevel`, `academicPerformance`, `fieldOfStudy`
- Employment: `currentJob`, `previousJobs`, `roleAuthority`, `workExperience`, `industrySector`, `incomeLevel`, etc.
- Household: `relationshipStatus`, `householdComposition`, `numDependents`, `housingType`, `homeOwnership`, `homeEnvironment`
- Financial: `financialHabits`, `longTermGoals`, `nextPurchase`
- Mobility: `primaryTransport`, `mobilityFrequency`, `mobilityPurpose`, `accessibilityConsiderations`, `mobilityRange`
- Health: `healthStatus`, `chronicConditions`, `disabilityStatus`, `accessibilityNeeds`
- Goals: `shortTermPriorities`, `longTermGoalsPriorities`
- Digital: `deviceOwnership`, `primaryDevice`, `operatingSystem`, `digitalLiteracy`, `securityPractices`, `trustPropensity`, `digitalActivityFrequency`, `techAttitude`
- Skills: `professionalSkills`, `softSkills`, `learningAgility`, `skillMotivation`, `certifications`
- Big Five: `extroversion`, `agreeableness`, `conscientiousness`, `neuroticism`, `openness`

## Output

### Individual Variable Experiment
The script generates two CSV files:
- `responses_full_{variable}.csv`: Responses with all variables included
- `responses_without_{variable}.csv`: Responses with the specified variable removed

### Group Experiment
The script generates two CSV files:
- `responses_full_group_{group}.csv`: Responses with all variables included
- `responses_without_group_{group}.csv`: Responses with the specified group removed

Each file contains:
- `id`: Question ID from input.csv
- `text`: The LLM's persona response (cleaned, no variables or meta-text)

## Notes

- The experiment processes all 1000 questions from `input.csv`
- Progress is printed every 10 questions
- Results are saved incrementally (flushed after each question)
- The model uses GPU if available, otherwise CPU (slower)
