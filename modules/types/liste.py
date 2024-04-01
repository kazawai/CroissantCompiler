from enum import Enum

from modules.utils.wrapper import Wrapper
from modules.exceptions.exception import SPFIndexError


def list_bc(args):
    return []


def list_gc(args):
    if len(args) > 1:
        return list(args[0])
    return args[0]


def concat_list(args):
    return args[0] + args[1]


def index_list(args):
    if args[1] < 0 or args[1] >= len(args[0]):
        raise SPFIndexError(args[1], len(args[0]))
    return args[0][args[1]]


def size_list(args):
    return len(args[0])


def range_list(args):
    return list(range(args[0], args[1]))

def add(args):
    if type(args[1]) != list:
        args[1] = [args[1]]
    return args[1] + [args[0]]

class ListExpression(Enum):
    LIST_BC = Wrapper(list_bc)
    LIST_GC = Wrapper(list_gc)
    CONCAT_LIST = Wrapper(concat_list)
    INDEX_LIST = Wrapper(index_list)
    SIZE_LIST = Wrapper(size_list)
    RANGE_LIST = Wrapper(range_list)
    SEQUENCE = Wrapper(lambda args: list(args))
    ADD = Wrapper(add)
