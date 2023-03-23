def core(self, current_parent, tokenidx, bscope=0):
	# branches = 18
	# OPT: Less branches
	node = None
	pattern = self._tokenref[tokenidx:]
	t1 = pattern[0][TYPE_SLOT]
	t2 = t3 = None
	try:
		t2 = pattern[1][TYPE_SLOT]
	except IndexError:
		pass
	try:
		t3 = pattern[2][TYPE_SLOT]
	except IndexError:
		pass
	if t1 == DEFINE and t2 == IDENTIFIER and t3 == ASSIGN:
		self.eat_token(3)
		# var x =
		a_node = AssignNode(current_parent)
		i_node = IdentifierNode(a_node)
		a_node.add_child(i_node)
		self.core(a_node, self._tokenidx, bscope)
		current_parent.add_child(a_node)
	elif t1 == COND_IF:
		self.eat_token(2) # if (
		b_node = BranchNode(current_parent)
		eq_tokens = self._get_equation_tokens(EQ_CONDITION)
		cond_node = self.parse_expr(b_node, eq_tokens)
		self.eat_token(1) # )
		assert(self.get_current_token() == BLOCK_START)
		b_node.add_child(cond_node)
		self.core(b_node, self._tokenidx, bscope)
		if(self.get_current_token() == COND_ELSE):
			self.eat_token(1) # else
			self.core(b_node, self._tokenidx, bscope)
		current_parent.add_child(b_node)
	elif t1 == COND_FOR:
		b_node = BranchNode(current_parent)
	elif t1 == COND_WHILE:
		b_node = BranchNode(current_parent)
	elif t1 == IDENTIFIER and t2 == CALL_PARAM_LIST:
		self.eat_token(2) # get func name here
		# used to decide if an argument is an expression or not
		arg_len = 0
		fc_node = FunctionStatementNode(current_parent)
		args_node = ArgumentsNode(fc_node)
		while self.get_current_token() != CALL_PARAM_END:
			# NOTE: This program will break when call_param tokens are expression tokens!
			arg_node = ArgumentNode(args_node)
			self.core(arg_node, self._tokenidx, bscope)
	elif type_is_number(t1):
		if t2 == STATEMENT_END or t2 == CALL_SEPERATOR:
			self.eat_token(2)
			lit_node = LiteralNode(current_parent)
			current_parent.add_child(lit_node)
		else:
			# get the equation tokens and amount of tokens
			eq_tokens = self._get_equation_tokens(EQ_NORMAL)
			# parse expression
			expr_node = self.parse_expr(current_parent, eq_tokens)
			current_parent.add_child(expr_node)
	elif t1 == IDENTIFIER:
		if t2 == STATEMENT_END or t2 == CALL_SEPERATOR:
			self.eat_token(2)
			iden_node = IdentifierNode(current_parent)
			current_parent.add_child(iden_node)
		else:
			eq_tokens = self._get_equation_tokens(EQ_NORMAL)
			expr_node = self.parse_expr(current_parent, eq_tokens)
			current_parent.add_child(expr_node)
	elif t1 == DEF_PARAM_LIST:
		self.eat_token(1)
		f_node = FunctionDeclNode(current_parent)
		args_node = ArgumentsNode(f_node)
		idx = 0
		next_type = None
		# encapsulation for funcdecl->arguments
		while next_type is not BLOCK_START:
			self.eat_token(1)
			# param || param_sep
			next_type = pattern[idx][TYPE_SLOT]
			idx += 1
			if next_type == DEF_PARAM:
				arg_node = ArgumentNode(args_node)
				f_node.add_child(arg_node)
			elif next_type == DEF_PARAM_END:
				f_node.add_child(args_node)
		self.core(f_node, self._tokenidx, bscope)
	elif t1 == BLOCK_START:
		s_node = StatementNode(current_parent)
		bscope += 1
		this_bscope = bscope
		next_type = t2
		while next_type is not BLOCK_END and bscope == this_bscope:
			next_type = pattern[self._tokenidx][TYPE_SLOT]
			self.core(s_node, self._tokenidx, bscope)
		current_parent.add_child(s_node)
		assert(self.get_current_token() == BLOCK_END)
		self.eat_token(1)
		bscope -= 1
	else:
		print("couldnt find logic for token {0}".format(t1))
		self.eat_token(1)
	return node