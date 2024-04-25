from lark import Token, Transformer, Tree, v_args

from modules.types.statement import Statement
from modules.utils.variable import Block, Variable, global_var


class Interpreter(Transformer):

    primitives = (int, str, bool)  # basic types

    @v_args()
    def interpret(self, args, statement_type=Statement()):
        """
        The main algorithm for interpreting a given input.
        This will visit each node of the syntax tree and interpret them with their given semantic rules
        according to the grammar (spf.lark)
        """
        if isinstance(args, Tree):
            type = args.data.upper()
            global_var.line_counter = args.meta.line
            # in the case of branching or loops -> work differently compared to basic semantic rules
            if "COND" in type:
                return self.cond(type, args)
            elif type == "WHILE":
                return self.while_(args)
            elif type == "FOR":
                return self.for_(args)
            elif type == "STATEMENT":
                return self.interpret(args.children[0])  # axiom of syntax tree

            return statement_type[type](self.interpret(args.children))
        elif isinstance(args, Token):
            return args.value  # lexem
        elif isinstance(args, list) and len(args) == 1 and isinstance(args[0], Token):
            return args[0].value  # same as lexem
        elif isinstance(args, Variable) or isinstance(args, self.primitives):
            return args
        elif args is None:  # Empty statement
            return None
        else:
            # basic inner nodes (i.e. productions)
            return [self.interpret(node) for node in args]

    def cond(self, type, tree):
        """
        Interpret branching condition in two ways specified by the type param:
            basic if -> interpret the body if the condition is respected
            if-else -> interpret the body of the if based of the correctness of the condition.
                       interpret the else if the condition of the if is not true
        """
        block = Block()
        if self.interpret(tree.children[0]):
            self.interpret(tree.children[1])
        elif "ELSE" in type:
            self.interpret(tree.children[2])
        block.pop()

    def while_(self, tree):
        """
        Interpret the children of the tree multiple times in accordance with the number of iterations
        needed based on the given condition of the loop.
        """
        block = Block()
        while self.interpret(tree.children[0]):
            self.interpret(tree.children[1])
        block.pop()

    def for_(self, tree):
        """
        Same as while except the fact that we are looking for one unique condition:
            Did we finish visiting the whole list ?
        """
        block = Block()
        var = self.interpret(tree.children[0])
        l = self.interpret(tree.children[1])
        i = 0
        while i < len(l):
            Variable.modification([str(var.label), l[i]])
            self.interpret(tree.children[2])
            i += 1
        block.pop()
