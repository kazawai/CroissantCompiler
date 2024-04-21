from enum import Enum

from modules.utils.wrapper import Wrapper

def display_bool(b):
    bool_t = {True : "vrai", False : "faux"}
    return bool_t[b]

def display_list(l):
    return "[%s]" % ', '.join(map(str, l))


def display(args):
    display_items = {list : display_list, bool : display_bool}
    if type(args[1]) in display_items:
        print(display_items[type(args[1])](args[1]))
    else:
        print(args[1])


def display_seq(args):
    display_items = {list : display_list, bool : display_bool}
    items = args[1:]
    items = list(map(lambda x : display_items[type(x)](x) if type(x) in display_items else x, items))
    print("je passe1")
    print(" ".join(map(str,items)))

class System(Enum):
    """
    System Expr:
        used to define how system operations are defined.
        the system operations are printing and exiting program.
    """

    PRINT_SEQ = Wrapper(display_seq)
    PRINT = Wrapper(display)
    EXIT = Wrapper(exit)