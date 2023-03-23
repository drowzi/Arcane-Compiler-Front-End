#(todo): Change strings into enumerations where possible.

# Config
DEBUG_MODE = 1
DEBUG_LOG_FILE = 0
FRONTEND_LOG = 1
LOG_FILE = 'debug.log'
NATIVE_LIB_PATH_D = r'C:\Users\Allen\Desktop\Programming\Language Design\Arcane compiler\1\arcane\native_lib'
NATIVE_LIB_PATH_R = r'r\native_lib'
FILE_EXT = '.arc'

# Frequently used strings
NL = '\n'
SPACE = ' '
EMPTY = ''
BACKSLASH = '\\'
DASH = '-'
COMMA = ','
SEMICOLON = ';'
OPEN_PAREN = '('
CLOSE_PAREN = ')'
PAREN = lambda x: x is OPEN_PAREN or x is CLOSE_PAREN
OPEN_CURLBRACKET = '{'
CLOSE_CURLBRACKET = '}'
CURLBRACKET = lambda x: x is OPEN_CURLBRACKET or x is CLOSE_CURLBRACKET
OPEN_SQBRACKET = '['
CLOSE_SQBRACKET = ']'
COMMENT_START = '*/'
COMMENT_END = '\*'
SQBRACKET = lambda x: x is OPEN_SQBRACKET or x is CLOSE_SQBRACKET
VARIABLE = 'var'
CONSTANT_VARIABLE = 'const'
FUNCTION = 'function'

# Enums

TYPE_SLOT = 0
TOKEN_SLOT = 1

NODE_DEFAULT = -1
NODE_PROGRAM = 0
NODE_STATEMENT = 1
NODE_IDENTIFIER = 2
NODE_LITERAL = 3
NODE_FUNCTION_STATEMENT = 4
NODE_ARGUMENT = 5
NODE_ARGUMENTS = 6
NODE_BLOCK = 7
NODE_FUNCTION_DECL = 8
NODE_CONDITION = 9
NODE_BRANCH = 10
NODE_RETURN = 11
NODE_ASSIGN = 12
NODE_OP = 13
NODE_UNARY = 14
NODE_IMPORT = 15

DEFINE = 0
CONST_DEFINE = 1
FUNC_DECL = 2
CONSTANT = 3
F_RETURN = 4
STATEMENT_END = 5
BLOCK_START = 6
BLOCK_END = 7
IDENTIFIER = 8
EQUATION = 9
ASSIGN = 10
DEF_PARAM_LIST = 11
DEF_PARAM = 12
DEF_SEPERATOR = 13
DEF_PARAM_END = 14
CALL_PARAM_LIST = 15
CALL_PARAM = 16
CALL_SEPERATOR = 17
CALL_PARAM_END = 18
VAR_SEPERATOR = 19
EQUATION_END = 20
DEFINITION = 21
OPERATOR = 22
COND_IF = 23
COND_ELSE = 24
COND_FOR = 25
COND_WHILE = 26
INCLUDE = 27
LOCAL_IMPORT_PATH = 28
C_IMPORT = 29
NATIVE_IMPORT = 30
EQUATION_START = 31
SEPERATOR = 32
START_OF_PROGRAM = 33
START_OF_FILE = 34
ADD = 35
SUBTRACT = 36
DIVIDE = 37
MULTIPLY = 38
GREATER_THAN = 39
LESS_THAN = 40
ARRAY = 41
LOG_EQUALS = 42
LOG_AND = 43
LOG_OR = 44
MODULO = 45
COMMENT = 46
POSTFIX_INC = 47
POSTFIX_DEC = 48
FUNC_CALL = 49
ARRAY_START = 50
ARRAY_END = 51
PREFIX_INC = 52
PREFIX_DEC = 53
UNARY_MINUS = 54
LOG_NOT = 55
GREATER_THAN_OR_EQUAL = 56
LESS_THAN_OR_EQUAL = 57
LOG_NOTEQUAL = 58
STRING = 59
UNARY_PLUS = 60
RW_BREAK = 61
RW_CONTINUE = 62

