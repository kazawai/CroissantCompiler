from enum import Enum

from modules.utils.wrapper import Wrapper


def display(args):

    bool_t = {True : "vrai", False : "faux"}
    if type(args[1]) == bool:
        return print(bool_t[args[1]])
    return print(args[1])

class Print(Enum):
    """
    Print Expr:
        used to define how print operations are defined
    """

    PRINT = Wrapper(display)
