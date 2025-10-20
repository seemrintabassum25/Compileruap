# lexicalanalyzer.py

import re

def lexical_analysis(file_path="input.txt"):
    """Reads C code from input.txt and identifies tokens (lexemes)."""
    try:
        with open(file_path, 'r') as file:
            c_code = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return

    # Define sets for different token types
    KEYWORDS = {'int', 'float', 'void', 'if', 'else', 'while', 'for', 'return'}
    OPERATORS = {'+', '-', '*', '/', '=', '>', '<', '==', '!='}
    SEPARATORS = {';', ',', '(', ')', '{', '}'}
    
    # Combined regex pattern for all tokens
    token_specification = [
        ('COMMENT',       r'//.*'),                   # Single-line comments
        ('KEYWORD',       r'\b(int|float|void|if|else|while|for|return)\b'), # Keywords
        ('IDENTIFIER',    r'[a-zA-Z_][a-zA-Z0-9_]*'), # Identifiers (variables, functions)
        ('LITERAL_FLOAT', r'\d+\.\d+'),               # Floating-point numbers
        ('LITERAL_INT',   r'\d+'),                    # Integers
        ('OPERATOR',      r'[+\-*/=><!]{1,2}'),       # Operators
        ('SEPARATOR',     r'[;,(){}]'),               # Separators
        ('SKIP',          r'\s+'),                    # Whitespace (to be ignored)
    ]
    
    # Create the master regex by joining all patterns
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

    print("--- Lexical Analyzer Output ---")
    
    for mo in re.finditer(tok_regex, c_code):
        kind = mo.lastgroup
        value = mo.group(kind)
        
        if kind == 'SKIP':
            continue
        elif kind == 'COMMENT':
            # Optionally print comments, but usually ignored in lexical analysis output
            # print(f"COMMENT:   {value}")
            continue
        elif kind == 'KEYWORD':
            print(f"KEYWORD:   '{value}'")
        elif kind == 'OPERATOR':
            print(f"OPERATOR:  '{value}'")
        elif kind == 'SEPARATOR':
            print(f"SEPARATOR: '{value}'")
        elif kind == 'IDENTIFIER':
            # Check if an identifier is actually a keyword
            if value in KEYWORDS:
                print(f"KEYWORD:   '{value}'")
            else:
                print(f"ID:        '{value}'")
        elif kind.startswith('LITERAL'):
             print(f"LITERAL:   '{value}' ({kind.split('_')[1]})")
        else:
            print(f"ERROR:     Unexpected character: '{value}'")

if __name__ == "__main__":
    lexical_analysis()