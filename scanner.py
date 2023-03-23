from constants import *
from arc_error import *
from sys import modules
from arc_util import *
from file import InFile
from enum2s import ENUM_TO_STRING # this import hinders speed

def tok_enum2s(idx):
    return ENUM_TO_STRING[idx] if 'enum2s' in modules else idx

class Token():

    def __init__(self, token_type, token_value, line_no, file_ptr):
        self.token_type = token_type
        self.token_value = token_value
        self.line_no = line_no
        self.file_ptr = file_ptr

    def get_type(self):
        return self.token_type

    def get_value(self):
        return self.token_value

    def get_type_and_val(self):
        return (self.token_type, self.token_value)

    def get_line_no(self):
        return self.line_no

    def get_file_ptr(self):
        return self.file_ptr

    def __str__(self):
        return 'TOKEN: type=\'{0}\', value=\'{1}\', line number={2}, file id={3}'.format(tok_enum2s(self.token_type),
                                                                                                    self.token_value,
                                                                                                    self.line_no,
                                                                                                    self.file_ptr)


class Tokenizer():

    _line_no = 1
    _basic_assertions = {DEFINE:IDENTIFIER,
                         DEF_PARAM_END:BLOCK_START,
                         DEF_SEPERATOR:DEF_PARAM,
                         CALL_SEPERATOR:CALL_PARAM}
    _b_depth = 0
    _p_depth = 0
    _reserved_name_index = ['var', 'function' 'for', 'if', 'else', 'while',
                            'break', 'continue', 'function', 'return', 'include']
    _variable_name_index = []
    _operator_index = ['+', '-', '/', '*', '>', '<', '=', '==', '&&', '||', '%', '/*']
    _tokens = []
    # binary cases for _get_type_by_name
    _type_bin = {VARIABLE:DEFINE,
                 CONSTANT_VARIABLE:CONST_DEFINE,
                 FUNCTION:FUNC_DECL,
                 SEMICOLON:STATEMENT_END,
                 OPEN_CURLBRACKET:BLOCK_START,
                 CLOSE_CURLBRACKET:BLOCK_END}
    _ready = 0
    _infile = None
    _infiles = []

    def __init__(self, filepath, source_loc, fileptr):
        self._file_path = filepath
        self._source = source_loc
        self._current_file = fileptr

    def set_file(self, file):
        self._infiles.append(file)
        self._current_file += 1
        self._infile = self._infiles[self._current_file]

    def top_file_complete(self):
        self._infile.close()
        self._current_file -= 1
        self._infile = self._infiles[self._current_file]

    def _open_local_import(self, filename):
        local_import = InFile(self._file_path, filename)
        self.set_file(local_import)
        self.tokenize()
        self.top_file_complete()

    def _eat_space(self):
        return self._infile.readc()

    def _eat_newline(self):
        self._infile.readc()
        self._line_no += 1

    def _next_word(self, current):
        word = current
        nextchar = self._infile.next()
        if is_symbol(current):
            if is_chain_start(current):
                chain_endpoint = get_chain_endpoint(current)
                while True:
                    nextchar = self._infile.readc()
                    word += nextchar
                    if nextchar == chain_endpoint:
                        break
            elif is_symbol(nextchar) and not PAREN(nextchar) and not CURLBRACKET(nextchar):
                second_op = self._infile.readc()
                word = word + second_op
                if word == '/*':
                    while self._next_word(self._infile.readc()) != '*/':
                        pass
        elif is_statement_end(current):
            pass
        else:
            while is_valid_word_char(nextchar):
                word = word + nextchar
                self._infile.readc()
                nextchar = self._infile.next()
        return word

    def get_next_non_stnl(self, curr):
        while is_stnl(curr):
            curr = self._infile.readc()
        return curr

    def clear_tokens(self):
        self._line_no = 1
        self._b_depth = 0
        self._p_depth = 0
        self._tokens = []
        self._variable_name_index = []
        self._ready = 0
        if self._infile:
            self._infile.close()
        self._infile = None

    def get_tokens(self):
        return self._tokens

    def _get_tokens_size(self):
        return len(self._tokens)

    def _get_last_token(self, idx=-1):
        if self._get_tokens_size() < abs(idx):
            raise ARCLexLastTokenOutOfRange("_get_last_token cant reference an index that doesnt exist")
        return self._tokens[idx]

    def get_variable_names(self):
        return self._variable_name_index

    def remove_tsnl(self, word):
        # (todo): Let this function check directly for newlines and increment lineno.
        return word.replace(" ", "").replace("\t", "").replace("\n", "")

    def _create_token(self, word, given_type=None):
        if word is EMPTY:
            return
        word = self.remove_tsnl(word)
        token_type = given_type or self._get_type_by_name(word)
        if token_type == C_IMPORT: word = word[2:len(word)-2]
        elif token_type == LOCAL_IMPORT_PATH or token_type == STRING or token_type == NATIVE_IMPORT:
            word = word[1:len(word)-1]
        if token_type is IDENTIFIER:
            if word not in self._variable_name_index:
                self._variable_name_index.append(word)
        tok = Token(token_type, word, self._line_no, self._current_file)
        self._tokens.append(tok)

    def _assert_syntax(self, last, current):
        if last in self._basic_assertions:
            expect(self._basic_assertions[last], current, self._line_no)

    def _get_type_by_name(self, name):

        token_type = None
        last_tok = self._get_last_token()
        last_type, last_name = last_tok.get_type_and_val()

        # If name has a 1:1 type representation.
        if name in self._type_bin:
            token_type = self._type_bin[name]

        # If name is a complete chained structure, e.g. "", '', <>.
        elif is_string(name):
            if last_type == INCLUDE:
                token_type = LOCAL_IMPORT_PATH
            else:
                token_type = STRING

        # If name begins with '<' and ends with '>'.
        elif is_c_import(name):
            if name[1] == '"':
                token_type = C_IMPORT
            else:
                token_type = NATIVE_IMPORT

        # If name is a group of alpha characters.
        elif is_vname(name):
            # if name is a reserved word
            if name in self._reserved_name_index:
                token_type = get_reserved_name_type(name)
            else:
                # DEF/CALL CHAINING
                # if last type is indicative of def
                if last_type == DEF_PARAM_LIST or last_type == DEF_SEPERATOR:
                    token_type = DEF_PARAM
                # if last type is indicative of call
                elif last_type == CALL_PARAM_LIST or last_type == CALL_SEPERATOR:
                    token_type = CALL_PARAM
                # fallback
                else:
                    token_type = IDENTIFIER


        # If name is a group of digits.
        elif is_constant(name):
            token_type = get_initial_c_type(name)

        # If name is indicative of an equation. (deprecated)
        elif is_equation(name):
            token_type = EQUATION

        # If name is +, -, /, *, >, <, =, ==, &&, ||, %, or /*.
        elif name in self._operator_index:
            token_type = get_operator_type(name, last_type)

        # Open parenthesis
        elif name == OPEN_PAREN:
            two_back = self._get_last_token(-2).get_type()
            # if pattern is "x = ("
            if two_back == FUNC_DECL:
                token_type = DEF_PARAM_LIST
            # if pattern is "x("
            elif last_type == IDENTIFIER:
                # the token for this will be name(
                token_type = CALL_PARAM_LIST
            # fallback
            else:
                token_type = EQUATION_START

        # Closing parenthesis
        elif name == CLOSE_PAREN:
            # def chain
            if last_type == DEF_PARAM_LIST or last_type == DEF_PARAM:
                token_type = DEF_PARAM_END
            # call chain
            elif last_type == CALL_PARAM_LIST or last_type == CALL_PARAM:
                token_type = CALL_PARAM_END
            # fallback
            else:
                token_type = EQUATION_END

        # Comma
        elif name == COMMA:
            # call chain
            if last_type == CALL_PARAM:
                token_type = CALL_SEPERATOR
            # def chain
            elif last_type == DEF_PARAM:
                token_type = DEF_SEPERATOR
            # fallback for pattern "var x = 3,"
            elif last_type == DEFINITION:
                token_type = VAR_SEPERATOR

        return token_type

    def tokenize(self):

        # Stub token to avoid index errors when backreferencing.
        last_token = self._create_token('sop', START_OF_PROGRAM)

        while True:

            # STEPS:

            # Eat '\n' if the last token was ';'.
            if last_token == STATEMENT_END: self._eat_newline()

            # Read a character from infile stream.
            curr = self._infile.readc()

            # If curr is a sentinel value: break the loop.
            if self._infile.eof(): break

            # If curr is \s, \t, or \n: find the next non s/t/nl value.
            if is_stnl(curr): curr = self.get_next_non_stnl(curr)

            # Find the next word boundary and store it in next_word.
            next_word = self._next_word(curr)

            # Create a full token out of next_word.
            self._create_token(next_word)

            # Get the newly created token's type.
            current_token = self._get_last_token().get_type()

            # Check for possible syntax errors.
            self._assert_syntax(last_token, current_token)

            # If the token is a local import: run a seperate instance of tokenize for path/last_token_value.
            if current_token == LOCAL_IMPORT_PATH:
                self._open_local_import(self._get_last_token().get_value())

            # Adjust block scope depth.
            if current_token == BLOCK_START: self._b_depth += 1
            if current_token == BLOCK_END: self._b_depth -= 1

            # Overwrite last_token.
            last_token = current_token

        # Catch simple scope errors here.
        expect(0, self._b_depth)
        expect(0, self._p_depth)

    def __str__(self):
        for token in self.get_tokens():
            print(token)




