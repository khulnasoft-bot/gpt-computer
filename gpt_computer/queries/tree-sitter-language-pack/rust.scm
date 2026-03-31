; Tree-sitter query for Rust code structure
; Source: https://github.com/tree-sitter/tree-sitter-rust

(function_item
  name: (identifier) @function.name
  parameters: (parameters
    (parameter
      pattern: (identifier) @function.parameter))?
  return_type: (type)? @function.return_type
  body: (block) @function.body) @function.definition

(struct_item
  name: (type_identifier) @struct.name
  body: (field_declaration_list
    (field_declaration
      name: (field_identifier) @struct.field
      type: (type_identifier) @struct.type))?) @struct.definition

(enum_item
  name: (type_identifier) @enum.name
  body: (enum_variant_list
    (enum_variant
      name: (identifier) @enum.variant))?) @enum.definition

(impl_item
  type: (type_identifier) @impl.type
  trait: (type_identifier)? @impl.trait
  body: (declaration_list)) @impl.definition

(trait_item
  name: (type_identifier) @trait.name
  body: (declaration_list)) @trait.definition

(use_declaration
  argument: (use_as_clause
    path: (scoped_identifier) @use.path
    alias: (identifier) @use.alias)?) @use.definition

(mod_item
  name: (identifier) @module.name) @module.definition

(let_declaration
  pattern: (identifier) @variable.name
  type: (type)? @variable.type
  value: _? @variable.value) @variable.definition
