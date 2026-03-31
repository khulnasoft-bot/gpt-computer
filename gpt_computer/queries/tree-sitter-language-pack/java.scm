; Tree-sitter query for Java code structure
; Source: https://github.com/tree-sitter/tree-sitter-java

(method_declaration
  name: (identifier) @method.name
  parameters: (formal_parameters
    (formal_parameter
      (identifier) @method.parameter))?
  return_type: (type_identifier)? @method.return_type
  body: (block) @method.body) @method.definition

(class_declaration
  name: (identifier) @class.name
  superclass: (superclass
    (type_identifier) @class.superclass)?
  interfaces: (super_interfaces)? @class.interfaces
  body: (class_body) @class.body) @class.definition

(interface_declaration
  name: (identifier) @interface.name
  body: (interface_body) @interface.body) @interface.definition

(field_declaration
  (variable_declarator
    name: (identifier) @field.name)
  type: (type_identifier) @field.type) @field.definition

(import_declaration
  name: (scoped_identifier) @import.name) @import.definition

(package_declaration
  (scoped_identifier) @package.name) @package.definition

(constructor_declaration
  name: (identifier) @constructor.name
  parameters: (formal_parameters
    (formal_parameter
      (identifier) @constructor.parameter))?
  body: (block) @constructor.body) @constructor.definition
