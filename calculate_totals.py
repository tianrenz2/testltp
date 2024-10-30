import sys
from collections import defaultdict

def calculate_totals(file_path):
    totals = defaultdict(int)
    seen_tests = set()

    with open(file_path, 'r') as file:
        for line in file:
            # Split the line by comma and extract values
            parts = line.strip().split(',')
            test_name = parts[0]

            # Skip if the test name has already been seen
            if test_name in seen_tests:
                continue
            
            seen_tests.add(test_name)

            # Process the metrics
            for part in parts[1:]:
                key, value = part.split('=')
                totals[key] += int(value)

    return totals

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python calculate_totals.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    totals = calculate_totals(file_path)

    print("Total counts:")
    for key in ['passed', 'failed', 'broken', 'skipped', 'warnings']:
        print(f"{key}: {totals[key]}")

