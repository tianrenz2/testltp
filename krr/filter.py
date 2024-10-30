input_file = 'ltp-result'  # Replace with your input file name
output_file = 'ltp-result-new'

results = {}

with open(input_file, 'r') as f:
    for line in f:
        if 'unformated' in line:
            continue
        parts = line.strip().split(',')
        test_name = parts[0]
        passed_value = int(parts[1].split('=')[1])

        # Keep the one with the maximum passed value
        if test_name not in results or results[test_name][1] < passed_value:
            results[test_name] = (line.strip(), passed_value)

# Write deduplicated results to the new file
with open(output_file, 'w') as f:
    for result in results.values():
        f.write(result[0] + '\n')

