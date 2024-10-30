# Open the file and read its contents
with open('ltp-result', 'r') as file:
    for line in file:
        # Split the line by commas
        fields = line.strip().split(',')

        # Iterate through each field and check for 'skipped'
        for field in fields:
            if 'skipped=' in field:
                # Extract the skipped value and check if it's greater than 0
                skipped_value = int(field.split('=')[1])
                if skipped_value > 0:
                    print(line.strip())

