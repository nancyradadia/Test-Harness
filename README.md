# Python Utilities Test Harness

## Name: Nancy Radadia 
nradadia@stevens.edu

## URL: 
https://github.com/nancyradadia/Test-Harness.git

## Time Spent 
An estimate of 48 hours were spent on this project.

## Description

This repository contains a test harness designed to validate the functionality of three Python utilities: `wc.py`, `csvsum.py` and `gron.py`. The `csvsum.py` sums specified columns from a CSV file, while `gron.py` converts JSON data into Gron format for easier parsing and querying and `wc.py` counts tells the number of characters, words, and lines in that file. The test harness includes a suite of test cases to ensure the correctness of these utilities.


## Project Structure
```
Test-Harness/
│
├── .github/                  # GitHub-specific configurations and workflows
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

```zsh
git clone https://github.com/nancyradadia/Test-Harness.git
```

Install the required dependencies:

```zsh
pip install -r requirements.txt
```
    

## Word Count Utility (wc.py)

The `wc.py` utility is a Python implementation of the classic Unix `wc` command. It provides a quick way to count the number of lines, words, and characters in a text file. The script can read input from standard input (STDIN).

### Implementation
The utility is written in Python and utilizes the built-in `argparse` library for argument parsing. It defines functions for counting text components and processing files, handling different edge cases like whether a file ends with a newline.

Functionality includes:
- Counting lines, words, and characters.
- Handling multiple files.
- Reading from STDIN when no file is provided.
- Customizing output to display counts of lines, words, and/or characters as required.

To count words, characters and lines for a file:

```zsh
python3 wc.py <input_file>
```

For Example:

wc.1.in
```txt
Hello
This is Nancy
This is a test file
```

wc.out
```
3   9   39   wc.1.in
```


## CSV Column Sum Utility (`csvsum.py`)

### Description
The `csvsum.py` script is a Python utility for summing numerical data in specified columns of a CSV file. It allows for the selection of columns and the precision of the sum's output, making it a versatile tool for quick calculations directly from the command line.

### Implementation
This utility leverages Python's built-in `csv` module to read and process CSV files. It supports:
- Summing multiple specified columns.
- Setting precision for floating-point sums.
- Reading from a file or standard input (STDIN).
- Robust error handling for non-numeric data and invalid column indices.

To sum columns in a CSV file:

```zsh
python3 csvsum.py <input_file> -c <column_number> <column_number> ... -p <precision>
```

For example:

csvsum.1.in
```txt
1.51, 4.53
4.60, 8.90
```

csvsum.out (for column 0 and 1 and precesion 2)
```
Column 0 sum: 6.11
Column 1 sum: 13.43
```


### JSON to Gron Format Utility (`gron.py`)

### Description
The `gron.py` script is a utility that converts JSON data into Gron format, which makes JSON searchable using grep without losing the structural hints. The utility processes either a JSON file or input provided via standard input (STDIN).

### Implementation
`gron.py` uses Python's `json` module for parsing JSON data and argparse for command-line interface creation. The script:
- Converts JSON objects and arrays into a series of assignment expressions in Gron format.
- Recursively processes nested JSON structures.
- Sorts object keys to produce deterministic and consistent output.


To convert JSON to Gron format:

```zsh
python3 gron.py <input_file>
```

For example:

gron.1.in
```json
{"menu": {
  "id": "file",
  "value": "File",
  "popup": {
    "menuitem": [
      {"value": "New", "onclick": "CreateNewDoc()"},
      {"value": "Open", "onclick": "OpenDoc()"},
      {"value": "Close", "onclick": "CloseDoc()"}
    ]
  }
}}
```

gron.1.out
```
json = {};
json.menu = {};
json.menu.id = "file";
json.menu.popup = {};
json.menu.popup.menuitem = [];
json.menu.popup.menuitem[0] = {};
json.menu.popup.menuitem[0].onclick = "CreateNewDoc()";
json.menu.popup.menuitem[0].value = "New";
json.menu.popup.menuitem[1] = {};
json.menu.popup.menuitem[1].onclick = "OpenDoc()";
json.menu.popup.menuitem[1].value = "Open";
json.menu.popup.menuitem[2] = {};
json.menu.popup.menuitem[2].onclick = "CloseDoc()";
json.menu.popup.menuitem[2].value = "Close";
json.menu.value = "File";
```

## Extensions Implemented

1. Multiple files for wc.py

   When provided with more than one file, it will output the counts for each file individually and also provide a cumulative total for all files.

   ### Implementation
   
   The script parses command-line arguments using the `argparse` library to determine the requested counts and files to process.
   - It iterates over each file, collecting the required counts based on the provided flags.
   - If multiple files are specified, it maintains a running total of each count, which is displayed after the individual file counts.

   ### Testing: 
   ```zsh
   python3 wc.py <input file 1> <input file 2> ....
   ```

   For Example:

   ```zsh
   python3 wc.py wc.1.in wc.2.in 
   ```
   Output:
   ```
   3    9    39   .\test\wc.1.in
   1    2    12   .\test\wc.2.in
   4    11   51     total
   ```

2. Flags for wc.py

   The utility also includes flags to control which counts are displayed. The flags `-l`, `-w`, and `-c` correspond to line counts, word counts, and character counts, respectively. These flags can be combined to display any subset of the counts.

   ### Implementation:
   - The script parses command-line arguments using the `argparse` library to determine the requested counts and files to process.
   - It iterates over each file, collecting the required counts based on the provided flags.
   - For output control, the script checks which flags are active and selectively adds the corresponding counts to the output.
    
   ### Testing: 
   ```zsh
   python3 wc.py <flags> <input file>
   ```

   For Example:

   ```zsh
   python3 wc.py -lc wc.1.in
   ```
   Output:
   ```
   3     39     wc.1.in
   ```

3. Timeout for `gron.py`

    For timeout, the script checks for the timeout value in the test file and if it is present, it will set the timeout for the command. If the command does not finish in the specified time, it will terminate the command and return a timeout error.

    ### Implementation:
    - The script parses the test file to check if the timeout value is present.
    - If the timeout value is present, it will set the timeout for the command.
    - If the command does not finish in the specified time, it will terminate the command and return a timeout error.
    - If the command finishes before the timeout, it will return the output of the command.
    - If the timeout value is not present, it will run the command without a timeout.

    To test timeout, the test file should have a timeout value in the following format:

    For example, `gron.1.timeout` is as follows:
    ```
    0.1
    ```
    To check for timeout error, reduce the value to 0.00001 or 0.000001. It will return a timeout error.

    Note:
    - Timeout has been implemented for all the utilities; but has been used and tested only for `gron.py` given the increasing complexity of `test.py`.
    -  The timeout value is in seconds

## Testing

The `test.py` script serves as the testing framework for verifying the functionality of the all the implemented utilities. It automates the process of running tests, comparing the actual output against expected output, and summarizing the results.

To run the test harness:
```zsh
python test.py
```
### Implementation
The test.py contains different test cases implemented for all three programs along with extensions.
1. The test.py file looks for `(program.in)` in the \test directory
2. For each test, it runs the program with input from STDIN and compares the output with the expected output ` (PROG.NAME.out)` and it looks for `(PROG.NAME.FLAG.out)` to test extensions and csvsum tests.
3. It writes summary of all tests, including passed, failed, and skipped tests in test_results.txt.


## Bugs 

There no known bugs or error in this code.

## Issues Encountered

One challenging issue encountered during the development of this testing framework was the management of command line arguments for different programs. The need to accommodate various flags and extensions for each program posed a significant complexity. Initially, the goal was to design a single, universal function capable of handling all programs regardless of their argument specifications. 

However, due to the diverse nature of the command line interfaces and output formats of each utility, this approach proved to be impractical. Ultimately, the solution required the implementation of distinct functions tailored to each program's unique argument and flag handling. This ensured accurate testing and reliable results but at the expense of having a more unified testing function.


