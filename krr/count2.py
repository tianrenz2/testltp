# Initialize dictionaries to store test results
test_results = {}

# Open and read the file
with open('ltp-result', 'r') as file:
    for line in file:
        if "unformated" in line:
            continue
        # Split the line by commas
        fields = line.strip().split(',')
        
        # Extract the test name and stats
        test_name = fields[0]
        stats = {stat.split('=')[0]: int(stat.split('=')[1]) for stat in fields[1:]}
        # Check if the test name already exists, keep the one with the higher passed value
        if test_name not in test_results or stats['passed'] > test_results[test_name]['passed']:
            test_results[test_name] = stats

# Initialize counters for the totals
total_passed = total_failed = total_broken = total_skipped = total_warnings = 0

# Sum the highest values for each test name
for result in test_results.values():
    total_passed += result['passed']
    total_failed += result['failed']
    total_broken += result['broken']
    total_skipped += result['skipped']
    total_warnings += result['warnings']

# Output the totals
print(f"Total Passed: {total_passed}")
print(f"Total Failed: {total_failed}")
print(f"Total Broken: {total_broken}")
print(f"Total Skipped: {total_skipped}")
print(f"Total Warnings: {total_warnings}")

