input_file = 'ltp-result'  # Replace with your actual input file name
output_file = 'ltp-result-new'

# Dictionary to hold the best "passed" value for each test name
results = {}

with open(input_file, 'r') as file:
    for line in file:
        if "unformatted" in line:  # Skip unformatted lines
            continue
        
        parts = line.strip().split(',')
        test_name = parts[0]
        values = {kv.split('=')[0]: int(kv.split('=')[1]) for kv in parts[1:]}

        # Check for the greatest passed value
        if test_name not in results or values['passed'] > results[test_name]['passed']:
            results[test_name] = values

# Write the deduplicated results to the output file, sorted by test name
with open(output_file, 'w') as file:
    for test_name in sorted(results.keys()):  # Sort by test name
        values = results[test_name]
        result_line = f"{test_name}," + ','.join(f"{k}={v}" for k, v in values.items())
        file.write(result_line + '\n')

