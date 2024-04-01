from enum import Enum

from modules.utils.wrapper import Wrapper


class Print(Enum):
    """
    Print Expr:
        used to define how print operations are defined
    """

    PRINT = Wrapper(lambda args: print(f"Print: {args[1]}"))
