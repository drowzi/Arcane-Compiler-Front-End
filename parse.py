import json
from constants import *
from arc_logger import get_log_handle
from arc_util import *

#(todo): Fix ast.show_as_dict: it currently shows the incorrect children data for some nodes with manually set parents.

parselogger = get_log_handle('parser')

# (todo): Check the speed difference between a node dict factory and a node class.
def make_node(type, parent, value):
    return {"type": type,
            "parent": parent,
            "value": value,
            "children": {}}

class ASTNode():

    def __init__(self, parent=None, value=None):
        self.parent = parent
        self.children = []
        self.value = value or 'value_not_set'
        self.node_type = NODE_DEFAULT
        # Key representing this node's location in the parent's child list.
        self.parent_key = parent.get_key() if parent else 0
        # Key to be given to child nodes (parent_key).
        self.child_key = 0
        self.max_direct_children = 10000

    def is_head(self):
        return self.parent is None

    def add_children(self, children):
        if type(children) is not list:
            self.add_child(children)
        else:
            for child in children:
                self.add_child(child)

    def add_child(self, child):
        self.child_key += 1
        self.children.append(child)

    def get_parent_key(self):
        return self.parent_key

    def get_value(self):
        return self.value

    def get_key(self):
        return self.child_key

    def get_node_type(self):
        return self.node_type

    def get_max_children(self):
        return self.max_direct_children

    def get_data(self):
        return self.data

    def get_parent(self):
        return self.parent

    def get_child_at_idx(self, idx):
        if idx >= len(self):
            return None
        else:
            return self.children[idx]

    def set_max_children(self, amount):
        self.max_direct_children = amount

    def set_parent(self, parent):
        self.parent = parent
        self.parent_key = parent.get_key()

    def set_value(self, value):
        self.value = value

    def has_children(self):
        return len(self) > 0

    def get_all_children(self):
        all_children = []
        if self.has_children():
            for child in self.children:
                all_children.append(child)
                all_children = all_children + child.get_all_children()
        return all_children

    def __len__(self):
        return len(self.children)

    def __str__(self):
        return '[p_key={parent_key}]{class_name}(held_value={node_value})'.format(parent_key=str(self.get_parent_key()),
                                                                                  class_name=self.__class__.__name__,
                                                                                  node_value=str(self.get_value()))


class ProgramNode(ASTNode):
    # top of the tree, unlimited children nodes

    def __init__(self, parent=None, value=None):
        super().__init__(parent, value)
        self.node_type = NODE_PROGRAM


class StatementNode(ASTNode):
    # function representation, unlimited task nodes and one fallback return node

    def __init__(self, parent=None, value=None):
        super().__init__(parent, value)
        self.node_type = NODE_STATEMENT


class IdentifierNode(ASTNode):

    def __init__(self, parent=None, value=None):
        super().__init__(parent, value)
        self.node_type = NODE_IDENTIFIER


class LiteralNode(ASTNode):

    def __init__(self, parent=None, value=None, type=None):
        super().__init__(parent, value)
        self.type = type
        self.node_type = NODE_LITERAL

    def get_type(self):
        return self.type


class FunctionStatementNode(ASTNode):

    def __init__(self, parent=None, value=None):
        super().__init__(parent, value)
        self.node_type = NODE_FUNCTION_STATEMENT


class ArgumentNode(ASTNode):

    def __init__(self, parent=None, value=None):
        super().__init__(parent, value)
        self.node_type = NODE_ARGUMENT


class ArgumentsNode(ASTNode):

    def __init__(self, parent=None, value=None):
        super().__init__(parent, "ARGUMENTS")
        self.node_type = NODE_ARGUMENTS


class BlockNode(ASTNode):

    def __init__(self, parent=None, value=None):
        super().__init__(parent, value)
        self.node_type = NODE_BLOCK


class FunctionDeclNode(ASTNode):

    def __init__(self, parent=None, value=None):
        super().__init__(parent, value)
        self.node_type = NODE_FUNCTION_DECL


class ConditionNode(ASTNode):

    def __init__(self, parent=None, value=None):
        super().__init__(parent, value)
        self.node_type = NODE_CONDITION


