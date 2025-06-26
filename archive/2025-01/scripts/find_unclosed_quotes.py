#!/usr/bin/env python3
"""Find unclosed quotes in Python file"""

def find_unclosed_quotes(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    in_triple_quote = False
    triple_quote_start = None
    
    for i, line in enumerate(lines, 1):
        # Count triple quotes in line
        count = line.count('"""')
        
        if count > 0:
            if not in_triple_quote:
                if count % 2 == 1:
                    in_triple_quote = True
                    triple_quote_start = i
                    print(f"Triple quote opened at line {i}: {line.strip()}")
            else:
                if count % 2 == 1:
                    in_triple_quote = False
                    print(f"Triple quote closed at line {i}: {line.strip()}")
                else:
                    print(f"WARNING: Even number of triple quotes while inside string at line {i}")
    
    if in_triple_quote:
        print(f"\nERROR: Unclosed triple quote starting at line {triple_quote_start}")
        return triple_quote_start
    else:
        print("\nAll triple quotes are properly closed")
        return None

if __name__ == "__main__":
    find_unclosed_quotes("/home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/test_result_verifier.py")