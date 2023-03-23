import os
import sys
import re
import subprocess
import time
from constants import *
from arc_error import *
from arc_logger import get_log_handle
from file import InFile, OutFile
from gen import *
from s_table import SymbolTable
from scanner import Tokenizer
from source_ref import SourceRef
from parse import Parser
from preprocessing import *

mainlogger = get_log_handle('main')

# (todo): rewrite the arcane class, hide info in main within class, and add .run() command.

class Arcane():

    _files = list()

    def __init__(self, path, name):
        self._start_time = time.time()
        self._source_loc = SourceRef()
        self._symbol_table = SymbolTable()
        self._path_to_file = path
        self._infile = InFile(path, name)
        self.addf(self._infile)
        self._lex = Tokenizer(filepath=self._path_to_file, source_loc=self._source_loc, fileptr=-1)

    def addf(self, f):
        self._files.append(f)

    def set_lex(self):
        """pass file instance to lex"""
        self._lex.set_file(self._infile)

    def lex(self):
        self.set_lex()
        self._lex.tokenize()
        self.set_tokens(self._lex.get_tokens())
        mainlogger.debug("Tokenizer successfully ran with no apparent errors.")

    def set_tokens(self, tokens):
        self._tokens = tokens

    def get_tokens(self):
        return self._tokens

    def parse(self):
        if not self._tokens:
            mainlogger.warning("Arcane.parse had no tokens to parse.")
            return
        else:
            self._parser = Parser(tokens=self._tokens)
            node = self._parser._ast.get_next_node(self._parser._ast.get_head(), 0)
            for t in range(20):
                print(node)
                node = self._parser._ast.get_next_node(node, 0)

    def generate_files(self):
        generate_output_files(self._path_to_file)

    def get_ast(self):
        return self._parser.get_ast_dict()

    def get_file_count(self):
        return len(self._files)

    def clean(self):
        for f in self._files:
            f.close()
            assert(f.closed)
        mainlogger.info("Successfully closed all files.")

    def print_frontend_log(self):
        # make a class for this later
        frontend_log = open(self._path_to_file+"frontendlogs/log.txt", 'w')
        # write source here
        frontend_log.write("----------\nTOKEN_DUMP\n----------\n")
        for token in self._lex.get_tokens():
            frontend_log.write(token.__str__()+'\n')
        frontend_log.write("----------\nAST_DUMP\n----------\n")
        frontend_log.write(self.get_ast())
        frontend_log.close()


def main(path, src):

    # Setup
    arc_st = time.time()
    arc = Arcane(path, src)

    # Lexical analysis
    arc.set_lex()
    arc_lex_st = time.time()
    arc.lex()
    arc_lex_et = time.time()
    mainlogger.debug("[time taken] Lexical analysis: {0} seconds".format(arc_lex_et - arc_lex_st))

    # Syntax analysis
    arc_parse_st = time.time()
    arc.parse()
    arc_parse_et = time.time()
    mainlogger.debug("[time taken] Syntax analysis: {0} seconds".format(arc_parse_et - arc_parse_st))

    if FRONTEND_LOG: arc.print_frontend_log()

    # Preprocessing

    # Code generation

    # Code optimization

    # Debug stats
    #print("LIST OF VARIABLE NAMES:\N{0}".format(arc._lex.get_variable_names()))
    #print("LIST OF TOKENS (__str__):\n{0}".format(arc._lex.__str__()))
    #print("LIST OF TOKENS:\n{0}".format(arc._lex.get_tokens()))
    #print("AST NODES:\n{0}".format(arc.get_ast()))

    # Cleanup & runtime
    arc.clean()
    arc_et = time.time()
    mainlogger.debug("[time taken] ARC: {0} seconds".format(arc_et - arc_st))

# 1 = run interpreter, 0 = run test suites
if __name__ == '__main__':
    try:
        source_file = sys.argv[1]
        ext = re.search(r'\.(\w)+$', source_file).group(0)
        mainlogger.debug("Source argument is present, checking for extension {}...".format(FILE_EXT))
        assert(ext==FILE_EXT)
        mainlogger.debug("Extension is correct, proceeding to parse file.")
    except:
        raise ARCFileNotFound("No file given.")
    # build
    #main(os.path.join(os.path.dirname(__file__)), source_file)
    # debug
    main(path='debug/', src=source_file)
else:
    # Test suite config goes here for now
    # mask logging from test suite with a fake import to avoid large amounts of log calls when testing cases
    def do_nothing(x):
        return
    if not dir().__contains__('logging'):
        class logging():
            pass

        for prop in ['info', 'debug', 'warning', 'error', 'critical']:
            setattr(logging, prop, do_nothing)