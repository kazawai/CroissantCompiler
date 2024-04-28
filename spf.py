"""
Entry of the programm where all the user input will be handled and interpreted.
"""

import readline as rl  # Readlines for easy history and copy-paste
from os import path
from sys import argv, stderr

from lark import (Lark, UnexpectedCharacters, UnexpectedEOF, UnexpectedInput,
                  UnexpectedToken)

from modules.exceptions.exception import SPFException, SPFSyntaxError
from modules.utils import global_var
from modules.utils.interpreter import Interpreter

GRAMMAR_PATH = "spf.lark"


def memory():
    """
    Show the memory (i.e. all variables) used during the execution of SPF programm
    """
    for variable in global_var.context.keys():
        print(f"MEM: {global_var.context[variable]}", file=stderr)


def _read(file):
    """
    Read a given SPF file to be interpreted
    """
    if not path.exists(file):  # not found with given path
        raise FileNotFoundError(f"fichier {file} non trouvé")
    print()
    if (
        file[-4 : len(file)] != ".spf"
    ):  # does not respect the naming convention of SPF files
        raise FileNotFoundError(f"fichier {file} doit avoir l'extension '.spf'")
    with open(file, "r") as f:
        return f.read()


def help():
    return """
BIENVENUE DANS LE PROGRAMME SPF !
    
Celui-ci permet d'interpreter du code SPF via un fichier ou via un interpréteur dédié.
Pour la syntaxe du langage, vous pouvez vous référer au fichier spf.lark écrit en EBNF
Pour ce qui est de la sémantique, la majorité se base sur celle de python (voir rapport pour plus de détails)

options
-------

    -h | --help : affiche le message d'aide
    -f | --file : prendre un fichier .spf en paramètre au programme (si pas spécifié, activation de l'interpréteur SPF)
    -d | --debug : activer le mode debug
    -m | --memory : afficher la mémoire totale utilisé lors de l'éxécution du programme
    
exemple
-------
    python spf.py -m -f sample/example.spf 
    python spf.py
"""


def prompt():
    """
    Interpreter mode : will ask an input infinitely and interpret it until the user put the exit command
    """
    input_ = input(">>> ")
    while True:
        try:
            global_var.input = input_
            tree = parser.parse(input_)
            result = interpreter.interpret(tree)
            print(result if (result != [] and result != [None]) else "")
            input_ = input(">>> ")
        except SPFException as e:
            print(e, file=stderr)
            input_ = ""
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

            global_var.line_counter = (
                e.line if hasattr(e, "line") else global_var.line_counter
            )
            print(SPFSyntaxError(m, label), file=stderr)
            input_ = ""
        # Cannot use finally as this actually resets the input everytime (not just after an exception)
        global_var.line_counter += 1


if __name__ == "__main__":
    global_var.init()  # instanciation of the needed globals variables
    try:
        with open(GRAMMAR_PATH, "r") as grammar:
            interpreter = Interpreter()  # entry of the spf interpreter
            parser = Lark(
                grammar,
                parser="lalr",  # in our case, one look ahead (i.e. LALR(1))
                transformer=interpreter,
                propagate_positions=True,  # used for getting current line
            )
            if "--help" in argv[1:] or "-h" in argv[1:]:
                print(help())
                exit()
            if "--debug" in argv[1:] or "-d" in argv[1:]:
                global_var.debug = True

            # if file path specified, will interpret it and return the result
            if "--file" in argv[1:] or "-f" in argv[1:]:
                start = (
                    argv.index("--file") if "--file" in argv[1:] else argv.index("-f")
                )
                file = argv[start + 1]
                try:
                    input_ = _read(file)
                    global_var.input = input_
                    parser.parse(input_)
                except SPFException as e:
                    print(e, file=stderr)
                except UnexpectedToken as e:
                    label = ""
                    if isinstance(e, UnexpectedToken):  # syntax error from grammar
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
        print(
            "\033[91mUne erreur est survenue, mémoire vidée\033[0m\n\033[92mutilisez -h si besoin\033[0m"
        )
        memory()
