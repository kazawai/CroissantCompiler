from lark import Token, Transformer, Tree, v_args
from modules.types.statement import Statement
from modules.utils.variable import Block, Variable

class Interpreter(Transformer):

    @v_args()
    def interpret(self, args, statement_type=Statement()):
        if isinstance(args, Tree):
            type = args.data.upper()
            if "COND" in type :
               return self.cond(type, args)
            elif type == "WHILE":
                return self.while_(args)
            elif type == "FOR":
                return self.for_(args)

            return statement_type[type](self.interpret(args.children))
        elif isinstance(args, Token):
            return args.value
        elif len(args) == 1 and isinstance(args[0], Token):
            return args[0].value
        else:
             return [self.interpret(node) for node in args]
        
    def cond(self, type, tree):
        block = Block()
        if self.interpret(tree.children[0]):
            self.interpret(tree.children[1])
        elif "ELSE" in type:
            self.interpret(tree.children[2])
        block.pop()

    def while_(self, tree):
        block = Block()
        while self.interpret(tree.children[0]):
            self.interpret(tree.children[1])
        block.pop()

    def for_(self, tree):
        block = Block()
        var = self.interpret(tree.children[0])
        l = self.interpret(tree.children[1])
        i = 0
        while i < len(l):
            Variable.modification([str(var.label), l[i]])
            self.interpret(tree.children[2])
            i += 1
        block.pop()
