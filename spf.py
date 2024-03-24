from lark import Lark, Token, Transformer, Tree, v_args

from modules.statement import Statement


class Interpreter(Transformer):

    context = {}

    @v_args()
    def interpret(self, args, statement_type=Statement()):
        if isinstance(args, Tree):
            type = args.data.upper()
            return statement_type[type](self.interpret(args.children), self.context)
        elif isinstance(args, Token):
            return args.value
        elif len(args) == 1 and isinstance(args[0], Token):
            return args[0].value
        else:
            return [self.interpret(node) for node in args]


if __name__ == "__main__":
    with open("spf.lark", "r") as grammar:
        parser = Lark(
            grammar, start="statement", parser="lalr", transformer=Interpreter()
        )
        while True:
            tree = parser.parse(input(">"))
            print(tree)
            result = Interpreter().interpret(tree)
            print(result)
