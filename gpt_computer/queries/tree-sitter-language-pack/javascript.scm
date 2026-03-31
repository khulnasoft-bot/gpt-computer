; Tree-sitter query for JavaScript code structure
; Source: https://github.com/tree-sitter/tree-sitter-javascript

(function_declaration
  name: (identifier) @function.name
  parameters: (formal_parameters
    (identifier) @function.parameter)?
  body: (statement_block) @function.body) @function.definition

(function_expression
  name: (identifier)? @function.name
  parameters: (formal_parameters
    (identifier) @function.parameter)?
  body: (statement_block) @function.body) @function.expression

(arrow_function
  parameters: (formal_parameters
    (identifier) @function.parameter)?
  body: _ @function.body) @arrow_function.definition

(class_declaration
  name: (identifier) @class.name
  heritage: (class_heritage
    (identifier) @class.superclass)?
  body: (class_body) @class.body) @class.definition

(variable_declaration
  (variable_declarator
    name: (identifier) @variable.name
    value: _ @variable.value)) @variable.definition

(import_statement
  source: (string) @import.source) @import.definition

(import_statement
  import_clause: (named_imports
    (import_specifier
      name: (identifier) @import.name))) @import.named_definition

(export_statement
  declaration: (function_declaration
    name: (identifier) @export.function)) @export.function_definition

(call_expression
  function: (identifier) @call.function) @call.expression
