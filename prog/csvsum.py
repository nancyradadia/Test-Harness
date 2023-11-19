import csv
import sys
import argparse

def sum_columns(csv_file, columns, precision):
    """
    Sum specified columns in a CSV file with given precision.

    Parameters:
    csv_file (file object): The CSV file to process.
    columns (list of int): Indices of the columns to sum.
    precision (int): Number of decimal places for the sum.

    Returns:
    list or str: Sums of the specified columns or an error message.
    """
    sums = [0 for _ in columns]  # Initialize sums for each column
    try:
        reader = csv.reader(csv_file)  # Create a CSV reader
        for row in reader:  # Iterate over each row
            for i, col in enumerate(columns):
                sums[i] += float(row[col])  # Add the value in the specified column
        # Format sums to the specified precision
        sums = [round(sum, precision) for sum in sums]
    except ValueError as e:  # Handle value errors (like converting to float)
        return f"Error: {e}"
    except IndexError as e:  # Handle index errors (column index out of range)
        return f"Error: {e}"
    return sums

def main():
    """
    The main function to parse arguments and execute the column sum functionality.
    """
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='CSV Column Sum Utility')
    
    # Define arguments for the CSV file, column indices, and precision
    parser.add_argument('file', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='CSV file to process')
    parser.add_argument('-c', '--columns', nargs='+', type=int, required=True, help='Column indices to sum (0-indexed)')
    parser.add_argument('-p', '--precision', type=int, default=2, help='Number of decimal places in the sum')
    
    args = parser.parse_args()

    # Perform the column sum operation
    sums = sum_columns(args.file, args.columns, args.precision)
    # Check for errors or print the sums
    if isinstance(sums, str):
        print(sums)  # Print error message
    else:
        for i, sum in enumerate(sums):
            print(f"Column {args.columns[i]} sum: {sum}")  # Print sum for each column

if __name__ == '__main__':
    main()
