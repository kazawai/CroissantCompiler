from sys import platlibdir

from lark import Lark, Token, Transformer, Tree, v_args

from modules.statement import Statement
from modules.variable import global_context


class Interpreter(Transformer):

    @v_args()
    def interpret(self, args, statement_type=Statement()):
        print(args)
        if isinstance(args, Tree):
            type = args.data.upper()
            return statement_type[type](self.interpret(args.children))
        elif isinstance(args, Token):
            return args.value
        elif len(args) == 1 and isinstance(args[0], Token):
            return args[0].value
        else:
            return [self.interpret(node) for node in args]


if __name__ == "__main__":
    with open("spf.lark", "r") as grammar:
        interpreter = Interpreter()
        parser = Lark(
            grammar, start="statement", parser="lalr", transformer=interpreter
        )
        """
        while True:
            tree = parser.parse(input(">"))
            result = interpreter.interpret(tree)
            print(result)
            print(global_context)
        """
        with open("modules/test.spf", "r") as file:
            for line in file:
                print("----------------------------------")
                print(f"TEST : " + line)
                tree = parser.parse(line)
                result = interpreter.interpret(tree)
                print(result)
                print(global_context)
