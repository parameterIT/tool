from typing import List

"""
file containing utilities for for metric implementations

contains dictionary of query translations used by underlying metrics,
a list of supported languages, and a list of supported file encodings.
"""

SUPPORTED_ENCODINGS: List[str] = [
    "UTF-8",
    # UTF-8-SIG files have a BOM, using UTF-8-SIG will correctly read the BOM as meta-data
    "UTF-8-SIG",
]

SUPPORTED_LANGUAGES: List[str] = [
    "python",
    "c_sharp",
    "java",
]

translate_to = {
    "python": {
        "parameters": "parameters: (parameters)",
        "bool_operator": "condition: (boolean_operator) right: (boolean_operator)",
        "bool_operator_child": "boolean_operator",
        "comment": "(comment)",
        "goto": "",
        "global_statement": "(module)",
        "function": "(function_definition)",
        "invocation": "(call)",
        "if_statement": "(if_statement)",
        "for_statement": "(for_statement)",
        "while_statement": "(while_statement)",
        "catch_statement": "(except_clause)",
        "break_statement": "(break_statement)",
        "continue_statement": "(continue_statement)",
        "function_block": "(function_definition body: (block) @function.block)",
        "return": "(return_statement)",
        "nested_function_call": "(function_definition body: (block (expression_statement (call) @nested_call)))",
        "global_control_flow": """
                                (module [
                                (if_statement 
                                    consequence: (block) @cons
                                        )
                                (if_statement 
                                    consequence: (block) @cons
                                    alternative: (_ [body: (block) consequence: (block) ] @cons) 
                                        )
                                (while_statement body: (block) @cons)
                                (for_statement body: (block) @cons)
                                (try_statement body: (block) @cons)
                                (try_statement (except_clause (block) @cons))]
                                )
        """,
        "method_control_flow": """
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
                                    (for_statement body: (block) @cons)
                                    (try_statement body: (block) @cons)
                                    (try_statement (except_clause (block) @cons))]))
        """,
        "constructor_control_flow": """""",
        "nested_controlflow_subsequent_nodes": """
                                (_ [
                                (if_statement 
                                    consequence: (block) @cons
                                        )
                                (if_statement 
                                    consequence: (block) @cons
                                    alternative: (_ [body: (block) consequence: (block) ] @cons) 
                                        )
                                (while_statement body: (block) @cons)
                                (for_statement body: (block) @cons)
                                (try_statement body: (block) @cons)
                                (try_statement (except_clause (block) @cons))]
                                )
                                """,
    },
    "c_sharp": {
        "parameters": "parameters: (parameter_list)",
        "bool_operator": "condition: (binary_expression) (binary_expression)",
        "bool_operator_child": "binary_expression",
        "comment": "(comment)",
        "goto": "(goto_statement)",
        "global_statement": "(global_statement)",
        "function": "(method_declaration)",
        "constructor": "(constructor_declaration)",
        "invocation": "(invocation_expression)",
        "if_statement": "(if_statement)",
        "for_statement": "[(for_statement) (for_each_statement)]",
        "while_statement": "(while_statement)",
        "catch_statement": "(catch_clause)",
        "break_statement": "(break_statement)",
        "continue_statement": "(continue_statement)",
        "function_block": "(method_declaration body: (block) @function.block) (constructor_declaration body: (block) @function.block)",
        "return": "(return_statement)",
        "nested_function_call": "(_ body: (block (expression_statement (invocation_expression) @func)))",
        "global_control_flow": """
                                (global_statement [
                                    (if_statement
                                        consequence: (block) @cons)
                                    (if_statement
                                        consequence: (_) @cons
                                        alternative: [
                                            (_ [alternative: (_) consequence: (_) ] @cons)
                                            (block) @cons])
                                    (for_statement
                                        body: (block) @cons)
                                    (for_each_statement
                                        body: (block) @cons)
                                    (while_statement
                                        (block) @cons)
                                    (switch_statement
                                        body: (switch_body (switch_section) @cons))
                                    (try_statement body: (block) @cons)
                                    (try_statement (catch_clause body: (block) @cons))])
        """,
        "method_control_flow": """
                                (method_declaration
                                    body: (block [
                                    (if_statement
                                        consequence: (block) @cons)
                                    (if_statement
                                        consequence: (_) @cons
                                        alternative: [
                                            (_ [alternative: (_) consequence: (_) ] @cons)
                                            (block) @cons])
                                    (for_statement
                                        body: (block) @cons)
                                    (for_each_statement
                                        body: (block) @cons)
                                    (while_statement
                                        (block) @cons)
                                    (switch_statement
                                        body: (switch_body (switch_section) @cons))
                                    (try_statement body: (block) @cons)
                                    (try_statement (catch_clause body: (block) @cons))]))
        """,
        "constructor_control_flow": """
                                (constructor_declaration
                                    body: (block [
                                    (if_statement
                                        consequence: (block) @cons)
                                    (if_statement
                                        consequence: (_) @cons
                                        alternative: [
                                            (_ [alternative: (_) consequence: (_) ] @cons)
                                            (block) @cons])
                                    (for_statement
                                        body: (block) @cons)
                                    (for_each_statement
                                        body: (block) @cons)
                                    (while_statement
                                        (block) @cons)
                                    (switch_statement
                                        body: (switch_body (switch_section) @cons))
                                    (try_statement body: (block) @cons)
                                    (try_statement (catch_clause body: (block) @cons))]))
        """,
        "nested_controlflow_subsequent_nodes": """
                                (_ [
                                    (if_statement
                                        consequence: (_) @cons)
                                    (if_statement
                                        consequence: (_) @cons
                                        alternative: [
                                            (_ [alternative: (_) consequence: (_) ] @cons)
                                            (block) @cons])
                                    (for_statement
                                        body: (block) @cons)
                                    (for_each_statement
                                        body: (block) @cons)
                                    (while_statement
                                        (block) @cons)
                                    (switch_statement
                                        body: (switch_body (switch_section) @cons))
                                    (try_statement body: (block) @cons)
                                    (try_statement (catch_clause body: (block) @cons))])
                                """,
    },
    "java": {
        "parameters": "parameters: (formal_parameters)",
        "bool_operator": "(binary_expression)",
        "bool_operator_child": "binary_expression",
        "comment": "(line_comment) (block_comment)",
        "goto": "",
        "function": "(method_declaration)",
        "constructor": "(constructor_declaration)",
        "invocation": "(method_invocation)",
        "if_statement": "(if_statement)",
        "for_statement": "(for_statement)",
        "while_statement": "(while_statement)",
        "catch_statement": "(catch_clause)",
        "break_statement": "(break_statement)",
        "continue_statement": "(continue_statement)",
        "function_block": "(method_declaration body: (block) @function.block) (constructor_declaration body: (constructor_body) @function.block)",
        "return": "(return_statement)",
        "nested_function_call": "(_ body: (_ (expression_statement (method_invocation) @func)))",
        "global_control_flow": """""",
        "method_control_flow": """
                                (method_declaration
                                    body: (block [
                                    (if_statement
                                        consequence: (_) @cons)
                                    (if_statement
                                        consequence: (_) @cons
                                        alternative: [
                                            (_ [alternative: (_) consequence: (_) ] @cons)
                                            (block) @cons])
                                    (for_statement
                                        body: (block) @cons)
                                    (while_statement
                                        (block) @cons)
                                    (switch_expression
                                        body: (switch_block (switch_block_statement_group) @cons))
                                    (try_statement body: (block) @cons)
                                    (try_statement (catch_clause body: (block) @cons))]))
        """,
        "constructor_control_flow": """
                                (constructor_declaration
                                    body: (constructor_body [
                                    (if_statement
                                        consequence: (_) @cons)
                                    (if_statement
                                        consequence: (_) @cons
                                        alternative: [
                                            (_ [alternative: (_) consequence: (_) ] @cons)
                                            (block) @cons])
                                    (for_statement
                                        body: (block) @cons)
                                    (while_statement
                                        (block) @cons)
                                    (switch_expression
                                        body: (switch_block (switch_block_statement_group) @cons))
                                    (try_statement body: (block) @cons)
                                    (try_statement (catch_clause body: (block) @cons))]))
        """,
        "nested_controlflow_subsequent_nodes": """
                                (_ [
                                    (if_statement
                                        consequence: (_) @cons)
                                    (if_statement
                                        consequence: (_) @cons
                                        alternative: [
                                            (_ [alternative: (_) consequence: (_) ] @cons)
                                            (block) @cons])
                                    (for_statement
                                        body: (block) @cons)
                                    (while_statement
                                        (block) @cons)
                                    (switch_expression
                                        body: (switch_block (switch_block_statement_group) @cons))
                                    (try_statement body: (block) @cons)
                                    (try_statement (catch_clause body: (block) @cons))])
                                """,
    },
}
