# Tree-sitter Language Pack

These scm files are all adapted from the github repositories listed here:

## Language-Specific Query Files

This directory contains tree-sitter query files (`.scm`) for individual programming languages. Each file defines patterns for extracting structural elements from source code.

### Available Languages

- **python.scm** - Python language queries
- **javascript.scm** - JavaScript language queries
- **typescript.scm** - TypeScript language queries
- **java.scm** - Java language queries
- **go.scm** - Go language queries
- **rust.scm** - Rust language queries

### Source Repositories

All query files are adapted from the official tree-sitter language repositories:

- **Python**: https://github.com/tree-sitter/tree-sitter-python
- **JavaScript**: https://github.com/tree-sitter/tree-sitter-javascript
- **TypeScript**: https://github.com/tree-sitter/tree-sitter-typescript
- **Java**: https://github.com/tree-sitter/tree-sitter-java
- **Go**: https://github.com/tree-sitter/tree-sitter-go
- **Rust**: https://github.com/tree-sitter/tree-sitter-rust

### Query Patterns

Each `.scm` file contains tree-sitter queries that match:

- **Functions**: Function definitions, signatures, and expressions
- **Classes/Structs**: Class, struct, and interface declarations
- **Variables**: Variable declarations and assignments
- **Imports**: Import and export statements
- **Methods**: Method definitions and calls
- **Types**: Type definitions and annotations

### Usage

These query files are used by GPT-Computer's code parsing system to:

1. Parse source code files
2. Extract structural information
3. Build code representations for analysis
4. Enable intelligent code understanding

### License

All query files are derived from the original tree-sitter language grammars and maintain the same open source licenses as their source repositories.
