import sys
from collections import defaultdict

def find_common_lines(testcase_file, *other_files):
    line_counts = defaultdict(int)

    # Count occurrences of lines in the other files
    for file_path in other_files:
        with open(file_path, 'r') as f:
            for line in f:
                line_counts[line.strip()] += 1

    # Filter lines that exist in more than one file
    common_lines = {line for line, count in line_counts.items() if count > 1}

    # Check if common lines exist in the testcase file
    with open(testcase_file, 'r') as f:
        testcase_lines = {line.strip() for line in f}

    # Return common lines that are also in testcase
    result = common_lines.intersection(testcase_lines)
    return result

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python find_common_lines.py <testcase_file> <file1> <file2> <file3>")
        sys.exit(1)

    testcase_file = sys.argv[1]
    other_files = sys.argv[2:5]
    common_lines = find_common_lines(testcase_file, *other_files)

    print("Common lines that exist in more than one file:")
    for line in common_lines:
        print(line)

