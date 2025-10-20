# assemblycodegenarate.py

import re

def generate_assembly(file_path="input.txt"):
    """
    Reads a simple arithmetic assignment statement from input.txt and 
    generates a basic sequence of x86-like Assembly Instructions.
    """
    try:
        with open(file_path, 'r') as file:
            c_code = file.read().strip()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return

    # Assuming the input is a single assignment statement: target = expression;
    match = re.search(r'(\w+)\s*=\s*(.*);', c_code)
    if not match:
        print("Error: Input is not a simple assignment statement (e.g., 'result = a + b;')")
        return

    target_var = match.group(1)
    expression = match.group(2).strip()

    # Simple tokenization for the expression
    # This assumes multiplication/division happens before addition/subtraction
    tokens = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*|\d+|[+\-*/]', expression)
    
    assembly_code = []
    
    # Assembly uses registers (EAX, EBX, etc.) for calculations. 
    # We will use EAX for intermediate results.
    
    # ----------------------------------------------------
    # Simplified Assembly Generation for 'a * 10 + b' type expression
    # ----------------------------------------------------
    
    # Step 1: Initial load or calculation (assuming 'a * 10' or 'a + b' type)
    if len(tokens) >= 3:
        operand1 = tokens[0]
        operator = tokens[1]
        operand2 = tokens[2]
        
        # Load the first operand into a register (EAX)
        assembly_code.append(f"  MOV EAX, [{operand1}]   ; Load {operand1} into EAX")
        
        # Perform the first operation
        if operator == '*':
            assembly_code.append(f"  IMUL EAX, {operand2}    ; EAX = EAX * {operand2} (Multiplication)")
        elif operator == '/':
             assembly_code.append(f"  IDIV EAX, {operand2}    ; EAX = EAX / {operand2} (Division)")
        elif operator == '+':
            assembly_code.append(f"  ADD EAX, [{operand2}]   ; EAX = EAX + {operand2} (Addition)")
        elif operator == '-':
            assembly_code.append(f"  SUB EAX, [{operand2}]   ; EAX = EAX - {operand2} (Subtraction)")
        
        # Handle the rest of the expression (very basic: assumes one more operation)
        if len(tokens) >= 5:
            next_operator = tokens[3]
            next_operand = tokens[4]
            
            if next_operator == '+':
                assembly_code.append(f"  ADD EAX, [{next_operand}] ; EAX = EAX + {next_operand}")
            elif next_operator == '-':
                assembly_code.append(f"  SUB EAX, [{next_operand}] ; EAX = EAX - {next_operand}")
                
        # Final assignment
        assembly_code.append(f"  MOV [{target_var}], EAX  ; Store final result in {target_var}")
    
    # ----------------------------------------------------

    print("\n--- Generated Assembly Code (x86-like) ---")
    print(f"Input C Expression: {c_code}")
    print("-" * 50)
    
    # Print a simplified data section for context
    assembly_code.insert(0, "\nSECTION .data")
    assembly_code.insert(1, f"  {target_var} dd 0")
    # Add assumed variables to data section for context
    for token in tokens:
         if re.match(r'^[a-zA-Z_]', token) and token != target_var:
             assembly_code.insert(2, f"  {token} dd 0 ; Assume initial value 0")

    for line in assembly_code:
        print(line)

if __name__ == "__main__":
    generate_assembly()