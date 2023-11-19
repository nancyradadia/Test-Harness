import os
import subprocess
import sys

# Directory containing test input files
test_dir = 'test/'

# Dictionary mapping program names to their respective command-line flags
program_flags = {
    'wc': ['-l', '-w', '-c']
}

# File to store the results of the tests
results_file = 'test_results.txt'

def run_test(prog, num, input_file, arg_mode, flag=None):
    """
    Execute a test for a specific program with given input and flags.

    Parameters:
    prog (str): Name of the program to test.
    num (int): Identifier for the test case.
    input_file (str): File containing test input.
    arg_mode (bool): Determines if input is passed as an argument to the program.
    flag (str, optional): Additional flag to pass to the program. Defaults to None.

    Returns:
    tuple: Actual output from the program and expected output from the file.
    """
    # Construct the path to the input file
    input_path = os.path.join(test_dir, input_file)

    # Check for a custom timeout setting for the test
    timeout = None
    if os.path.exists(input_path.replace('.in', '.timeout')):
        timeout = float(open(input_path.replace('.in', '.timeout'), 'r').read())

    # Construct the command to run the test program
    cmd = ['python', os.path.join('prog', f'{prog}.py')]

    # Add the input file to the command if in argument mode
    if arg_mode:
        cmd.append(input_path)

    # Add the flag to the command if provided
    if flag:
        cmd.append(flag)

    # Initialize a variable to capture any errors during execution
    err = ''
    # cmd = ' '.join(cmd)

    # Execute the program and capture its output
    try:
        if arg_mode:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            actual_output, err = process.communicate(timeout=timeout)
        else:
            with open(input_path, 'r') as file:
                input_text = file.read()
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            actual_output, err = process.communicate(input=input_text, timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        actual_output = 'Timeout expired'
    
    # Print any errors encountered during execution
    print(err, end='')

    # Determine the path for the expected output file
    output_suffix = '.arg.out' if arg_mode else '.out'
    expected_output_path = input_path.replace('.in', output_suffix) if not flag else input_path.replace('.in', f'.{flag}.out')
    
    # Read the expected output
    with open(expected_output_path, 'r') as file:
        expected_output = file.read().strip()

    # Return the actual output and expected output
    return actual_output.strip(), expected_output

def test_csv_sum(test_file, flag, total_tests, failed_tests):
    """
    Test the 'csvsum' program with a given test file and flag.

    Parameters:
    test_file (str): The test input file name.
    flag (str): Command line flag to be used with the program.
    file (file object): File object to write the test results to.
    total_tests (int): Counter for total number of tests run.
    failed_tests (int): Counter for the number of failed tests.

    Returns:
    tuple: Updated total_tests and failed_tests counters.
    """
    total_tests += 1
    # actual_output, expected_output = run_test(prog='csvsum', num=test_file.split('.')[1], input_file=test_file, arg_mode=True, flag=flag)

    cmd = ['python', os.path.join('prog', 'csvsum.py'), os.path.join(test_dir, test_file), f' {flag}']
    cmd = ' '.join(cmd)
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    actual_output, err = process.communicate(input=flag)

    output_file = os.path.join(test_dir, test_file.replace('.in', f'.{flag}.out'))
    with open(output_file, 'r') as file:
        expected_output = file.read().strip()

    if actual_output.strip() != expected_output.strip():
        with open(results_file, 'a') as file:
            failed_tests += 1
            file.write(f"FAIL: Program: csvsum, Test File: {test_file}, Arg Mode: True, Flag: {flag}\n")
            file.write(f"Expected output: \n{expected_output}\n")
            file.write(f"Actual output: \n{actual_output}\n\n")

    return total_tests, failed_tests

def test_wc_multiple_files(test_files, flag, output_file, total_tests, failed_tests):
    """
    Test the 'wc' program with multiple files extension.

    Parameters:
    test_files (list): List of test file names.
    flag (str): Command line flag to be used with the program.
    output_file (str): Name of the file containing expected output.
    total_tests (int): Counter for total number of tests run.
    failed_tests (int): Counter for the number of failed tests.

    Returns:
    tuple: Updated total_tests, failed_tests, and a string with the test result.
    """
    total_tests += 1

    cmd = ['python', os.path.join('prog', 'wc.py')]
    for i in test_files:
        cmd.append(os.path.join(test_dir, i))
    if flag:
        cmd.append(flag)
    # cmd = ' '.join(cmd)

    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        actual_output, _ = process.communicate()
    except subprocess.TimeoutExpired:
        process.kill()
        actual_output = 'Timeout expired'

    with open(os.path.join(test_dir, output_file), 'r') as file:
        expected_output = file.read().strip()
    
    write_data = ''
    if actual_output.strip() != expected_output.strip():
        failed_tests += 1
        write_data = f"FAIL: Program: wc, Test File: {test_files}, Arg Mode: True, Flag: {flag}\n"
        write_data += f"Expected output: \n{expected_output}\n"
        write_data += f"Actual output: \n{actual_output}\n\n"

    return total_tests, failed_tests, write_data

def main():
    """
    Main function to run all tests and record the results.

    It iterates over all test files, runs tests for different programs, and handles
    special cases like multiple file tests. It writes the results to a file and
    determines the exit status of the script.
    """
    test_files = [f for f in os.listdir(test_dir) if f.endswith('.in')]
    total_tests = failed_tests = skipped_tests = 0

    with open(results_file, 'w') as file:
        for test_file in test_files:
            prog, num = test_file.split('.')[:2]
            
            # we Skip csvsum tests for now as they are handled separately
            if prog == 'csvsum':
                continue

            for arg_mode in [True, False]:
                flags = [None] if arg_mode else program_flags.get(prog, [None])

                for flag in flags:
                    expected_output_file = test_file.replace('.in', '.arg.out' if arg_mode else '.out') if flag is None else test_file.replace('.in', f'.{flag}.out')
                    expected_output_path = os.path.join(test_dir, expected_output_file)

                    if not os.path.exists(expected_output_path):
                        if flag is not None:
                            skipped_tests += 1
                            file.write(f"SKIPPED: Program: {prog}, Test File: {test_file}, Flag: {flag} - Expected output file does not exist.\n")
                            continue

                    total_tests += 1
                    actual_output, expected_output = run_test(prog, num, test_file, arg_mode, flag)
                    if actual_output != expected_output:
                        failed_tests += 1
                        file.write(f"FAIL: Program: {prog}, Test File: {test_file}, Arg Mode: {arg_mode}, Flag: {flag}\n")
                        file.write(f"Expected output: \n{expected_output}\n")
                        file.write(f"Actual output: \n{actual_output}\n\n")

    # Test csvsum separately
    total_tests, failed_tests = test_csv_sum('csvsum.1.in', '-c 0 2', total_tests, failed_tests)
    total_tests, failed_tests = test_csv_sum('csvsum.2.in', '-c 0 3', total_tests, failed_tests)
    total_tests, failed_tests = test_csv_sum('csvsum.3.in', '-c 0 1', total_tests, failed_tests)
    total_tests, failed_tests = test_csv_sum('csvsum.4.in', '-c 0 1 -p 2', total_tests, failed_tests)
    total_tests, failed_tests = test_csv_sum('csvsum.5.in', '-c 0 1', total_tests, failed_tests)

    # Test wc with multiple files
    test_files = ['wc.1.in', 'wc.2.in']
    output_file = 'wc.1.2.out'
    total_tests, failed_tests, write_data = test_wc_multiple_files(test_files, None, output_file, total_tests, failed_tests)
    with open(results_file, 'a') as file:
        file.write(write_data)

        file.write(f"\nTotal tests: {total_tests}\n")
        file.write(f"Unsuccessful tests: {failed_tests}\n")
        file.write(f"Skipped tests: {skipped_tests}\n")
        file.write(f"Passed tests: {total_tests - failed_tests - skipped_tests}\n")

    sys.exit(0 if failed_tests == 0 else 1)

if __name__ == "__main__":
    main()