# Numeros
SIGNED_CHAR = 200
UNSIGNED_CHAR = 201
SIGNED_INT = 202
UNSIGNED_INT = 203
SIGNED_LONG = 204
UNSIGNED_LONG = 205
NUMBER_TYPES = [SIGNED_CHAR, UNSIGNED_CHAR, SIGNED_INT, UNSIGNED_INT, SIGNED_LONG, UNSIGNED_LONG]

EQ_NORMAL = 0
EQ_CONDITION = 1
EQ_FUNCTION_CALL = 2

# Collections
SYMBOL_LIST = set(['+', '-', '/', '*', '>', '<', '=', '(', ')', ',', '&&', '||', '{', '}', '%', '"', '\'', '\\', '/'])

RESERVED_NAME_LIST = {'var':IDENTIFIER,
                      'function':FUNC_DECL,
                      'for':COND_FOR,
                      'if':COND_IF,
                      'else':COND_ELSE,
                      'while':COND_WHILE,
                      'break':RW_BREAK,
                      'continue':RW_CONTINUE,
                      'return':F_RETURN,
                      'include':INCLUDE}

TYPE_PAIRS = {'+': ADD, '-': SUBTRACT, '/': DIVIDE, '*': MULTIPLY, '>': GREATER_THAN, '<': LESS_THAN, '=': ASSIGN, '==': LOG_EQUALS, '&&': LOG_AND, '||': LOG_OR, '%': MODULO, '/*': COMMENT}

OPERATOR_TYPES = [ADD, SUBTRACT, DIVIDE, MULTIPLY, GREATER_THAN, LESS_THAN, ASSIGN, LOG_AND, LOG_OR, UNARY_MINUS, LOG_EQUALS, MODULO]

EPRL, EPLR = range(2) # ASSOCIATIVITY ENUM

# http://en.cppreference.com/w/c/language/operator_precedence
EQUATION_PRECEDENCE = {POSTFIX_INC: {"precedence": 22, "associativity": EPLR},
                       POSTFIX_DEC: {"precedence": 21, "associativity": EPLR},
                       FUNC_CALL: {"precedence": 20, "associativity": EPLR},
                       ARRAY: {"precedence": 19, "associativity": EPLR},
                       PREFIX_INC: {"precedence": 18, "associativity": EPRL},
                       PREFIX_DEC: {"precedence": 17, "associativity": EPRL},
                       UNARY_MINUS: {"precedence": 16, "associativity": EPRL},
                       LOG_NOT: {"precedence": 15, "associativity": EPRL},
                       MULTIPLY: {"precedence": 14, "associativity": EPLR},
                       DIVIDE: {"precedence": 13, "associativity": EPLR},
                       MODULO: {"precedence": 12, "associativity": EPLR},
                       ADD: {"precedence": 11, "associativity": EPLR},
                       SUBTRACT: {"precedence": 10, "associativity": EPLR},
                       LESS_THAN: {"precedence": 9, "associativity": EPLR},
                       LESS_THAN_OR_EQUAL: {"precedence": 8, "associativity": EPLR},
                       GREATER_THAN: {"precedence": 7, "associativity": EPLR},
                       GREATER_THAN_OR_EQUAL: {"precedence": 6, "associativity": EPLR},
                       LOG_EQUALS: {"precedence": 5, "associativity": EPLR},
                       LOG_NOTEQUAL: {"precedence": 4, "associativity": EPLR},
                       LOG_AND: {"precedence": 3, "associativity": EPLR},
                       LOG_OR: {"precedence": 2, "associativity": EPLR},
                       ASSIGN: {"precedence": 1, "associativity": EPRL},
                       SEPERATOR: {"precedence": 0, "associativity": EPLR},
                       EQUATION_START: {"precedence": -1, "associativity": EPLR}}
