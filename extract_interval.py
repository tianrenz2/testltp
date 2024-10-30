import re

def extract_intervals(formatted_results_file, log_file):
    # Read test names from formatted_results.txt
    with open(formatted_results_file, 'r') as results_file:
        test_names = results_file.readlines()
    
    # Strip whitespace from each test name
    test_names = [name.strip() for name in test_names]

    # Initialize a dictionary to store results
    intervals = {}

    # Read the LOG file
    with open(log_file, 'r') as log:
        log_lines = log.readlines()
        
        # Iterate through each test name
        for test_name in test_names:
            # Create a regex pattern to match the line format
            pattern = re.compile(rf"{re.escape(test_name)} replay passed interval (\d+)")
            for line in log_lines:
                match = pattern.search(line)
                if match:
                    # Extract the value of N
                    N = match.group(1)
                    intervals[test_name] = N
                    break  # Stop searching after the first match

    # Print the results
    for test_name, interval in intervals.items():
        print(f"{test_name}:{interval}")

# Call the function with the file names
extract_intervals('formatted_results.txt', 'LOG')
