import readline
from os import path
from sys import argv, stderr

from lark import (Lark, UnexpectedCharacters, UnexpectedEOF, UnexpectedInput,
                  UnexpectedToken)

from modules.exceptions.exception import SPFException, SPFSyntaxError
from modules.utils import global_var
from modules.utils.interpreter import Interpreter


def memory():
    for variable in global_var.context.keys():
        print(f"MEM: {global_var.context[variable]}", file=stderr)


def _read(file):
    if not path.exists(file):
        raise FileNotFoundError(f"fichier {file} non trouvé")
    print()
    if file[-4 : len(file)] != ".spf":
        raise FileNotFoundError(f"fichier {file} doit avoir l'extension '.spf'")
    with open(file, "r") as f:
        return f.read()


def prompt():
    input_ = input(">>> ")
    while input_ != "sortir":
        try:
            global_var.input = input_
            tree = parser.parse(input_)
            result = interpreter.interpret(tree)
            print(result if (result != [] and result != [None]) else "")
            input_ = input(">>> ")
        except UnexpectedInput as e:
            label = ""
            m = "Entrée non attendue"
            if isinstance(e, UnexpectedToken):
                label = e.token
            elif isinstance(e, UnexpectedCharacters):
                label = e.char
            elif isinstance(e, UnexpectedEOF):
                label = input_[-1]
                m = "Entrée non attendue, ';' attendu"

            global_var.line_counter = e.line
            print(SPFSyntaxError(m, label), file=stderr)
            input_ = ""
        except SPFException as e:
            print(e, file=stderr)
            input_ = ""
        # Cannot use finally as this actually resets the input everytime (not just after an exception)
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
                    input_ = _read(file)
                    global_var.input = input_
                    tree = parser.parse(input_)
                    result = interpreter.interpret(tree)
                except SPFException as e:
                    print(e, file=stderr)
                except UnexpectedToken as e:
                    label = ""
                    if isinstance(e, UnexpectedToken):
                        label = e.token
                    elif isinstance(e, UnexpectedCharacters):
                        label = e.char
                    global_var.line_counter = e.line
                    raise SPFSyntaxError(
                        "Symbole non-attendu lu dans le fichier", label
                    )
            else:
                prompt()
        if "--memory" in argv[1:] or "-m" in argv[1:]:
            memory()
    except SPFException as e:
        print(e, file=stderr)
    except Exception as e:
        print(e, file=stderr)
        print("\033[91mUne erreur est survenue, mémoire vidée\033[0m")
        memory()
