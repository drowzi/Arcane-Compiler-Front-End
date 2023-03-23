
DEFINE = 'DEFINE'
CONST_DEFINE = 'CONST_DEFINE'
FUNC_DECL = 'FUNC_DECL'
CONSTANT = 'CONSTANT'
F_RETURN = 'RETURN'
STATEMENT_END = 'STATEMENT_END'
BLOCK_START = 'BLOCK_START'
BLOCK_END = 'BLOCK_END'
IDENTIFIER = 'IDENTIFIER'
EQUATION = 'EQUATION'
ASSIGN = 'ASSIGN'
DEF_PARAM_LIST = 'DEF_PARAM_LIST'
DEF_PARAM = 'DEF_PARAM'
DEF_SEPERATOR = 'DEF_SEPERATOR'
DEF_PARAM_END = 'DEF_PARAM_END'
CALL_PARAM_LIST = 'CALL_PARAM_LIST'
CALL_PARAM = 'CALL_PARAM'
CALL_SEPERATOR = 'CALL_SEPERATOR'
CALL_PARAM_END = 'CALL_PARAM_END'
VAR_SEPERATOR = 'VAR_SEPERATOR'
EQUATION_END = 'EQUATION_END'
DEFINITION = 'DEFINITION'
OPERATOR = 'OPERATOR'
COND_IF = 'IF'
COND_ELSE = 'ELSE'
COND_FOR = 'FOR'
COND_WHILE = 'WHILE'

SIGNED_CHAR = 'SIGNED_CHAIR'
UNSIGNED_CHAR = 'UNSIGNED_CHAR'
SIGNED_INT = 'SIGNED_INT'
UNSIGNED_INT = 'UNSIGNED_INT'
SIGNED_LONG = 'SIGNED_LONG'
UNSIGNED_LONG = 'UNSIGNED_LONG'

EPRL, EPLR = range(2) # ASSOCIATIVITY ENUM
EQUATION_PRECEDENCE = {"POSTFIX_INCREMENT": {"precedence": 22, "associativity": EPLR},
                       "POSTFIX_DECREMENT": {"precedence": 21, "associativity": EPLR},
                       "FUNCTION_CALL": {"precedence": 20, "associativity": EPLR},
                       "ARRAY": {"precedence": 19, "associativity": EPLR},
                       "PREFIX_INCREMENT": {"precedence": 18, "associativity": EPRL},
                       "PREFIX_DECREMENT": {"precedence": 17, "associativity": EPRL},
                       "UNARY_MINUS": {"precedence": 16, "associativity": EPRL},
                       "NOT": {"precedence": 15, "associativity": EPRL},
                       "MULTIPLY": {"precedence": 14, "associativity": EPLR},
                       "DIVIDE": {"precedence": 13, "associativity": EPLR},
                       "MODULO": {"precedence": 12, "associativity": EPLR},
                       "ADD": {"precedence": 11, "associativity": EPLR},
                       "SUBTRACT": {"precedence": 10, "associativity": EPLR},
                       "LESS_THAN": {"precedence": 9, "associativity": EPLR},
                       "LESS_THAN_OR_EQUAL": {"precedence": 8, "associativity": EPLR},
                       "GREATER_THAN": {"precedence": 7, "associativity": EPLR},
                       "GREATER_THAN_OR_EQUAL": {"precedence": 6, "associativity": EPLR},
                       "EQUALS": {"precedence": 5, "associativity": EPLR},
                       "NOT_EQUAL": {"precedence": 4, "associativity": EPLR},
                       "AND": {"precedence": 3, "associativity": EPLR},
                       "OR": {"precedence": 2, "associativity": EPLR},
                       "ASSIGN": {"precedence": 1, "associativity": EPRL},
                       "SEPERATOR": {"precedence": 0, "associativity": EPLR},
                       "EQUATION_START": {"precedence": -1, "associativity": EPLR}}


TYPE_PAIRS = {'+': 'ADD', '-': 'SUBTRACT', '/': 'DIVIDE', '*': 'MULTIPLY', '>': 'GREATER_THAN', '<': 'LESS_THAN', '=': 'ASSIGN', '==': 'EQUALS', '&&': 'AND', '||': 'OR', '%': 'MODULO', '/*': "COMMENT"}
OPERATOR_TYPES = ['ADD', 'SUBTRACT', 'DIVIDE', 'MULTIPLY', 'GREATER_THAN', 'LESS_THAN', 'ASSIGN', 'AND', 'OR', 'UNARY_MINUS', 'POWER', 'EQUALS', 'MODULO']

