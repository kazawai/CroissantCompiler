from sys import argv, stderr

from lark import Lark, Token, Transformer, Tree, v_args
from lark.exceptions import UnexpectedInput
from modules.types.statement import Statement
from modules.utils import global_var
from modules.exceptions.exception import SPFException, SPFSyntaxError


class Interpreter(Transformer):

    @v_args()
    def interpret(self, args, statement_type=Statement()):
        if isinstance(args, Tree):
            type = args.data.upper()
            return statement_type[type](self.interpret(args.children))
        elif isinstance(args, Token):
            return args.value
        elif len(args) == 1 and isinstance(args[0], Token):
            return args[0].value
        else:
             return [self.interpret(node) for node in args]

def memory():
    for variable in global_var.context.keys():
        print(f"MEM: {global_var.context[variable]}", file=stderr)


if __name__ == "__main__":
    global_var.init()
    print(argv)
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
            print(context)
        """ 
        if "--debug" in argv[1:] or "-d" in argv[1:]:
            print("je passe")
            global_var.debug = True
        with open("sample/test.spf", "r") as file:
            for line in file:
                try:
                    try:
                        tree = parser.parse(line)
                        result = interpreter.interpret(tree)
                    except UnexpectedInput:
                        raise SPFSyntaxError()
                except SPFException as e:
                    print(e)
                    #break
                global_var.line_counter += 1
        if "--memory" in argv[1:] or "-m" in argv[1:]:
            memory()