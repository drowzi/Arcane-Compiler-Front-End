import unittest
from arc import *

# Helpers

def load_file(this, file_name):
    this.file = InFile(this.test_dir, file_name)
    this.t.set_file(this.file)

def load_file_and_tokenize(this, file_name, print_out):
    """ used by TestLex """
    this.t.clear_tokens()
    load_file(this, file_name)
    this.t.tokenize()
    if print_out:
        print(this.t.get_tokens())
    this.file.close()

# Test cases

class TestIO(unittest.TestCase):

    inputfile = InFile('testcases/', 'test.arc')
    outputfile = OutFile('testcases/', 'out.c')

    def test_input_load_read_close(self):
        self.assertTrue(self.inputfile.lookahead(1) == ':')
        self.assertEqual(self.inputfile.readc(), ':')
        self.assertEqual(self.inputfile.readln(), 'TESTING INPUT\n')
        self.assertTrue(self.inputfile.lookbehind(6) == 'INPUT\n')
        self.inputfile.close()
        self.outputfile.close()

    def test_output_load_write_close(self):
        pass

"""
class TestLex(unittest.TestCase):

    test_dir = 'testcases/test_tokens/'
    t = Tokenizer()

    def test_token_assignment(self):
        tokens = [('START_OF_PROGRAM', 'sop'), ('DEFINE', 'var'), ('IDENTIFIER', 'x'), ('ASSIGN', '='), ('UNSIGNED_CHAR', '3'),
                  ('STATEMENT_END', ';'), ('DEFINE', 'var'), ('IDENTIFIER', 'y'), ('ASSIGN', '='), ('UNARY_MINUS', '-'), ('UNSIGNED_CHAR', '3'),
                  ('STATEMENT_END', ';'), ('DEFINE', 'var'), ('IDENTIFIER', 'z'), ('ASSIGN', '='), ('IDENTIFIER', 'x'), ('STATEMENT_END', ';')]
        load_file_and_tokenize(self, 'assignment.arc', print_out=0)
        self.assertTrue(self.t.get_tokens() == tokens)

    def test_token_equation(self):
        tokens = [('START_OF_PROGRAM', 'sop'), ('DEFINE', 'var'), ('IDENTIFIER', 'x'), ('ASSIGN', '='), ('UNSIGNED_CHAR', '3'),
                  ('ADD', '+'), ('UNSIGNED_CHAR', '5'), ('MULTIPLY', '*'), ('UNSIGNED_CHAR', '7'), ('DIVIDE', '/'),
                  ('UNSIGNED_CHAR', '11'), ('STATEMENT_END', ';')]
        load_file_and_tokenize(self, 'equation.arc', print_out=0)
        self.assertTrue(self.t.get_tokens() == tokens)

    def test_token_function_def(self):
        tokens = [('START_OF_PROGRAM', 'sop'), ('FUNC_DECL', 'function'), ('IDENTIFIER', 'func'), ('DEF_PARAM_LIST', '('),
                  ('DEF_PARAM', 'x'), ('DEF_SEPERATOR', ','), ('DEF_PARAM', 'y'), ('DEF_PARAM_END', ')'),('BLOCK_START', '{'),
                  ('BLOCK_END', '}'), ('STATEMENT_END', ';')]
        load_file_and_tokenize(self, 'function_def.arc', print_out=0)
        self.assertTrue(self.t.get_tokens() == tokens)

    def test_token_function_call(self):
        tokens = [('START_OF_PROGRAM', 'sop'), ('IDENTIFIER', 'func'), ('CALL_PARAM_LIST', '('), ('CALL_PARAM', 'x'),
                  ('CALL_SEPERATOR', ','), ('CALL_PARAM', 'y'), ('CALL_PARAM_END',')'), ('STATEMENT_END', ';')]
        load_file_and_tokenize(self, 'function_call.arc', print_out=0)
        self.assertTrue(self.t.get_tokens() == tokens)

    def test_token_constant(self):
        tokens = [('START_OF_PROGRAM', 'sop'), ('DEFINE', 'var'), ('IDENTIFIER', 'constant'), ('ASSIGN', '='),
                  ('UNSIGNED_CHAR', '35'), ('STATEMENT_END', ';'), ('DEFINE', 'var'), ('IDENTIFIER', 'neg_constant'),
                  ('ASSIGN', '='), ('UNARY_MINUS', '-'), ('UNSIGNED_CHAR', '35'), ('STATEMENT_END', ';')]
        load_file_and_tokenize(self, 'constant.arc', print_out=0)
        self.assertTrue(self.t.get_tokens() == tokens)


    def test_token_control_flow(self):
        # doesnt work yet, pass
        pass

    def test_syntax_function(self):
        self.assertRaises(ARCSyntaxError, load_file_and_tokenize, self, 'syntax_function_def.arc', print_out=0)

    def test_syntax_assign(self):
        self.assertRaises(ARCSyntaxError, load_file_and_tokenize, self, 'syntax_assign.arc', print_out=0)

    def test_syntax_block(self):
        self.assertRaises(ARCSyntaxError, load_file_and_tokenize, self, 'syntax_block.arc', print_out=0)
"""

if __name__ == 'main':
    testlogger = logging.getLogger()
    debuglogger.setLevel(50)
    unittest.main()