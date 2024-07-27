import re

# Define the filename
filename = 'art.txt'

# Open the file for reading
with open(filename, 'r') as file:
    # Read the content of the file
    text = file.read()

# Process the content to keep only the part after the period for lines starting with a number followed by a period
lines = text.strip().split('\n')
processed_lines = []
for line in lines:
    # Check if the line is not empty
    if line.strip():
        # Check if the line starts with a number followed by a period
        if re.match(r'^\d+\.', line):
            # Find the first period and keep the text after it
            period_index = line.find('.')
            if period_index != -1:
                processed_lines.append(line[period_index + 1:].strip())
        else:
            # Add lines that don't match the pattern unchanged
            processed_lines.append(line)

# Remove empty lines
processed_lines = [line for line in processed_lines if line.strip()]

# Join the processed lines into a single string
result = '\n'.join(processed_lines)

# Open the file for writing and save the processed content
with open(filename, 'w') as file:
    file.write(result)

print(f"Processed content has been written to {filename}")
