from enum import Enum

from modules.utils.wrapper import Wrapper

def display_bool(b) -> str:
    """
    display_bool:
        used to display a boolean value in french.

    Parameters:
        b (bool): the boolean value to display.

    Returns:
        str: the boolean value in french.
    """
    bool_t = {True: "vrai", False: "faux"}
    return bool_t[b]


def display_list(l):
    """
    display_list:
        used to display a list.

    Parameters:
        l (list): the list to display.

    Returns:
        str: the list in string format.
    """
    return "[%s]" % ", ".join(map(str, l))


def render_displayable_item(item)->str:
    """
    render_displayable_item:
        used to display the nice string for the item value.

    Parameters:
        item : the argument to display.

    Returns:
        str: the value in string format.
    """
    bool_t = {True: "vrai", False: "faux"}
    if type(item) == bool:
        return bool_t[item]
    elif type(item) == list:
        return "[%s]" % ", ".join(map(render_displayable_item, item))
    elif type(item) == str:
        return '"'+ item +'"'
    return str(item)

def display(args):
   
    display_items = {list: display_list, bool: display_bool}
    if type(args[1]) in display_items:
        print(display_items[type(args[1])](args[1]))
    else:
        print(args[1])


def display_seq(args):
    """
    display_seq:
        used to display a sequence of values (inline lists).

    Parameters:
        args (list): the arguments to display.

    Returns:
        str: the sequence of values in string format.
    """
    display_items = {list: display_list, bool: display_bool}
    items = args[1:]
    items = list(
        map(
            lambda x: display_items[type(x)](x) if type(x) in display_items else x,
            items,
        )
    )
    print(" ".join(map(str, items)))


class System(Enum):
    """
    System Expr:
        used to define how system operations are defined.
        the system operations are printing and exiting program.
    """

    PRINT_SEQ = Wrapper(display_seq)
    PRINT = Wrapper(lambda args : print(render_displayable_item(args[1])))
    EXIT = Wrapper(exit)
