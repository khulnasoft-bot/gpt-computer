; Tree-sitter query for Python code structure
; Source: https://github.com/tree-sitter/tree-sitter-python

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

(call
  function: (identifier) @call.function) @call.expression

(decorator
  (identifier) @decorator.name) @decorator.definition

(expression_statement
  (string
    (string_content) @docstring.content)) @docstring.definition
