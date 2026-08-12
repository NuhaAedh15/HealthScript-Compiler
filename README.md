# HealthScript-Compiler
 A healthcare-focused programming language and compiler built in Python, featuring lexical analysis, LL(1) parsing, semantic analysis, and TAC generation.
## Overview
This project presents the design and implementation of a compiler front-end
for a custom programming language called HealthScript.
The compiler was developed in three phases: lexical analysis, syntax analysis,
and semantic analysis with intermediate code generation.
Python was used to implement the scanner, parser, semantic analyzer, and
Three-Address Code (TAC) generator.
The final system is capable of processing HealthScript programs, detecting
errors, and generating structured intermediate code through a complete
compiler front-end pipeline.
## Features
- Lexical Analysis
- LL(1) Syntax Analysis
- Recursive Descent Parsing
- Semantic Analysis
- Error Detection
- Symbol Table Management
- Three-Address Code (TAC) Generation
## Technologies
- Python
- Regular Expressions
- Context-Free Grammars
- LL(1) Parsing
## Project Structure
```text
HealthScript-Compiler/
├── src/
│   ├── scanner.py
│   ├── parser.py
│   └── semantic_codegen.py
├── examples/
│   └── test.txt
├── docs/
│   ├── COMPILERPROJECT.pdf
│   ├── Phase-1-Lexical-Analysis.pdf
│   ├── Phase-2-Syntax-Analysis.pdf
│   └── Phase-3-Semantic-Analysis.pdf
├── README.md
└── .gitignore
```
## Compiler Phases
### Phase 1 — Lexical Analysis
The scanner performs lexical analysis of HealthScript source code and converts the input into tokens used by the parser.
### Phase 2 — Syntax Analysis
The parser performs LL(1) recursive-descent parsing according to the HealthScript grammar and detects syntax errors.
### Phase 3 — Semantic Analysis and Intermediate Code Generation
The semantic analyzer performs type checking, manages the symbol table, detects semantic errors, and generates Three-Address Code (TAC).
## Example
An example HealthScript program is available in:
```text
examples/test.txt
```
## How to Run
Make sure Python is installed, then run the compiler source files from the project directory.
```bash
python src/scanner.py
python src/parser.py
python src/semantic_codegen.py
```
## Documentation
Detailed documentation for each compiler phase is available in the `docs` directory:
- Phase 1 — Lexical Analysis
- Phase 2 — Syntax Analysis
- Phase 3 — Semantic Analysis
- Complete Compiler Project Report
