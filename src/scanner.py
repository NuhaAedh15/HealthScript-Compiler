import re

def healthscript_scanner(source_code):
    tokens_list = [] 
    symbol_table = {}
    error_list = []
    total_lexemes =  0
    
    # Keywords we agreed on in the Language Spec document
    keywords = {
        "start", "finish", "if", "then", "else", "repeat", "while", "var", 
        "int", "float", "string", "bool", "do", "read", "print", "void", 
        "return", "func", "and", "or", "not"
    }
    
    # Regular expressions for our tokens (Order is critical)
    token_specification = [
        ('BLOCK_COMMENT',       r'/\*(?:.|\n)*?\*/'),           # /* block comment */ 
        ('UNTERMINATED_BLOCK',  r'/\*(?:.|\n)*'),               # catch missing */
        ('LINE_COMMENT',        r'//[^\n]*'),                   # // single line comment
        ('STRING',              r'"[^"\n]*"'),                  # "text inside quotes"
        ('UNTERMINATED_STRING', r'"[^"\n]*'),                   # catch missing end quote
        ('MALFORMED_FLOAT',     r'[+-]?\d{9,}\.\d+'),           # Error: Float exceeding 8 digits
        ('MALFORMED_INTEGER',   r'[+-]?\d{9,}'),                # Error: Integer exceeding 8 digits
        ('FLOAT',               r'[+-]?\d{1,8}\.\d+'),          # numbers with decimals (max 8)
        ('INTEGER',             r'[+-]?\d{1,8}'),               # normal numbers (max 8)
        ('REL_OP',              r'==|!=|<=|>=|<|>'),            # relational operators
        ('ARITH_OP',            r'[\+\-\*/%\^=]'),              # math and assignment (=)
        ('DELIMITER',           r'[.\(\),\{\};:]'),             # brackets and punctuation
        ('IDENTIFIER',          r'[a-zA-Z][a-zA-Z0-9]*'),       # variable/function names
        ('NEWLINE',             r'\n'),                         # count line numbers
        ('WHITESPACE',          r'[ \t]+'),                     # spaces and tabs
        ('UNKNOWN',             r'.'),                          # anything else is an error
    ]
    
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    get_token = re.compile(tok_regex)
    
    line_num = 1
    
    for match in get_token.finditer(source_code):
        kind = match.lastgroup
        value = match.group()
        
        if kind == 'NEWLINE':
            line_num += 1
            continue
        elif kind in ['WHITESPACE', 'LINE_COMMENT']:
            continue
        elif kind == 'BLOCK_COMMENT':
            line_num += value.count('\n')
            continue
        
        # Handle the deliberate lexical errors
        if kind == 'UNTERMINATED_BLOCK':
            error_list.append(f"Lexical Error at line {line_num}: Unterminated block comment")
            line_num += value.count('\n')
            continue
        elif kind == 'UNTERMINATED_STRING':
            error_list.append(f"Lexical Error at line {line_num}: Unterminated string literal [{value}]")
            continue
        elif kind == 'MALFORMED_FLOAT':
            error_list.append(f"Lexical Error at line {line_num}: Malformed float number '{value}'")
            continue
        elif kind == 'MALFORMED_INTEGER':
            error_list.append(f"Lexical Error at line {line_num}: Malformed integer number '{value}'")
            continue
        elif kind == 'UNKNOWN':
            error_list.append(f"Lexical Error at line {line_num}: Invalid symbol '{value}'")
            continue
            
        # Handle Identifiers and Keywords
        if kind == 'IDENTIFIER':
            lower_value = value.lower() 
            if lower_value in keywords:
                tokens_list.append(("KEYWORD", line_num, lower_value))
                total_lexemes += 1
            elif len(value) > 8:
                error_list.append(f"Lexical Error at line {line_num}: Identifier '{value}' exceeds max length (8 chars)")
            else:
                tokens_list.append(("IDENTIFIER", line_num, value))
                total_lexemes += 1
                if value not in symbol_table:
                    symbol_table[value] = line_num
        else:
            tokens_list.append((kind, line_num, value))
            total_lexemes += 1
            
    return total_lexemes, tokens_list, symbol_table, error_list


# Testing the Scanner
if __name__ == '__main__':
    # Sample code with perfectly formatted syntax and deliberate lexical errors
    test_code = """
 start
 var float temp = 36.5;
 if temp > 37 then
 print "Fever"; 
 finish
 finish
    """
    with open("test.txt","r") as file:
      test_code=file.read()
    
    total, tokens, sym_table, errors = healthscript_scanner(test_code)
    
    print("=== Phase 1 Scanner Results ===")
    print(f"Total Lexemes Found: {total}")
    print()
    
    print("Tokens (<Type, Line, Value>)")
    for t in tokens:
        print(f"<{t[0]}, {t[1]}, {t[2]}>")
        
    print()
    print("Symbol Table")
    for identifier, line in sym_table.items():
        print(f"{identifier} (first seen at line {line})")
        
    print()
    print("Errors")
    if not errors:
        print("No errors! Ready for Phase 2.")
    else:
        for err in errors:
            print(err)