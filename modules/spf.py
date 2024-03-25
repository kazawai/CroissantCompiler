from sys import argv

import lark
from lark import Lark, Transformer
from statement import Statement

GRAMMAR_PATH = "spf.lark"


class Interpretor(Transformer):

    def interpret(self, args, statement_type=Statement()):
        if isinstance(args, lark.Tree):
            type = args.data.upper()
            return statement_type[type](self.interpret(args.children))
        elif isinstance(args, lark.Token):
            return args.value
        elif len(args) == 1 and isinstance(args[0], lark.Token):
            return args[0].value
        else:
            return [self.interpret(node) for node in args]


if __name__ == "__main__":
    """
    with open(argv[1]) as file_input:
        with open(GRAMMAR_PATH, "r") as grammar:
            parser = Lark(grammar, parser="lalr", transformer=(Interpretor()))
            print(parser.parse(file_input.read()))
    """
    with open(GRAMMAR_PATH, "r") as grammar:
        parser = Lark(grammar, parser="lalr", transformer=Interpretor())
        while 1:
            print(parser.parse(input(">"))[0])
