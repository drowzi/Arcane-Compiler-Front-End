from arc_util import *
from constants import *
from file import OutFile

class CodeSegment(object):
    """ Data structure for a segment of target code """

    def __init__(self):
        self.node_type = node_type
        self.return_type = return_type
        self.args = args
        self.source = source
        self.target = target
        # Pointer to the next segment. None=end
        self.next = None

class CodeRepr():

    _segments = []

    def __init__(self):
        # if segment.next is null: coderepr.next_segment()
        pass

    def add_segment(self, segment):
        self._segments.append(segment)

class CodeInspector():
    """ Inspects tree branches for information """

    def __init__(self):
        pass

    def get_identifier_type(self, identifier):
        pass

    def get_function_return_type(self, node):
        pass

    def eval_node(self, node):
        return node.get_node_type(), node.get_value()

class CodeGenerator():

    _buffer = ''

    def __init__(self, path, ast):
        self._out = OutFile(path, 'out.c')
        self.ast = ast
        self.inspect = CodeInspector()
        self.repr = CodeRepr()
        # Enumeration : Action
        self._actions = {NODE_PROGRAM: self._w_program,
                         NODE_STATEMENT: self._w_statement,
                         NODE_IDENTIFIER: self._w_ident,
                         NODE_LITERAL: self._w_literal,
                         NODE_FUNCTION_STATEMENT: self._w_fs,
                         NODE_ARGUMENT: self._w_arg,
                         NODE_ARGUMENTS: self._w_args,
                         NODE_BLOCK: self._w_block,
                         NODE_FUNCTION_DECL: self._w_fd,
                         NODE_CONDITION: self._w_cond,
                         NODE_BRANCH: self._w_branch,
                         NODE_RETURN: self._w_return,
                         NODE_ASSIGN: self._w_assign,
                         NODE_OP: self._w_op,
                         NODE_UNARY: self._w_unary,
                         NODE_IMPORT: self._w_import}

    def _w_fd(self, node):
        pass
        # get function return type
        # emit type name(
        # get/emit args
        # emitln ) {
        # while node isnt block_end
        # self.generate()
        # emitln }


    def _w_assign(self):
        # type(s) ptr?name = lit/iden/expr
        pass

    def _exec(self, event, context):
        return self._actions[event](context)

    def generate(self):
        # unpack repr one by one
        pass

    def generate_repr(self):
        # get node info, build segment, add to repr
        current_node = self.ast.get_next_node()
        assert(current_node.get_node_type == NODE_PROGRAM)
        while current_node is not None:
            node_type, node_value = self.inspect.eval_node(current_node)
            self._exec(node_type, node_value)
            current_node = self.ast.get_next_node()
