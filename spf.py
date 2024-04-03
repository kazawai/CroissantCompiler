import traceback
from os import path
from sys import argv, stderr

from lark import Lark, UnexpectedInput, UnexpectedToken
from lark.exceptions import UnexpectedInput

from modules.exceptions.exception import SPFException, SPFSyntaxError
from modules.utils import global_var
from modules.utils.interpreter import Interpreter


def memory():
    for variable in global_var.context.keys():
        print(f"MEM: {global_var.context[variable]}", file=stderr)


def _read(file):
    if not path.exists(file):
        raise FileNotFoundError(f"File {file} not found")
    with open(file, "r") as f:
        return f.read()


if __name__ == "__main__":
    global_var.init()
    try:
        with open("spf.lark", "r") as grammar:
            interpreter = Interpreter()
            parser = Lark(
                grammar,
                parser="lalr",
                transformer=interpreter,
                propagate_positions=True,
            )
            if "--debug" in argv[1:] or "-d" in argv[1:]:
                print("je passe")
                global_var.debug = True

            if "--file" in argv[1:] or "-f" in argv[1:]:
                start = (
                    argv.index("--file") if "--file" in argv[1:] else argv.index("-f")
                )
                file = argv[start + 1]
                try:
                    input = _read(file)
                    tree = parser.parse(input)
                    result = interpreter.interpret(tree)
                except SPFException as e:
                    print(e)
                except UnexpectedToken as e:
                    print(e.get_context(_read(file)))
                    print(e)
                    raise SPFSyntaxError()
            else:
                input_ = input(">>> ")
                while input_ != "sortir":
                    try:
                        try:
                            tree = parser.parse(input_)
                            result = interpreter.interpret(tree)
                            print(result)
                            input_ = input(">>> ")
                        except UnexpectedInput:
                            raise SPFSyntaxError()
                    except SPFException as e:
                        print(e)
                    global_var.line_counter += 1
        if "--memory" in argv[1:] or "-m" in argv[1:]:
            memory()
    except SPFException as e:
        print(e)
    except Exception as e:
        print(e)
        print("An error occurred, dumping memory")
        memory()
        traceback.print_exc()
