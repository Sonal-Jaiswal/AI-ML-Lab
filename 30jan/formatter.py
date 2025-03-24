import os
import sys
import black

def format_code(file_path):
    try:
        # Check if the file exists
        if not os.path.isfile(file_path):
            print(f"Error: The file {file_path} does not exist.")
            return None
        
        # Read the original code
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Format using Black (fixes indentation and overall formatting)
        formatted_code = black.format_str(code, mode=black.FileMode())

        # Save formatted code to a new file
        formatted_file = file_path.replace('.py', '_formatted.py')
        with open(formatted_file, 'w', encoding='utf-8') as f:
            f.write(formatted_code)
        
        print(f"Formatted code saved to: {formatted_file}")
        return formatted_file
    except Exception as e:
        print(f"Error formatting code: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python formatter.py <file.py>")
    else:
        format_code(sys.argv[1])
