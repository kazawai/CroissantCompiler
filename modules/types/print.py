from enum import Enum

from modules.utils.wrapper import Wrapper

bool_t = {True : "vrai", False : "faux"}

def display(args):
    if type(args[1]) != list:
        if type(args[1]) == bool:
            print(bool_t[args[1]])
        else:
            print(args[1])
    else:
        items = list(map(lambda x : bool_t[x] if type(x) == bool else x, args[1]))
        print(" ".join(map(str,items)))

class Print(Enum):
    """
    Print Expr:
        used to define how print operations are defined
    """

    PRINT = Wrapper(display)
