query_lang = {

    "python" : {
        "parameters" : "parameters: (parameters)",
        "bool_operator" : "condition: (boolean_operator) right: (boolean_operator)",
        "comment" : "(comment)",
        "function" : "(function_definition)",
        "function_block" : "(function_definition body: (block) @function.block)",
        "return" : "(return_statement)",
   },

   "c_sharp" : {
        "parameters" : "parameters: (parameter_list)",
        "bool_operator" : "condition: (binary_expression) (binary_expression)",
        "comment" : "(comment)",
        "function" : "(method_declaration) (constructor_declaration)",
        "function_block" : "(method_declaration body: (block) @function.block) (constructor_declaration body: (block) @function.block)",
        "return" : "(return_statement)"
   },

   "java" : {
        "parameters" : "parameters: (formal_parameters)",
        "bool_operator" : "(binary_expression)",
        "comment" : "(line_comment) (block_comment)",
        "function" : "(method_declaration) (constructor_declaration)",
        "function_block" : "(method_declaration body: (block) @function.block) (constructor_declaration body: (constructor_body) @function.block)",
        "return" : "(return_statement)"
   }

}