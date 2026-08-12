from scanner import healthscript_scanner

class SemanticCodeGenerator:
    def __init__(self):
        self.symbol_table = {}
        self.semantic_errors = []
        self.tac = []
        self.temp_count = 1

    def new_temp(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

    def add_symbol(self, name, var_type, line):
        if name in self.symbol_table:
            self.semantic_errors.append(
                f"Semantic Error at line {line}: Duplicate declaration of variable '{name}'"
            )
        else:
            self.symbol_table[name] = {
                "type": var_type,
                "scope": "global",
                "line": line
            }

    def get_type(self, value):
        if value.startswith('"') and value.endswith('"'):
            return "string"
        if value in ["true", "false"]:
            return "bool"
        try:
            int(value)
            return "int"
        except ValueError:
            pass
        try:
            float(value)
            return "float"
        except ValueError:
            pass
        if value in self.symbol_table:
            return self.symbol_table[value]["type"]
        return "unknown"

    def check_declared(self, name, line):
        if name not in self.symbol_table:
            self.semantic_errors.append(
                f"Semantic Error at line {line}: Variable '{name}' used but not declared"
            )
            return False
        return True

    def compatible(self, left_type, right_type):
        if left_type == right_type:
            return True
        if left_type == "float" and right_type == "int":
            return True
        return False

    def analyze_expression(self, expr, line):
        parts = expr.replace(";", "").split()

        if len(parts) == 1:
            value = parts[0]
            if value.isidentifier() and value not in ["true", "false"]:
                self.check_declared(value, line)
            return self.get_type(value), value

        if len(parts) == 3:
            left, op, right = parts

            if left.isidentifier() and left not in ["true", "false"]:
                self.check_declared(left, line)
            if right.isidentifier() and right not in ["true", "false"]:
                self.check_declared(right, line)

            left_type = self.get_type(left)
            right_type = self.get_type(right)

            if op == "/" and right == "0":
                self.semantic_errors.append(
                    f"Semantic Error at line {line}: Division by zero"
                )

            if op in ["+", "-", "*", "/", "%", "^"]:
                if left_type not in ["int", "float"] or right_type not in ["int", "float"]:
                    self.semantic_errors.append(
                        f"Type Error at line {line}: Arithmetic operation requires numeric values"
                    )
                result_type = "float" if "float" in [left_type, right_type] else "int"

            elif op in ["==", "!=", "<", ">", "<=", ">="]:
                result_type = "bool"

            else:
                result_type = "unknown"

            temp = self.new_temp()
            self.tac.append(f"{temp} = {left} {op} {right}")
            return result_type, temp

        return "unknown", expr

    def process_line(self, line, line_num):
        line = line.strip()

        if not line or line in ["start", "finish"]:
            return

        if line.startswith("var "):
            parts = line.replace(";", "").split()

            if len(parts) >= 3:
                var_type = parts[1]
                name = parts[2]
                self.add_symbol(name, var_type, line_num)

                if "=" in parts:
                    eq_index = parts.index("=")
                    expr = " ".join(parts[eq_index + 1:])
                    expr_type, expr_value = self.analyze_expression(expr, line_num)

                    if not self.compatible(var_type, expr_type):
                        self.semantic_errors.append(
                            f"Type Error at line {line_num}: Cannot assign '{expr_type}' to variable of type '{var_type}'"
                        )
                    self.tac.append(f"{name} = {expr_value}")

            return

        if line.startswith("print "):
            expr = line.replace("print", "", 1).replace(";", "").strip()
            expr_type, expr_value = self.analyze_expression(expr, line_num)
            self.tac.append(f"print {expr_value}")
            return

        if "=" in line and not line.startswith("if"):
            left, right = line.split("=", 1)
            name = left.strip()
            expr = right.replace(";", "").strip()

            if self.check_declared(name, line_num):
                left_type = self.symbol_table[name]["type"]
                expr_type, expr_value = self.analyze_expression(expr, line_num)

                if not self.compatible(left_type, expr_type):
                    self.semantic_errors.append(
                        f"Type Error at line {line_num}: Cannot assign '{expr_type}' to variable of type '{left_type}'"
                    )

                self.tac.append(f"{name} = {expr_value}")

            return

        if line.startswith("if "):
            condition = line.replace("if", "", 1).replace("then", "").strip()
            cond_type, cond_value = self.analyze_expression(condition, line_num)
            self.tac.append(f"if {cond_value} goto L_true")
            return

        if line.startswith("while "):
            condition = line.replace("while", "", 1).replace("do", "").strip()
            cond_type, cond_value = self.analyze_expression(condition, line_num)
            self.tac.append(f"while {cond_value} goto L_loop")
            return

    def analyze(self, source_code):
        lines = source_code.splitlines()

        for i, line in enumerate(lines, start=1):
            self.process_line(line, i)

        return self.symbol_table, self.semantic_errors, self.tac


# Main execution
with open("test.txt", "r") as file:
    source_code = file.read()

total, tokens, sym_table, lexical_errors = healthscript_scanner(source_code)

print("=== Phase 3: Semantic Analysis and Code Generation ===")
print()

if lexical_errors:
    print("Lexical errors found:")
    for err in lexical_errors:
        print(err)

else:
    analyzer = SemanticCodeGenerator()
    symbol_table, semantic_errors, tac = analyzer.analyze(source_code)

    print("--- Enhanced Symbol Table ---")
    for name, info in symbol_table.items():
        print(
            f"{name} | Type: {info['type']} | Scope: {info['scope']} | Declared at line: {info['line']}"
        )

    print()
    print("--- Semantic Errors ---")
    if semantic_errors:
        for err in semantic_errors:
            print(err)
    else:
        print("No semantic errors found.")

    print()
    print("--- Generated Three-Address Code (TAC) ---")
    for instruction in tac:
        print(instruction)

    print()
    if not semantic_errors:
        print("End-to-end compilation completed successfully.")
    else:
        print("Compilation stopped due to semantic errors.")