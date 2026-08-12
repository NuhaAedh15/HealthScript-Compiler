from scanner import healthscript_scanner

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.tree = []

    def current_token(self):
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return ("EOF", -1, "EOF")

    def add_tree(self, text):
        self.tree.append(text)

    def match(self, expected):
        token_type, line, value = self.current_token()
        if value == expected:
            self.add_tree(f"Matched: {value}")
            self.current += 1
        else:
            raise SyntaxError(
                f"Syntax Error at line {line}: Expected '{expected}' but found '{value}'"
            )

    def match_type(self, expected_type):
       token_type, line, value = self.current_token()
       if token_type == expected_type:
           self.add_tree(f"Matched: {token_type}({value})")
           self.current += 1
       else:
          raise SyntaxError(
               f"Syntax Error at line {line}: Expected {expected_type} but found '{value}'"
           )

    def Program(self):
        self.add_tree("<Program>")
        self.match("start")
        self.StmtList()
        self.match("finish")

    def StmtList(self):
        self.add_tree("  <StmtList>")
        while self.current_token()[2] in ["var", "print", "read", "if", "while", "do", "func"] or self.current_token()[0] == "IDENTIFIER":
            self.Stmt()

    def Stmt(self):
        value = self.current_token()[2]
        token_type = self.current_token()[0]

        self.add_tree("    <Stmt>")

        if value == "var":
            self.VarDecl()
        elif token_type == "IDENTIFIER":
            self.AssignStmt()
        elif value == "print":
            self.PrintStmt()
        elif value == "read":
            self.ReadStmt()
        elif value == "if":
            self.IfStmt()
        elif value == "while":
            self.WhileStmt()
        elif value == "do":
            self.FuncCall()
        elif value == "func":
            self.FuncDecl()
        else:
            line = self.current_token()[1]
            raise SyntaxError(f"Syntax Error at line {line}: Unexpected token '{value}'")

    def VarDecl(self):
        self.add_tree("      <VarDecl>")
        self.match("var")
        self.Type()
        self.match_type("IDENTIFIER")

        if self.current_token()[2] == "=":
            self.match("=")
            self.Expr()

        self.match(";")

    def Type(self):
        value = self.current_token()[2]
        line = self.current_token()[1]

        if value in ["int", "float", "string", "bool"]:
            self.add_tree(f"      <Type> {value}")
            self.current += 1
        else:
            raise SyntaxError(f"Syntax Error at line {line}: Expected data type")

    def ReturnType(self):
        value = self.current_token()[2]
        line = self.current_token()[1]

        if value in ["int", "float", "string", "bool", "void"]:
            self.add_tree(f"      <ReturnType> {value}")
            self.current += 1
        else:
            raise SyntaxError(f"Syntax Error at line {line}: Expected return type")

    def AssignStmt(self):
        self.add_tree("      <AssignStmt>")
        self.match_type("IDENTIFIER")
        self.match("=")
        self.Expr()
        self.match(";")

    def PrintStmt(self):
        self.add_tree("      <PrintStmt>")
        self.match("print")
        self.Expr()
        self.match(";")

    def ReadStmt(self):
        self.add_tree("      <ReadStmt>")
        self.match("read")
        self.match_type("IDENTIFIER")
        self.match(";")

    def IfStmt(self):
        self.add_tree("      <IfStmt>")
        self.match("if")
        self.BoolExpr()
        self.match("then")
        self.StmtList()

        if self.current_token()[2] == "else":
            self.match("else")
            self.StmtList()

        self.match("finish")

    def WhileStmt(self):
        self.add_tree("      <WhileStmt>")
        self.match("while")
        self.BoolExpr()
        self.match("do")
        self.StmtList()
        self.match("finish")

    def FuncDecl(self):
        self.add_tree("      <FuncDecl>")
        self.match("func")
        self.ReturnType()
        self.match_type("IDENTIFIER")
        self.match("(")

        if self.current_token()[2] != ")":
            self.ParamList()

        self.match(")")
        self.StmtList()
        self.match("finish")

    def ParamList(self):
        self.add_tree("      <ParamList>")
        self.Type()
        self.match_type("IDENTIFIER")

        while self.current_token()[2] == ",":
            self.match(",")
            self.Type()
            self.match_type("IDENTIFIER")

    def FuncCall(self):
        self.add_tree("      <FuncCall>")
        self.match("do")
        self.match_type("IDENTIFIER")
        self.match("(")

        if self.current_token()[2] != ")":
            self.ArgList()

        self.match(")")
        self.match(";")

    def ArgList(self):
        self.add_tree("      <ArgList>")
        self.Expr()

        while self.current_token()[2] == ",":
            self.match(",")
            self.Expr()

    def BoolExpr(self):
        self.add_tree("      <BoolExpr>")
        self.BoolTerm()

        while self.current_token()[2] == "or":
            self.match("or")
            self.BoolTerm()

    def BoolTerm(self):
        self.add_tree("      <BoolTerm>")
        self.BoolFactor()

        while self.current_token()[2] == "and":
            self.match("and")
            self.BoolFactor()

    def BoolFactor(self):
        self.add_tree("      <BoolFactor>")

        if self.current_token()[2] == "not":
            self.match("not")
            self.BoolFactor()
        else:
            self.Expr()

            if self.current_token()[2] in ["==", "!=", "<", ">", "<=", ">="]:
                self.current += 1
                self.add_tree("Matched: REL_OP")
                self.Expr()

    def Expr(self):
        self.add_tree("      <Expr>")
        self.Term()

        while self.current_token()[2] in ["+", "-"]:
            self.current += 1
            self.add_tree("Matched: ADD_OP")
            self.Term()

    def Term(self):
        self.add_tree("      <Term>")
        self.Power()

        while self.current_token()[2] in ["*", "/", "%"]:
            self.current += 1
            self.add_tree("Matched: MUL_OP")
            self.Power()

    def Power(self):
        self.add_tree("      <Power>")
        self.Unary()

        if self.current_token()[2] == "^":
            self.match("^")
            self.Power()

    def Unary(self):
        self.add_tree("      <Unary>")

        if self.current_token()[2] in ["+", "-", "not"]:
            op = self.current_token()[2]
            self.match(op)
            self.Unary()
        else:
            self.Factor()

    def Factor(self):
        token_type, line, value = self.current_token()
        self.add_tree("      <Factor>")

        if token_type in ["IDENTIFIER", "INTEGER", "FLOAT", "STRING"]:
            self.add_tree(f"Matched: {token_type}({value})")
            self.current += 1
        elif value in ["true", "false"]:
            self.add_tree(f"Matched: BOOL({value})")
            self.current += 1
        elif value == "(":
            self.match("(")
            self.Expr()
            self.match(")")
        else:
            raise SyntaxError(
                f"Syntax Error at line {line}: Unexpected token '{value}' in expression"
            )

    def display_parse_tree(self):
        print("\n--- Parse Tree Display ---")
        for item in self.tree:
            print(item)


with open("test.txt", "r") as file:
    source_code = file.read()

total, tokens, sym_table, lexical_errors = healthscript_scanner(source_code)

if lexical_errors:
    print("Lexical errors found:")
    for err in lexical_errors:
        print(err)
else:
    parser_tokens = [(t[0], t[1], t[2]) for t in tokens]
    parser = Parser(parser_tokens)

    try:
        parser.Program()
        print("Parsing successful.")
        parser.display_parse_tree()
    except SyntaxError as e:
        print(e)