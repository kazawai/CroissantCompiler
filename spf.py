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
        raise FileNotFoundError(f"fichier {file} non trouvé")
    if file[-1:-3] != ".spf":
        raise FileNotFoundError(f"fichier {file} doit avoir l'extension '.spf'")
    with open(file, "r") as f:
        return f.read()

def prompt():
    input_ = input(">>> ")
    global_var.input = input_
    while input_ != "sortir":
        try:
            tree = parser.parse(input_)
            # print(tree)
            result = interpreter.interpret(tree)
            print(result)
            input_ = input(">>> ")
        except UnexpectedInput as e:
            print(e.get_context(input_))
            global_var.line_counter = e.line
            raise SPFSyntaxError("Entrée non attendue")
        except SPFException as e:
            print(e)
        global_var.line_counter += 1


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
                global_var.debug = True

            if "--file" in argv[1:] or "-f" in argv[1:]:
                start = (
                    argv.index("--file") if "--file" in argv[1:] else argv.index("-f")
                )
                file = argv[start + 1]
                try:
                    input = _read(file)
                    global_var.input = input
                    tree = parser.parse(input)
                    result = interpreter.interpret(tree)
                except SPFException as e:
                    print(e, file=stderr)
                except UnexpectedToken as e:
                    print(e.get_context(_read(file)))
                    global_var.line_counter = e.line
                    raise SPFSyntaxError("Symbole non-attendu lu dans le fichier")
            else:
                prompt()
        if "--memory" in argv[1:] or "-m" in argv[1:]:
            memory()
    except SPFException as e:
        print(e, file=stderr)
    except Exception as e:
        print(e, file=stderr)
        print("Une erreur est survenue, mémoire vidée")
        memory()
