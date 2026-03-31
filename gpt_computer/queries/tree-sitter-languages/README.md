# Credits

GPT-Computer uses modified versions of the tags.scm files from these open source
tree-sitter language implementations:

## Core Tree-sitter Libraries
- **tree-sitter** - https://github.com/tree-sitter/tree-sitter
- **tree-sitter-python** - https://github.com/tree-sitter/tree-sitter-python
- **tree-sitter-javascript** - https://github.com/tree-sitter/tree-sitter-javascript
- **tree-sitter-typescript** - https://github.com/tree-sitter/tree-sitter-typescript
- **tree-sitter-html** - https://github.com/tree-sitter/tree-sitter-html
- **tree-sitter-css** - https://github.com/tree-sitter/tree-sitter-css
- **tree-sitter-java** - https://github.com/tree-sitter/tree-sitter-java
- **tree-sitter-cpp** - https://github.com/tree-sitter/tree-sitter-cpp
- **tree-sitter-c** - https://github.com/tree-sitter/tree-sitter-c
- **tree-sitter-go** - https://github.com/tree-sitter/tree-sitter-go
- **tree-sitter-rust** - https://github.com/tree-sitter/tree-sitter-rust
- **tree-sitter-ruby** - https://github.com/tree-sitter/tree-sitter-ruby
- **tree-sitter-php** - https://github.com/tree-sitter/tree-sitter-php
- **tree-sitter-kotlin** - https://github.com/tree-sitter/tree-sitter-kotlin
- **tree-sitter-markdown** - https://github.com/tree-sitter/tree-sitter-markdown

## Usage

The `tags.scm` file contains tree-sitter queries for extracting code structure elements like:
- Function definitions and signatures
- Class and interface declarations
- Variable assignments and declarations
- Import statements
- Method calls
- Decorators and annotations

These queries are used by GPT-Computer to parse and understand code structure across multiple programming languages.

## License

All tree-sitter language grammars are licensed under their respective open source licenses, typically the MIT License or Apache License 2.0. Please refer to individual repositories for specific licensing information.
