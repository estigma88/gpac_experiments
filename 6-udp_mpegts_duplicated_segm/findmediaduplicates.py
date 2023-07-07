import re
from collections import Counter

def extract_last_path_part(line):
    pattern = r'"PUT (.+?) HTTP/1\.1"'
    match = re.search(pattern, line)
    if match:
        path = match.group(1)
        last_part = path.split('/')[-1]
        return last_part
    return None

def process_file(filename):
    last_parts = []
    with open(filename, 'r') as file:
        for line in file:
            last_part = extract_last_path_part(line)
            if last_part:
                last_parts.append(last_part)

    duplicates = [part for part, count in Counter(last_parts).items() if count > 1]
    for duplicate in duplicates:
        print(duplicate)

# Example usage
filename = 'logs/access.log'  # Replace with the actual filename
process_file(filename)
