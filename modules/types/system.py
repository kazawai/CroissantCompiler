from enum import Enum

from modules.utils.wrapper import Wrapper

def display_bool(b):
    bool_t = {True : "vrai", False : "faux"}
    return bool_t[b]

def display_list(l):
    return "[%s]" % ', '.join(map(str, l))

display_items = {list : display_list, bool : display_bool}

def display(args):
    if type(args[1]) in display_items:
        print(display_items[type(args[1])](args[1]))
    print(args[1])


def display_seq(args):
    items = args[1:]
    items = list(map(lambda x : display_items[type(x)](x) if type(x) in display_items else x, items))
    print(" ".join(map(str,items)))

class System(Enum):
    """
    Print Expr:
        used to define how print operations are defined
    """

    PRINT_SEQ = Wrapper(display_seq)
    PRINT = Wrapper(display)
    EXIT = Wrapper(exit)