; Tree-sitter query for TypeScript code structure
; Source: https://github.com/tree-sitter/tree-sitter-typescript

(function_declaration
  name: (identifier) @function.name
  parameters: (formal_parameters
    (identifier) @function.parameter)?
  return_type: (type_annotation)? @function.return_type
  body: (statement_block) @function.body) @function.definition

(function_signature
  name: (identifier) @function.name
  parameters: (formal_parameters
    (identifier) @function.parameter)?
  return_type: (type_annotation) @function.return_type) @function.signature

(arrow_function
  parameters: (formal_parameters
    (identifier) @function.parameter)?
  return_type: (type_annotation)? @function.return_type
  body: _ @function.body) @arrow_function.definition

(class_declaration
  name: (type_identifier) @class.name
  type_parameters: (type_parameters)? @class.type_parameters
  heritage: (class_heritage
    (type_identifier) @class.superclass)?
  body: (class_body) @class.body) @class.definition

(interface_declaration
  name: (type_identifier) @interface.name
  type_parameters: (type_parameters)? @interface.type_parameters
  body: (object_type) @interface.body) @interface.definition

(type_alias_declaration
  name: (type_identifier) @type_alias.name
  value: _ @type_alias.value) @type_alias.definition

(variable_declaration
  (variable_declarator
    name: (identifier) @variable.name
    type: (type_annotation)? @variable.type
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
