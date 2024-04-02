from lark import Token, Transformer, Tree, v_args
from modules.types.statement import Statement
from modules.utils import global_var
from modules.utils.variable import Block

class Interpreter(Transformer):

    @v_args()
    def interpret(self, args, statement_type=Statement()):
        if isinstance(args, Tree):
            type = args.data.upper()
            if "COND" in type :
               return self.cond(type, args)
            return statement_type[type](self.interpret(args.children))
        elif isinstance(args, Token):
            return args.value
        elif len(args) == 1 and isinstance(args[0], Token):
            return args[0].value
        else:
             return [self.interpret(node) for node in args]
        
    def cond(self, type, tree):
        block = Block()
        interpreted = None
        if self.interpret(tree.children[0]):
            interpreted = self.interpret(tree.children[1])
        elif "ELSE" in type:
            interpreted = self.interpret(tree.children[2])
        block.pop()
        return interpreted
    

