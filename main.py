# main.py - Compiler Phases Integration

import re
import os

# --- 1. Lexical Analyzer Function ---

def lexical_analysis(file_path="input.txt"):
    """Reads C code and identifies tokens (lexemes)."""
    try:
        with open(file_path, 'r') as file:
            c_code = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return

    # Define sets and specification for tokens
    KEYWORDS = {'int', 'float', 'void', 'if', 'else', 'while', 'for', 'return'}
    token_specification = [
        ('COMMENT',       r'//.*'),
        ('KEYWORD_R',     r'\b(int|float|void|if|else|while|for|return)\b'),
        ('IDENTIFIER',    r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('LITERAL_FLOAT', r'\d+\.\d+'),
        ('LITERAL_INT',   r'\d+'),
        ('OPERATOR',      r'[+\-*/=><!]{1,2}'),
        ('SEPARATOR',     r'[;,(){}]'),
        ('SKIP',          r'\s+'),
    ]

    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

    print("\n" + "="*70)
    print("                 PHASE 1: LEXICAL ANALYSIS")
    print("="*70)
    
    tokens_list = []
    
    for mo in re.finditer(tok_regex, c_code):
        kind = mo.lastgroup
        value = mo.group(kind)
        
        if kind == 'SKIP' or kind == 'COMMENT':
            continue
        elif kind == 'KEYWORD_R':
            print(f"KEYWORD:   '{value}'")
            tokens_list.append(('KEYWORD', value))
        elif kind == 'OPERATOR':
            print(f"OPERATOR:  '{value}'")
            tokens_list.append(('OPERATOR', value))
        elif kind == 'SEPARATOR':
            print(f"SEPARATOR: '{value}'")
            tokens_list.append(('SEPARATOR', value))
        elif kind == 'IDENTIFIER':
            if value in KEYWORDS:
                 print(f"KEYWORD:   '{value}'")
                 tokens_list.append(('KEYWORD', value))
            else:
                print(f"ID:        '{value}'")
                tokens_list.append(('ID', value))
        elif kind.startswith('LITERAL'):
             print(f"LITERAL:   '{value}' ({kind.split('_')[1]})")
             tokens_list.append(('LITERAL', value))
        else:
            print(f"ERROR:     Unexpected character: '{value}'")
            
    return tokens_list

# --- 2. Symbol Table Function (Basic) ---

def build_symbol_table(file_path="input.txt"):
    """Scans for variable/function declarations and builds a basic symbol table."""
    try:
        with open(file_path, 'r') as file:
            c_code = file.read()
    except FileNotFoundError:
        return

    DATA_TYPES = ['int', 'float', 'double', 'char', 'void']
    symbol_table = {}
    index = 1
    
    # Simple tokenization for symbol table
    all_tokens = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*|\d+\.\d+|\d+|[+\-*/=;,(){}]', c_code)
    
    i = 0
    while i < len(all_tokens):
        token = all_tokens[i]

        if token in DATA_TYPES:
            data_type = token
            if i + 1 < len(all_tokens):
                identifier = all_tokens[i + 1]
                
                # Check if it's a valid identifier and not already in table
                if identifier not in ['=', ';', '(', ')', '{', '}'] and identifier not in symbol_table:
                    
                    scope = "Variable"
                    # Simple check for function: identifier followed by '('
                    if i + 2 < len(all_tokens) and all_tokens[i+2] == '(':
                        scope = "Function"
                    
                    symbol_table[identifier] = {
                        "Index": index,
                        "Type": data_type,
                        "Scope": scope,
                        "Initial Value": "N/A"
                    }
                    index += 1
        i += 1

    print("\n" + "="*70)
    print("                 PHASE 2: SYMBOL TABLE")
    print("="*70)
    if not symbol_table:
        print("No data type declarations (int, float, etc.) found.")
        return

    print("{:<10} {:<20} {:<10} {:<15} {:<15}".format(
        "Index", "Identifier", "Type", "Scope", "Initial Value"
    ))
    print("-" * 70)

    for name, data in symbol_table.items():
        print("{:<10} {:<20} {:<10} {:<15} {:<15}".format(
            data["Index"], name, data["Type"], data["Scope"], data["Initial Value"]
        ))
    return symbol_table

# --- 3. Three-Address Code (TAC) Function ---

def generate_tac(file_path="input.txt"):
    """Generates Three-Address Code (TAC) for a simple assignment using RPN."""
    try:
        with open(file_path, 'r') as file:
            c_code = file.read().strip()
    except FileNotFoundError:
        return []

    # 1. Extract Target Variable and Expression
    match = re.search(r'(\w+)\s*=\s*(.*);', c_code)
    if not match:
        return []

    target_var = match.group(1)
    expression = match.group(2).strip()

    # Define operators and their precedence
    operators = {'*': 3, '/': 3, '+': 2, '-': 2, '(': 1}
    tokens = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*|\d+\.\d+|\d+|[+\-*/()]', expression)

    # 2. Shunting-Yard Algorithm: Convert to RPN
    op_stack = []
    output_queue = []

    for token in tokens:
        if token not in operators and token != ')':
            output_queue.append(token)
        elif token == '(':
            op_stack.append(token)
        elif token == ')':
            while op_stack and op_stack[-1] != '(':
                output_queue.append(op_stack.pop())
            if op_stack and op_stack[-1] == '(':
                op_stack.pop() 
        elif token in operators:
            while (op_stack and op_stack[-1] != '(' and 
                   operators.get(op_stack[-1], 0) >= operators[token]):
                output_queue.append(op_stack.pop())
            op_stack.append(token)

    while op_stack:
        output_queue.append(op_stack.pop()) 

    # 3. Generate TAC from RPN
    tac_instructions = []
    temp_count = 1
    operand_stack = []

    for token in output_queue:
        if token not in operators:
            operand_stack.append(token)
        elif token in operators:
            op2 = operand_stack.pop()
            op1 = operand_stack.pop()
            
            temp_var = f"t{temp_count}"
            tac_instructions.append(f"{temp_var} = {op1} {token} {op2}")
            operand_stack.append(temp_var)
            temp_count += 1
            
    if operand_stack:
        final_temp = operand_stack.pop()
        tac_instructions.append(f"{target_var} = {final_temp}")

    print("\n" + "="*70)
    print("             PHASE 3: THREE-ADDRESS CODE (TAC)")
    print("="*70)
    print(f"Input C Expression: {c_code}")
    print("-" * 50)
    for instruction in tac_instructions:
        print(instruction)
        
    return tac_instructions


# --- 4. Assembly Code Generation Function (Basic) ---

def generate_assembly(tac_instructions, file_path="input.txt"):
    """Generates simplified x86-like Assembly Code from the TAC instructions."""
    
    if not tac_instructions:
        print("\n" + "="*70)
        print("             PHASE 4: ASSEMBLY CODE GENERATION")
        print("="*70)
        print("Cannot generate Assembly: No TAC instructions provided.")
        return

    # Extract target variable from the last TAC instruction
    target_var_match = re.match(r'(\w+)\s*=\s*(\w+)', tac_instructions[-1])
    target_var = target_var_match.group(1) if target_var_match else "result"

    assembly_code = []
    variables = set()

    for tac in tac_instructions:
        match_op = re.match(r'(t\d+|\w+)\s*=\s*(\w+|\d+)\s*([+\-*/])\s*(\w+|\d+)', tac)
        match_assign = re.match(r'(\w+)\s*=\s*(\w+)', tac)
        
        # Collect variables for the data section
        for token in re.findall(r'\b[a-zA-Z_]\w*\b', tac):
            if not token.startswith('t') and token not in ['dd']: # 'dd' is part of assembly syntax
                 variables.add(token)

        if match_op:
            result_var, op1, operator, op2 = match_op.groups()
            
            # Use EBX for temporary calculations
            assembly_code.append(f"  MOV EAX, [{op1}]   ; Load {op1} into EAX")
            
            if operator == '+':
                assembly_code.append(f"  ADD EAX, [{op2}]   ; EAX = EAX + {op2}")
            elif operator == '-':
                assembly_code.append(f"  SUB EAX, [{op2}]   ; EAX = EAX - {op2}")
            elif operator == '*':
                # IMUL for multiplication, uses a different syntax when one operand is a register
                assembly_code.append(f"  MOV EBX, [{op2}]   ; Load {op2} into EBX")
                assembly_code.append(f"  IMUL EAX, EBX   ; EAX = EAX * EBX")
            elif operator == '/':
                # IDIV is more complex (uses EDX:EAX), simplified here
                assembly_code.append(f"  IDIV EAX, [{op2}]   ; EAX = EAX / {op2} (simplified)")

            # Store the temporary result
            assembly_code.append(f"  MOV [{result_var}], EAX ; Store result in {result_var}")
            
        elif match_assign and match_assign.group(1) == target_var:
            # Final assignment
            assembly_code.append(f"  MOV EAX, [{match_assign.group(2)}] ; Load final result from {match_assign.group(2)} into EAX")
            assembly_code.append(f"  MOV [{target_var}], EAX  ; Store final EAX value in {target_var}")

    print("\n" + "="*70)
    print("             PHASE 4: ASSEMBLY CODE GENERATION")
    print("="*70)
    print(f"Target Variable: {target_var}")
    print("-" * 50)

    # Print a simplified data section
    print("\nSECTION .data ; Variable Declarations (Simplified)")
    for var in sorted(list(variables)):
        print(f"  {var} dd 0") # dd = Define Double-word (4-byte integer)
    
    # Print the code section
    print("\nSECTION .text ; Program Code")
    for line in assembly_code:
        print(line)


# --- Setup and Main Execution ---

def setup_input_file(file_path="input.txt"):
    """Creates a sample input.txt file for the compiler phases."""
    sample_c_code = """
// Sample C code for compiler demonstration
int x = 10;
float y;
int main() {
    y = x * (5.0 + y) - 2; // Expression for TAC and Assembly
    return 0;
}
"""
    try:
        with open(file_path, 'w') as file:
            file.write(sample_c_code.strip())
        print(f"Created/updated '{file_path}' with sample C code.")
    except Exception as e:
        print(f"Error creating file: {e}")


def main():
    """Executes all compiler phases sequentially."""
    file_path = "input.txt"
    setup_input_file(file_path)

    # Phase 1: Lexical Analysis
    tokens = lexical_analysis(file_path)

    # Phase 2: Symbol Table Construction
    symbol_table = build_symbol_table(file_path)

    # Phase 3: Intermediate Code Generation (TAC)
    tac_instructions = generate_tac(file_path)

    # Phase 4: Code Generation (Assembly)
    generate_assembly(tac_instructions, file_path)
    
    # Clean up (optional)
    # os.remove(file_path) 

if __name__ == "__main__":
    main()