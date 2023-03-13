query_lang = {
    "python": {
        "parameters": "parameters: (parameters)",
        "bool_operator": "condition: (boolean_operator) right: (boolean_operator)",
        "comment": "(comment)",
        "function": "(function_definition)",
        "function_block": "(function_definition body: (block) @function.block)",
        "return": "(return_statement)",
        "nested_controlflow1": """
                                (module [
                                (if_statement 
                                    consequence: (block) @cons
                                        )
                                (if_statement 
                                    consequence: (block) @cons
                                    alternative: (_ [body: (block) consequence: (block) ] @cons) 
                                        )
                                (while_statement body: (block) @cons)
                                (for_statement body: (block) @cons)]
                                )

                                (function_definition
                                body: (block [
                                    (if_statement 
                                        consequence: (block) @cons
                                            )
                                    (if_statement 
                                        consequence: (block) @cons
                                        alternative: (_ [body: (block) consequence: (block)] @cons)
                                            )
                                    (while_statement body: (block) @cons)
                                    (for_statement body: (block) @cons)])
                                )
                                """,
        "nested_controlflow2": """
                                (_ [
                                (if_statement 
                                    consequence: (block) @cons
                                        )
                                (if_statement 
                                    consequence: (block) @cons
                                    alternative: (_ [body: (block) consequence: (block) ] @cons) 
                                        )
                                (while_statement body: (block) @cons)
                                (for_statement body: (block) @cons)]
                                )
                                """,
    },
    "c_sharp": {
        "parameters": "parameters: (parameter_list)",
        "bool_operator": "condition: (binary_expression) (binary_expression)",
        "comment": "(comment)",
        "function": "(method_declaration) (constructor_declaration)",
        "function_block": "(method_declaration body: (block) @function.block) (constructor_declaration body: (block) @function.block)",
        "return": "(return_statement)",
        "nested_controlflow1": """
                                (method_declaration
                                    body: (block [
                                    (if_statement
                                        consequence: (block) @cons)
                                    (if_statement
                                        consequence: (block) @cons
                                        alternative: (_ [alternative: (block) consequence: (block) ] @cons))
                                    (for_statement
                                        body: (block) @cons)
                                    (for_each_statement
                                        body: (block) @cons)
                                    (while_statement
                                        (block) @cons)]))

                                (global_statement [
                                    (if_statement
                                        consequence: (block) @cons)
                                    (if_statement
                                        consequence: (block) @cons
                                        alternative: (_ [alternative: (block) consequence: (block) ] @cons))
                                    (for_statement
                                        body: (block) @cons)
                                    (for_each_statement
                                        body: (block) @cons)
                                    (while_statement
                                        (block) @cons)])
                                """,
        "nested_controlflow2": """
                                (_
                                    body: (block [
                                    (if_statement
                                        consequence: (block) @cons)
                                    (if_statement
                                        consequence: (block) @cons
                                        alternative: (_ [alternative: (block) consequence: (block) ] @if))
                                    (for_statement
                                        body: (block) @cons)
                                        (for_each_statement
                                                body: (block) @cons)
                                    (while_statement
                                        (block) @cons)]))
                                """,
    },
    "java": {
        "parameters": "parameters: (formal_parameters)",
        "bool_operator": "(binary_expression)",
        "comment": "(line_comment) (block_comment)",
        "function": "(method_declaration) (constructor_declaration)",
        "function_block": "(method_declaration body: (block) @function.block) (constructor_declaration body: (constructor_body) @function.block)",
        "return": "(return_statement)",
        "nested_controlflow1": """
                                (method_declaration
                                    body: (block [
                                    (if_statement
                                        consequence: (block) @cons)
                                    (if_statement
                                        consequence: (block) @cons
                                        alternative: (_ [alternative: (block) consequence: (block) ] @if))
                                    (for_statement
                                        body: (block) @cons)
                                    (while_statement
                                        (block) @cons)]))
                                """,
        "nested_controlflow2": """
                                (_
                                    body: (block [
                                    (if_statement
                                        consequence: (block) @cons)
                                    (if_statement
                                        consequence: (block) @cons
                                        alternative: (_ [alternative: (block) consequence: (block) ] @if))
                                    (for_statement
                                        body: (block) @cons)
                                    (while_statement
                                        (block) @cons)]))
                                """,
    },
}
