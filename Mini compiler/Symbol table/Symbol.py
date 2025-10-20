# symboltable_beginner.py

def build_symbol_table(file_path="input.txt"):
    
    try:
        with open(file_path, 'r') as file:
            c_code = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return

    # Define the keywords we are looking for (Data Types)
    DATA_TYPES = ['int', 'float', 'double', 'char', 'void']
    
    symbol_table = {}
    index = 1
    
    # Split the code into simple tokens (words, numbers, symbols)
    # This is a basic way to tokenize without complex regex
    all_tokens = c_code.replace('(', ' ( ').replace(')', ' ) ') \
                       .replace('{', ' { ').replace('}', ' } ') \
                       .replace(';', ' ; ').replace('=', ' = ') \
                       .split()
                       
    
    i = 0
    while i < len(all_tokens):
        token = all_tokens[i]

        # Check if the current token is a Data Type
        if token in DATA_TYPES:
            data_type = token
            
            # Check the next token, which should be the identifier
            if i + 1 < len(all_tokens):
                identifier = all_tokens[i + 1]
                
                # Filter out tokens that are likely not identifiers (like operators or separators)
                if identifier not in ['=', ';', '(', ')', '{', '}'] and identifier not in symbol_table:
                    
                    # Very simple scope check: if the next token is '(', it's likely a function
                    scope = "Variable"
                    if i + 2 < len(all_tokens) and all_tokens[i+2] == '(':
                        scope = "Function"
                    
                    # Add to the Symbol Table
                    symbol_table[identifier] = {
                        "Index": index,
                        "Type": data_type,
                        "Scope": scope,
                        "Initial Value": "N/A"
                    }
                    index += 1
            
        i += 1

    print("\n--- Symbol Table Output from input.txt (Beginner Version) ---")
    if not symbol_table:
        print("No declarations (int, float, double, char, void) found.")
        return

    # Print the table header
    print("{:<10} {:<20} {:<10} {:<15} {:<15}".format(
        "Index", "Identifier", "Type", "Scope", "Initial Value"
    ))
    print("-" * 70)

    # Print the table rows
    for name, data in symbol_table.items():
        print("{:<10} {:<20} {:<10} {:<15} {:<15}".format(
            data["Index"], name, data["Type"], data["Scope"], data["Initial Value"]
        ))

if __name__ == "__main__":
    build_symbol_table()