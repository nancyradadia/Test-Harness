import argparse
import sys


def count_text(text):
    """
    Count lines, words, and characters in a given text string.

    Parameters:
    text (str): The text to be counted.

    Returns:
    tuple: A tuple containing the counts of lines, words, and characters.
    """

    lines = text.count('\n') + (not text.endswith('\n') and text != '')
    words = len(text.split())
    characters = len(text)
    return lines, words, characters


def process_file(file_name):
    """
    Process a file to count its lines, words, and characters.

    Parameters:
    file_name (str): The name of the file to be processed.

    Returns:
    tuple: A tuple containing the counts of lines, words, and characters, or None if an error occurs.
    """
    try:
        with open(file_name, 'r') as file:
            text = file.read()
            return count_text(text)
    except Exception as e:
        print(f"Error processing {file_name}: {e}", file=sys.stderr)
        return None


def main():
    """
    The main function to parse arguments and execute the word count functionality.
    """
    try:

        parser = argparse.ArgumentParser(description='Word Count Utility')
        parser.add_argument('files', nargs='*', help='Files to process')
        parser.add_argument(
            '-l', '--lines', action='store_true', help='Count lines only')
        parser.add_argument(
            '-w', '--words', action='store_true', help='Count words only')
        parser.add_argument(
            '-c', '--chars', action='store_true', help='Count characters only')
        args = parser.parse_args()

        if args.files:
            total_lines = total_words = total_chars = 0
            for file_name in args.files:
                counts = process_file(file_name)
                if counts:
                    lines, words, chars = counts
                    total_lines += lines
                    total_words += words
                    total_chars += chars
                    print_output(lines, words, chars, file_name, args)

            if len(args.files) > 1:
                print_output(total_lines, total_words,
                             total_chars, 'total', args)

        else:
            stdin_text = sys.stdin.read()
            lines, words, chars = count_text(stdin_text)
            print_output(lines, words, chars, '', args)
        sys.exit(0)

    except Exception as e:
        sys.exit(1)  # Exit with error status if an exception occurs


def print_output(lines, words, chars, label, args):
    """
    Print the count output formatted based on the specified arguments.

    Parameters:
    lines (int): Number of lines.
    words (int): Number of words.
    chars (int): Number of characters.
    label (str): Label for the output (filename or 'total').
    args (argparse.Namespace): Parsed command-line arguments.
    """
    outputs = []
    # Determine which counts to output based on the arguments
    if args.lines or not (args.lines or args.words or args.chars):
        outputs.append(str(lines))
    if args.words or not (args.lines or args.words or args.chars):
        outputs.append(str(words))
    if args.chars or not (args.lines or args.words or args.chars):
        outputs.append(str(chars))

    print(' '.join(outputs), end='')

    if label:
        print(f"\t{label}")


if __name__ == "__main__":
    main()
