import sys
import re

def count_unique_bracket_words(file_path):
    unique_words = set()
    
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r'\[(.*?)\]', line)
            if match:
                unique_words.add(match.group(1))
    
    return len(unique_words)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python count_unique_bracket_words.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    unique_count = count_unique_bracket_words(file_path)
    print(f"Number of unique lines based on the word in brackets: {unique_count}")

