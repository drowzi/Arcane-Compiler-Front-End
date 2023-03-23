import itertools
from constants import *
from arc_error import *

def expect(expected, given, lineno=None):
    if type(expected) is not list:
        expected = [expected]
    for item in expected:
        if item == given:
            return
    raise ARCSyntaxError("line: {0}, expected: {1}, given: {2}".format(lineno, expected, given))

def between(number, min, max):
    return number >= min and number <= max

# TOKEN RESOLUTION HELPERS

def is_vname(name):
    for char in name:
        if char.isalpha():
            return 1
    return 0

def is_constant(name):
    return name.isdigit() or (name[0] is '-' and name[1:].isdigit())

def is_statement_end(char):
    return char == SEMICOLON

def is_chain_start(word):
    return word in ['"', '\'', '<']
    #return word == '"' or word == '\'' or word == '<'

def is_stnl(c):
    return c in [SPACE, '\t', '\n']
    #return c == SPACE or c == '\t' or c == '\n'

def is_c_import(word):
    length = len(word)
    return length > 0 and word[0] == '<' and word[length-1] == '>'

def get_chain_endpoint(word):
    return '>' if word == '<' else word

def is_symbol(char):
    return char in SYMBOL_LIST

def is_string(word):
    length = len(word)
    first = word[0]
    if is_chain_start(first):
        return length > 0 and word[0] == first and word[length-1] == first
    else:
        return 0

def is_equation(chars):
    """ Equation recognition """
    constant_count = symbol_count = 0
    for char in chars:
        if is_constant(char):
            constant_count += 1
        elif is_symbol(char):
            symbol_count += 1
    return symbol_count > 0 and constant_count > 1

def is_valid_word_char(c):
    """ Find if a char is indicative of a word. """
    return c not in itertools.chain([SPACE, NL, SEMICOLON, EMPTY], SYMBOL_LIST)
    #return c is not SPACE and c is not NL and c is not SEMICOLON and c is not EMPTY and not is_symbol(c)

def is_unary_op(type):
    return type in [UNARY_MINUS, UNARY_PLUS]
    #return type == UNARY_MINUS or type == UNARY_PLUS

def is_binary_op(type):
    return

def get_statement_type(name):
    return 'CONSTANT'

def type_is_operator(type):
    return type in OPERATOR_TYPES

def get_reserved_name_type(name):
    return RESERVED_NAME_LIST[name]

def get_equation_precedence(op):
    return EQUATION_PRECEDENCE[op]["precedence"]

def get_operator_type(op, last_type=None):
    type = None
    if op in TYPE_PAIRS:
        type = TYPE_PAIRS[op]
        if type == SUBTRACT and type_is_operator(last_type):
            # may break with increment operators, 'x = y++ - 3;"
            type = UNARY_MINUS
    else:
        raise ARCUtilError("get_operator_type could not find the type for operator {0}.".format(op))
    return type

def get_initial_c_type(n):
    """
    return c number types.
    (notes):
          -This is just an initial setter, a lot of these types will be wrong.
          -Make sure you evaluate the program later to properly set these types.
    """
    n = int(n)
    n_between = lambda x,y: between(n, x, y)
    c_type = None
    if n_between(-128, -1):
        c_type = SIGNED_CHAR
    elif n_between(0, 255):
        c_type = UNSIGNED_CHAR
    elif n_between(-32768, -1):
        c_type = UNSIGNED_INT
    elif n_between(0, 65535):
        c_type = SIGNED_INT
    elif n_between(-2147483648, -1):
        c_type = UNSIGNED_LONG
    elif n_between(0, 4294967295):
        c_type = SIGNED_LONG
    return c_type

if __name__ == '__main__':
    pass
    #print(is_valid_word_char(""))
    #expect([';', '{'], 'func', 32)