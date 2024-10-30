# Define the input and output file names
input_file = 'ltp-result'  # Replace with your input file name
output_file = 'formatted_results.txt'  # Output file for unformatted lines

# Initialize counters
totals = {
    'passed': 0,
    'failed': 0,
    'broken': 0,
    'skipped': 0,
    'warnings': 0
}

# Set to track counted test names
counted_tests = set()

# List to collect unformatted test names
unformatted_tests = set()

# Read the input file
with open(input_file, 'r') as file:
    for line in file:
        line = line.strip()
        if "unformated report" in line:
            test_name = line.split()[0]  # Get the test name
            unformatted_tests.add(test_name)
            continue  # Skip unformatted lines

        # Process lines with results
        parts = line.split(',')
        test_name = parts[0].strip()
        
        if test_name in counted_tests:
            continue  # Skip already counted test names
        
        counted_tests.add(test_name)  # Mark this test name as counted
        
        for part in parts[1:]:  # Start from the second part
            key_value = part.split('=')
            if len(key_value) == 2:
                key = key_value[0].strip()
                value = int(key_value[1].strip())
                if key in totals:
                    totals[key] += value

# Write unformatted test names to a new file
with open(output_file, 'w') as file:
    for test_name in list(unformatted_tests):
        file.write(test_name + '\n')

# Print the totals
print("Totals:")
print(f"Passed: {totals['passed']}")
print(f"Failed: {totals['failed']}")
print(f"Broken: {totals['broken']}")
print(f"Skipped: {totals['skipped']}")
print(f"Warnings: {totals['warnings']}")
