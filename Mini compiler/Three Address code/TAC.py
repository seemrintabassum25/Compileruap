# ThreeAddressCode.py (Improved to handle precedence and parentheses)

import re

def generate_tac(file_path="input.txt"):
    """
    Reads the arithmetic expression from input.txt and generates
    Three-Address Code (TAC) using Shunting-Yard for correct precedence.
    """
    try:
        with open(file_path, 'r') as file:
            c_code = file.read().strip()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return

    # 1. Extract Target Variable and Expression
    match = re.search(r'(\w+)\s*=\s*(.*);', c_code)
    if not match:
        print("Error: Input must be a simple assignment statement (e.g., 'result = a + b;')")
        return

    target_var = match.group(1)
    expression = match.group(2).strip()

    # Define operators and their precedence
    operators = {'*': 3, '/': 3, '+': 2, '-': 2, '(': 1}
    
    # Split expression into tokens (handles identifiers, numbers, and operators/parentheses)
    tokens = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*|\d+\.\d+|\d+|[+\-*/()]', expression)

    # 2. Shunting-Yard Algorithm: Convert to Reverse Polish Notation (RPN)
    op_stack = []
    output_queue = []

    for token in tokens:
        if token not in operators and token not in [')']: # Operand (Identifier or Literal)
            output_queue.append(token)
        elif token == '(':
            op_stack.append(token)
        elif token == ')':
            while op_stack and op_stack[-1] != '(':
                output_queue.append(op_stack.pop())
            if op_stack and op_stack[-1] == '(':
                op_stack.pop() # Discard '('
            # else: Error: Mismatched parenthesis (ignored for simplicity)
        elif token in operators: # Operator
            while (op_stack and op_stack[-1] != '(' and 
                   operators.get(op_stack[-1], 0) >= operators[token]):
                output_queue.append(op_stack.pop())
            op_stack.append(token)

    # Pop any remaining operators from the stack to the queue
    while op_stack:
        output_queue.append(op_stack.pop()) 

    # 3. Generate TAC from RPN
    tac_instructions = []
    temp_count = 1
    operand_stack = []

    for token in output_queue:
        if token not in operators:
            operand_stack.append(token) # Operand (or already generated temp var)
        elif token in operators: # Operator
            op2 = operand_stack.pop()
            op1 = operand_stack.pop()
            
            temp_var = f"t{temp_count}"
            tac_instructions.append(f"{temp_var} = {op1} {token} {op2}")
            operand_stack.append(temp_var)
            temp_count += 1
            
    # Final assignment
    if operand_stack:
        final_temp = operand_stack.pop()
        tac_instructions.append(f"{target_var} = {final_temp}")


    print("\n--- Generated Three-Address Code (TAC) ---")
    print(f"Input C Expression: {c_code}")
    print("-" * 50)
    for instruction in tac_instructions:
        print(instruction)

if __name__ == "__main__":
    generate_tac()