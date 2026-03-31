; Tree-sitter query for extracting code structure from Python files
; Adapted from tree-sitter-python repository

(function_definition
  name: (identifier) @function.name
  parameters: (parameters
    (identifier) @function.parameter)?
  return_type: (type)? @function.return_type) @function.definition

(class_definition
  name: (identifier) @class.name
  superclasses: (argument_list
    (identifier) @class.superclass)?) @class.definition

(import_statement
  name: (dotted_name) @import.name) @import.definition

(import_from_statement
  module_name: (dotted_name) @import.module
  name: (dotted_name) @import.name) @import.from_definition

(assignment
  left: (identifier) @variable.name
  right: _ @variable.value) @variable.definition

; Function calls
(call
  function: (identifier) @call.function) @call.expression

; Decorators
(decorator
  (identifier) @decorator.name) @decorator.definition

; Docstrings
(expression_statement
  (string
    (string_content) @docstring.content)) @docstring.definition
