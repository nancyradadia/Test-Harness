import subprocess
import os

def run_test(input_file, expected_output_file, arg_mode=False):
    if arg_mode:
        cmd = ['python', 'prog/wc.py', input_file]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
        actual_output, _ = process.communicate()
    else:
        with open(input_file, 'r') as file:
            input_text = file.read()
        cmd = ['python', 'prog/wc.py']
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
        actual_output, _ = process.communicate(input=input_text)

    with open(expected_output_file, 'r') as file:
        expected_output = file.read().strip()

    return actual_output.strip() == expected_output

def main():
    test_dir = 'test/'
    test_files = [f for f in os.listdir(test_dir) if f.endswith('.in')]
    total_tests = failed_tests = 0

    with open('test_results.txt', 'w') as result_file:
        for test_file in test_files:
            base_name = test_file[:-3]
            input_file = test_dir + test_file
            expected_output_file = test_dir + base_name + '.out'
            expected_arg_output_file = test_dir + base_name + '.arg.out'

            total_tests += 1
            if not run_test(input_file, expected_output_file):
                result_file.write(f"FAIL: {base_name} failed (STDIN mode)\n")
                failed_tests += 1

            if os.path.exists(expected_arg_output_file):
                total_tests += 1
                if not run_test(input_file, expected_arg_output_file, arg_mode=True):
                    result_file.write(f"FAIL: {base_name} failed (Argument mode)\n")
                    failed_tests += 1

        result_file.write(f"\nOK: {total_tests - failed_tests}\n")
        result_file.write(f"Failed: {failed_tests}\n")
        result_file.write(f"Total: {total_tests}\n")

if __name__ == "__main__":
    main()