class BranchNode(ASTNode):

    def __init__(self, parent=None, value=None):
        super().__init__(parent, value)
        self.node_type = NODE_BRANCH


class ReturnNode(ASTNode):
    """
        return
           |
        val/expr
    """

    def __init__(self, parent=None, value=None):
        super().__init__(parent, "RETURN")
        self.node_type = NODE_RETURN


class AssignNode(ASTNode):
    """
        assign
        /    \
    target  source
    (var)  (val/expr)
    """

    def __init__(self, parent=None, value=None):
        super().__init__(parent, value)
        self.node_type = NODE_ASSIGN


class OpNode(ASTNode):
    """
        op
       /  \
     op1  op2
    (v/e)(v/e)
    """

    def __init__(self, parent=None, value=None):
        super().__init__(parent, value)
        self.node_type = NODE_OP


class UnaryOpNode(ASTNode):
    """
        op
       /
     op1
    (v/e)
    """

    def __init__(self, parent=None, value=None):
        super().__init__(parent, value)
        self.set_max_children(1)
        self.node_type = NODE_UNARY


class ImportNode(ASTNode):

    def __init__(self, parent=None, value=None, import_type=None):
        super().__init__(parent, value)
        self.type = import_type
        self.node_type = NODE_IMPORT


class AST():


    def __init__(self):
        self._head = ProgramNode()

    def get_head(self):
        return self._head

    def get_next_node(self, head, idx):
        next_node = head.get_child_at_idx(idx)
        if next_node is None:
            if head == self._head:
                return None
            next_node = self.get_next_node(head.get_parent(), head.get_parent_key() + 1)
        return next_node

    def _show_as_dict(self, top):
        # (todo): Fix parse_expr assigning 0 to all children
        iter_children = 0
        ast_dict = {}
        while len(top) > iter_children:
            current_node = top.get_child_at_idx(iter_children)
            next_branch = self._show_as_dict(current_node)
            ast_dict.update({current_node.__str__():next_branch})
            iter_children += 1
        return ast_dict

    def __str__(self):
        return json.dumps(self._show_as_dict(self._head), sort_keys=True, indent=4)


def type_is_number(token_type):
    return token_type in NUMBER_TYPES

def type_is_expr(token_type):
    return token_type == UNARY_MINUS or token_type == EQUATION_START


