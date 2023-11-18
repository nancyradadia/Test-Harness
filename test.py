import subprocess
import sys
import os

test_dir = 'test/'

def run_test(prog, num, input_file, arg_mode=False):
    # print(f"prog: {prog}, num: {num}, test_file: {input_file}, arg_mode: {arg_mode}")
    input_file = test_dir+input_file
    if(arg_mode):
        cmd = ['python', f'prog/{prog}.py', input_file]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
        actual_output, _ = process.communicate()
    else:
        with open(input_file, 'r') as file:
            input_text = file.read()
        cmd = ['python', f'prog/{prog}.py']
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
        actual_output, _ = process.communicate(input=input_text)
    
    expected_output_file = f'{test_dir}{prog}.{num}.out' if arg_mode else f'{test_dir}{prog}.{num}.arg.out'

    with open(expected_output_file, 'r') as file:
        expected_output = file.read().strip()

    # return actual_output.strip() == expected_output
    return actual_output, expected_output

def main():
    
    test_files = [f for f in os.listdir(test_dir) if f.endswith('.in')]
    total_tests = failed_tests = 0

    with open('test_results.txt', 'w') as file:

        for test_file in test_files:
            prog, num = test_file.split('.')[0], test_file.split('.')[1]
            
            # Run the program, one for loop for arg mode = True, one for False
            for arg_mode in [True, False]:
                total_tests += 1
                actual_output, expected_output = run_test(prog, num, test_file, arg_mode)
                if(actual_output.strip() != expected_output):
                    failed_tests += 1
                    file.write(f"FAIL: Program:{prog}, input_file:{prog}.{num}.in, arg mode={arg_mode} \n")
                    file.write(f"Expected output: \n{expected_output}\n")
                    file.write(f"Actual output: \n{actual_output}\n\n")
                    # with open(f'{test_dir}{prog}.{num}.err', 'r') as file:
                    #     file.write(f"Error output: \n{file.read()}\n\n")

        
        file.write(f"\nTotal tests: {total_tests}\n")
        file.write(f"Failed tests: {failed_tests}\n")
        file.write(f"Passed tests: {total_tests - failed_tests}\n")

    
    sys.exit(0 if failed_tests == 0 else 1)

if __name__ == '__main__':
    main()