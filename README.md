# Python Utilities Test Harness

### Name: Nancy Radadia (nradadia@stevens.edu)

### URL: https://github.com/nancyradadia/Test-Harness.git

### Estimate of hours: 35 hours

### Description of code testing

### Bugs

### Extensions
1. Multiple files for wc.py
2. Timeout for all commands
3. flags for wc.py


# Notes


## Description

This repository contains a test harness designed to validate the functionality of three Python utilities: `wc.py`,`csvsum.py` and `gron.py`. `csvsum.py` sums specified columns from a CSV file, while `gron.py` converts JSON data into Gron format for easier parsing and querying and `wc.py` counts tells the number of characters, words, and lines in that file. The test harness includes a suite of test cases to ensure the correctness of these utilities.

## Project Structure
```
Test-Harness/
│
├── .github/                  # GitHub-specific configurations and workflows
├── env/                      # Environment configurations or scripts
├── prog/                     # Directory containing utility scripts
│   ├── csvsum.py             # Utility to sum columns in a CSV file
│   └── gron.py               # Utility to convert JSON data to Gron format
│
├── test/                     # Test suite with input and expected output files
│   ├── _.in                  # Input test files
│   ├── _.out                 # Expected output test files
│   ├── _.arg.out             # Expected output with arguments
│   └── _.timeout             # Optional timeout configuration for tests
│
├── .gitignore                # Specifies intentionally untracked files to ignore
├── README.md                 # This file
├── requirements.txt          # Python dependencies for the utilities
├── test.py                   # Extension script for additional tests (if applicable)
└── test_results.txt          # Results of the test executions
```



## Installation

Clone the repository to your local machine:

<!-- Add the git repo link here -->

```bash
git clone https://github.com/nancyradadia/Test-Harness.git
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```
    

## Usage

### CSV Column Sum Utility (`csvsum.py`)
To sum columns in a CSV file:

```bash
python3 csvsum.py <input_file> <column_number> <column_number> ...
```

### JSON to Gron Format Utility (`gron.py`)
To convert JSON to Gron format:

```bash
python3 gron.py <input_file>
```

### Word Count Utility (`wc.py`)
To count the number of words in a file:

```bash
python3 wc.py <input_file>
```



## Testing
To run the test harness:
```
python test_extend.py
```