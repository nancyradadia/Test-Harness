import argparse
import csv
import sys

def sum_csv_columns(file, columns):
    sums = {column: 0 for column in columns}
    column_indices = None

    reader = csv.reader(file)
    for i, row in enumerate(reader):
        if i == 0:
            # Identify column indices
            if all(isinstance(col, str) for col in columns):
                column_indices = [row.index(col) for col in columns]
            else:
                column_indices = columns
        else:
            for idx, col_index in enumerate(column_indices):
                sums[columns[idx]] += float(row[col_index])

    return sums

def main():
    parser = argparse.ArgumentParser(description='Sum specified columns in a CSV file')
    parser.add_argument('file', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='CSV file to process')
    parser.add_argument('columns', nargs='+', help='Column names or indices to sum')
    args = parser.parse_args()

    # Convert column indices to int if possible
    columns = [int(col) if col.isdigit() else col for col in args.columns]

    sums = sum_csv_columns(args.file, columns)
    for col, sum_val in sums.items():
        print(f"Sum of column '{col}': {sum_val}")

if __name__ == "__main__":
    main()
