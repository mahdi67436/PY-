"""Simple py++ runner."""

import sys
from interpreter import interpret

def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py <file.pypp>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    try:
        with open(filepath, 'r') as f:
            source = f.read()
        interpret(source)
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
