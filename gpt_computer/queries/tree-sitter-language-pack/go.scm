; Tree-sitter query for Go code structure
; Source: https://github.com/tree-sitter/tree-sitter-go

(function_declaration
  name: (identifier) @function.name
  parameters: (parameter_list
    (parameter_declaration
      name: (identifier) @function.parameter))?
  result: (parameter_list)? @function.result
  body: (block) @function.body) @function.definition

(method_declaration
  name: (field_identifier) @method.name
  receiver: (parameter_declaration
    name: (identifier) @method.receiver)?
  parameters: (parameter_list
    (parameter_declaration
      name: (identifier) @method.parameter))?
  result: (parameter_list)? @method.result
  body: (block) @method.body) @method.definition

(type_declaration
  (type_spec
    name: (type_identifier) @type.name
    type: (struct_type
      (field_declaration
        name: (field_identifier) @struct.field
        type: (type_identifier) @struct.type))? @type.definition)) @type.definition

(type_declaration
  (type_spec
    name: (type_identifier) @interface.name
    type: (interface_type
      (method_spec
        name: (field_identifier) @interface.method))? @interface.definition)) @interface_definition

(var_declaration
  (var_spec
    name: (identifier) @variable.name
    type: (type_identifier)? @variable.type
    value: _? @variable.value)) @variable.definition

(import_declaration
  path: (import_spec_list
    (import_spec
      path: (string) @import.path))) @import.definition

(package_clause
  (package_identifier) @package.name) @package.definition
