from enum import Enum

from modules.wrapper import Wrapper


class Assignment(Enum):
    ASSIGNMENT = Wrapper(lambda args: print(args))