class Parser():

    equation_endpoints = [STATEMENT_END, EQUATION_END, [CALL_SEPERATOR, CALL_PARAM_END]]

    def __init__(self, tokens):
        self._ast = AST()
        self._block_scope = 0
        self._tokenref = tokens
        self._tokenlen = len(tokens)
        self._tokenidx = 0
        self._tokencache = list()
        self.tokens_to_ast()

    def get_current_token(self):
        return self._tokenref[self._tokenidx]

    def get_current_token_type(self):
        return self.get_current_token().get_type()

    def get_current_token_value(self):
        return self.get_current_token().get_value()

    def get_token_cache(self):
        return self._tokenref[self._tokenidx:]

    def has_remaining_tokens(self):
        return self._tokenidx < self._tokenlen

    def eat_token(self, amount=1):
        self._tokenidx += amount

    def _get_equation_tokens(self, equation_type):
        eq_tokens = []
        endpoint = self.equation_endpoints[equation_type]
        token_type = self.get_current_token_type()
        if equation_type == EQ_FUNCTION_CALL:
            while token_type != endpoint[0] or token_type != endpoint[1]:
                eq_tokens.append(self.get_current_token())
                self.eat_token()
                token_type = self.get_current_token_type()
        else:
            while token_type != endpoint:
                eq_tokens.append(self.get_current_token())
                self.eat_token()
                token_type = self.get_current_token_type()
        return eq_tokens

    def parse_expr(self, current_parent, expr_tokens):
        """ Shunting-yard algorithm - https://en.wikipedia.org/wiki/Shunting-yard_algorithm """
        #print("Expression tokens passed: %s", expr_tokens)
        op_stack, out_queue, n_stack = [], [], []
        for t in range(len(expr_tokens)):
            current_type, current_val = expr_tokens[t].get_type_and_val()
            #print(current_type)
            if type_is_number(current_type) or current_type == IDENTIFIER:
                out_queue.append(expr_tokens[t])
            elif current_val == OPEN_PAREN:
                op_stack.append(expr_tokens[t])
            elif current_val == CLOSE_PAREN:
                while op_stack[len(op_stack)-1].get_type() != EQUATION_START:
                    newval = op_stack.pop()
                    out_queue.append(newval)
                op_stack.pop()
            elif type_is_operator(current_type):
                current_prec = get_equation_precedence(current_type)
                while op_stack and get_equation_precedence(op_stack[len(op_stack)-1].get_type()) >= current_prec:
                    newval = op_stack.pop()
                    out_queue.append(newval)
                op_stack.append(expr_tokens[t])
        while op_stack:
            newval = op_stack.pop()
            out_queue.append(newval)
        #print(out_queue)
        while out_queue:
            current_tok = out_queue.pop(0)
            current_type, current_val = current_tok.get_type_and_val()
            if type_is_number(current_type): # or type is func_call
                n_stack.append(([current_type, current_val], CONSTANT))
            elif current_type == IDENTIFIER:
                n_stack.append((current_val, IDENTIFIER))
            else:
                is_unary = is_unary_op(current_type)
                # pop first value as its always needed
                val_one, type_one = n_stack.pop()
                if is_unary:
                    op_node = UnaryOpNode(value=current_type)
                else:
                    op_node = OpNode(value=current_type)
                    # pop second value if binary
                    val_two, type_two = n_stack.pop()
                if type_one is OPERATOR:
                    n_node = val_one
                    n_node.set_parent(op_node)
                else:
                    n_node = LiteralNode(op_node, value=val_one[1], type=val_one[0]) if type_one is CONSTANT else IdentifierNode(op_node, value=val_one)
                if not is_unary:
                    if type_two is OPERATOR:
                        m_node = val_two
                        m_node.set_parent(op_node)
                    else:
                        m_node = LiteralNode(op_node, value=val_two[1],
                                             type=val_two[0]) if type_two is CONSTANT else IdentifierNode(op_node, value=val_two)
                    op_node.add_children([n_node, m_node])
                else:
                    op_node.add_child(n_node)
                n_stack.append((op_node, OPERATOR))
        #print("n_stack before popping the final value from the stack: ", n_stack)
        expr_tree = n_stack.pop()[0] # there should be one entry left, the tree head
        expr_tree.set_parent(current_parent)
        assert(len(n_stack) == 0)
        return expr_tree

    def _do_basic_assign(self, head, is_number=None):
        """ head -> LiteralNode or IdentifierNode """
        #if is_number is None: is_number = type_is_number(self.get_current_token()[TYPE_SLOT])
        value = self.get_current_token_value()
        self.eat_token(2)
        new_node = LiteralNode(head, value) if is_number else IdentifierNode(head, value)
        head.add_child(new_node)

    def _do_block(self, head):
        """ head -> BlockNode -> ... """
        self.eat_token(1)
        self._block_scope += 1
        entry_scope = self._block_scope
        bl_node = BlockNode(head, 'SCOPE='+str(self._block_scope))
        next_type = self.get_current_token_type()
        while True: # if '}' and scope=this_scope: break
            if next_type == BLOCK_END and self._block_scope == entry_scope:
                break
            self.parse(bl_node)
            next_type = self.get_current_token_type()
        self.eat_token(1)
        self._block_scope -= 1
        head.add_child(bl_node)

    def _do_define(self, head):
        """ head -> AssignNode -> IdentifierNode -> ... """
        self.eat_token(1)
        var_value = self.get_current_token_value()
        self.eat_token(2)
        a_node = AssignNode(head, ASSIGN)
        i_node = IdentifierNode(a_node, var_value)
        a_node.add_child(i_node)
        self.parse(a_node)
        head.add_child(a_node)

    def _do_else(self, head):
        self.eat_token(1)
        else_node = BlockNode(head, COND_ELSE)
        self.parse(else_node)
        head.add_child(else_node)

    def _do_expr(self, head):
        """ head -> ConditionNode or OpNode -> postfix_branches """
        expr_node = self.parse_expr(head, self._get_equation_tokens(EQ_NORMAL))
        head.add_child(expr_node)

    def _do_if(self, head):
        """
        head -> BranchNode -> ConditionNode -> postfix_branches
                              BlockNode(if) -> ...
                              BlockNode(else) -> ...
        """
        self.eat_token(2)
        b_node = BranchNode(head, 'IF_BRANCH')
        cond_node = self.parse_expr(b_node, self._get_equation_tokens(EQ_CONDITION))
        self.eat_token(1)
        b_node.add_child(cond_node)
        assert(self.get_current_token_type() == BLOCK_START)
        if_node = BlockNode(b_node, COND_IF)
        self.parse(if_node)
        b_node.add_child(if_node)
        if self.has_remaining_tokens() and self.get_current_token_type() == COND_ELSE:
            self._do_else(b_node)
        head.add_child(b_node)

    def _do_for(self, head):
        """
        head -> BranchNode -> BlockNode(while) -> ConditionNode -> postfix_branches
                              BlockNode(do) -> AssignNode
                                               BlockNode -> ...
        """
        self.eat_token(2)
        b_node = BranchNode(head, 'FOR_BRANCH')
        assign_block_node = BlockNode(b_node, 'FOR_INIT_ASSIGN') # collection of initial assignment statements
        while self.get_current_token_type() != STATEMENT_END:
            self._do_define(assign_block_node)
            if self.get_current_token_type() == VAR_SEPERATOR:
                self.eat_token(1)
        self.eat_token(1)
        b_node.add_child(assign_block_node)
        while self.get_current_token_type() != STATEMENT_END:
            cond_node = self.parse_expr(b_node, self._get_equation_tokens(EQ_CONDITION))
        self.eat_token(1)
        b_node.add_child(cond_node)
        do_prefix_node = BlockNode(b_node, 'FOR_PREFIX') # assignments to do before running the main do-block
        while self.get_current_token_type() != EQUATION_END:
            self._do_define(do_prefix_node)
            if self.get_current_token_type() == VAR_SEPERATOR:
                self.eat_token(1)
        self.eat_token(1)
        b_node.add_child(do_prefix_node)
        assert(self.get_current_token_type() == BLOCK_START)
        do_node = BlockNode(b_node, 'FOR_BLOCK')
        self.parse(do_node)
        b_node.add_child(do_node)
        head.add_child(b_node)

    def _do_func_call(self, head):
        """ head -> FunctionStatementNode -> ArgumentsNode -> ArgumentNode -> LiteralNode, IdentifierNode, or postfix_branches """
        func_name = self.get_current_token_value()
        self.eat_token(2)
        fc_node = FunctionStatementNode(head, func_name)
        args_node = ArgumentsNode(fc_node, 'FUNCTION_STATEMENT_ARGUMENTS')

    def _do_func_decl(self, head):
        """
        head -> FunctionDeclNode -> ArgumentsNode -> ArgumentNode
                                    BlockNode -> ...
                                    ReturnNode?
        """
        self.eat_token(1) # function
        func_name = self.get_current_token_value()
        self.eat_token(1) # function name
        f_node = FunctionDeclNode(head, func_name)
        args_node = ArgumentsNode(f_node, 'FUNC_DECL_PARAM')
        while True:
            self.eat_token(1) # eat ( and then every token until )
            current_token = self.get_current_token()
            current_type, current_value = current_token.get_type_and_val()
            if current_type == DEF_PARAM_END: break
            if current_type == DEF_PARAM:
                arg_node = ArgumentNode(args_node, current_value)
                args_node.add_child(arg_node)
        f_node.add_child(args_node)
        self.eat_token(1)
        assert(self.get_current_token_type() == BLOCK_START)
        self.parse(f_node)
        head.add_child(f_node)\

    def _do_import(self, head, import_type):
        self.eat_token(1)
        im_node = ImportNode(head, import_type)
        head.add_child(im_node)

    def _do_return(self, head):
        self.eat_token(1)
        r_node = ReturnNode(head)
        self.parse(r_node)
        head.add_child(r_node)

    def _do_while(self, head):
        """
        head -> BranchNode -> BlockNode(while) -> ConditionNode -> postfix_branches
                              BlockNode(do) -> BlockNode -> ...
        """
        self.eat_token(2)
        b_node = BranchNode(head, 'WHILE_BRANCH')
        while_node = self.parse_expr(b_node, self._get_equation_tokens(EQ_CONDITION))# assume it is an expression that can be parsed
        self.eat_token(1)
        b_node.add_child(while_node)
        assert(self.get_current_token_type() == BLOCK_START)
        do_node = BlockNode(b_node, 'WHILE_BLOCK')
        self.parse(do_node)
        b_node.add_child(do_node)
        head.add_child(b_node)

    def parse(self, current_parent):
        node = None
        pattern = self.get_token_cache()
        t1 = pattern[0].get_type()
        t2 = t3 = None
        if self._tokenidx + 1 < self._tokenlen:
            t2 = pattern[1].get_type()
        if self._tokenidx + 2 < self._tokenlen:
            t3 = pattern[2].get_type()
        if t1 == DEFINE and t2 == IDENTIFIER and t3 == ASSIGN:
            self._do_define(current_parent)
        elif t1 == COND_IF:
            self._do_if(current_parent)
        elif t1 == COND_FOR:
            self._do_for(current_parent)
        elif t1 == COND_WHILE:
            self._do_while(current_parent)
        elif t1 == F_RETURN:
            self._do_return(current_parent)
        elif t1 == IDENTIFIER:
            if t2 == CALL_PARAM_LIST:
                self._do_func_call(current_parent)
            elif t2 == STATEMENT_END:
                self._do_basic_assign(current_parent, is_number=False)
            else:
                self._do_expr(current_parent)
        elif type_is_number(t1):
            if t2 == STATEMENT_END:
                self._do_basic_assign(current_parent, is_number=True)
            else:
                self._do_expr(current_parent)
        elif type_is_expr(t1):
            self._do_expr(current_parent)
        elif t1 == FUNC_DECL:
            self._do_func_decl(current_parent)
        elif t1 == BLOCK_START:
            self._do_block(current_parent)
        elif t1 == NATIVE_IMPORT or t1 == C_IMPORT:
            self._do_import(current_parent, import_type=t1)
        else:
            parselogger.info("Couldn't find logic for token {0}".format(t1))
            self.eat_token(1)
        return node

    def tokens_to_ast(self):
        # Core loop for AST progression
        current_parent = self._ast.get_head()
        while self.has_remaining_tokens():
            self.parse(current_parent)

    def get_ast_dict(self):
        return self._ast.__str__()


