import sys

def find_lines_with_x_greater_than_0(file_path, x_param):
    # Open and read the file
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line by commas and create a dictionary from it
            fields = line.strip().split(',')
            stats = {stat.split('=')[0]: int(stat.split('=')[1]) for stat in fields[1:]}
            
            # Check if the specified parameter (X) has a value greater than 0
            if stats.get(x_param, 0) > 0:
                print(line.strip())

if __name__ == '__main__':
    # Get the file name and X parameter from command line arguments
    if len(sys.argv) != 3:
        print("Usage: python script.py <file_path> <X_param>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    x_param = sys.argv[2]
    
    find_lines_with_x_greater_than_0(file_path, x_param)