if __name__ == '__main__':

    """ AST tree testing """

    debug_tokens = [('START_OF_PROGRAM', 'sop'), ('DEFINE', 'var'), ('IDENTIFIER', 'x'), ('ASSIGN', '='),
                    ('UNSIGNED_CHAR', '3'),('STATEMENT_END', ';'), ('DEFINE', 'var'), ('IDENTIFIER', 'y'),
                    ('ASSIGN', '='), ('SIGNED_CHAR', '-3'),('STATEMENT_END', ';'), ('DEFINE', 'var'),
                    ('IDENTIFIER', 'z'), ('ASSIGN', '='), ('IDENTIFIER', 'x'), ('STATEMENT_END', ';')]
    debug_eq_tokens =  [('START_OF_PROGRAM', 'sop'), ('DEFINE', 'var'), ('IDENTIFIER', 'x'),
                        ('ASSIGN', '='), ('UNSIGNED_CHAR', '3'),('ADD', '+'), ('UNSIGNED_CHAR', '5'),
                        ('MULTIPLY', '*'), ('UNSIGNED_CHAR', '7'), ('DIVIDE', '/'),('UNSIGNED_CHAR', '11'),
                        ('STATEMENT_END', ';')]
    debug_parser = Parser(debug_tokens)
    #thistree = debug_parser._ast.get_head()
    #print(thistree)
    print(debug_parser.get_ast_dict())